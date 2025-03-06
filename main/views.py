from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from main.models import Category, Article, UserProfile, Comment, Forum, Thread, Post, Poll, PollOption, UNIVERSITY_CHOICES
from main.forms import CategoryForm, ArticleForm, UserProfileForm, CommentForm, ForumForm, ThreadForm, PostForm, PollForm, PollOptionForm
from datetime import datetime
from main.bing_search import run_query
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import logout
from django.utils.safestring import mark_safe
from django.forms import formset_factory
import json

BANNED_WORDS = [
    # Profanity & Swear Words
    "fuck", "shit", "damn", "bitch", "ass", "asshole", "bastard", "prick", "wanker",
    "bollocks", "dick", "cunt", "twat", "arse", "arsehole",

    # Sexually Explicit Terms
    "porn", "hentai", "blowjob", "anal", "dildo", "vibrator", "cum", "orgasm",
    "pussy", "deepthroat", "threesome", "gangbang", "incest", "sex", "shag", "fucking"

    # Violent & Threatening Language
    "kill yourself", "die", "murder you", "bomb", "terrorist", "execute",
    "massacre", "suicide", "genocide", "kill you", "murder", "gun", "shoot", "blood"

    # Hate Speech & Harassment
    "retard", "cripple", "faggot", "dyke", "tranny", "spastic", "gimp",
    "fag", "stupid", "idiot", "dumb",

    # Drug & Substance-Related Terms
    "weed", "cocaine", "heroin", "meth", "ecstasy", "lsd", "shrooms", 
    "ketamine", "overdose",

    # Self-Harm & Suicide References
    "cut myself", "end my life", "overdose", "slit my wrists", "i want to die", "kill myself", "kms",

    # Scam & Spam Words
    "free money", "click here", "earn cash", "work from home", "make millions",
    "hot singles", "win a prize"
]

def get_server_side_cookie(request, cookie, default_val=None):

    val = request.session.get(cookie)
    
    if not val:
    
        val = default_val
    
    return val

def visitor_cookie_handler(request):
    
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
    
        visits = visits + 1
    
        request.session['last_visit'] = str(datetime.now())
    
    else:
    
        request.session['last_visit'] = last_visit_cookie
    
    request.session['visits'] = visits

class IndexView(View):

    def get(self, request):

        context_dict = {}

        category_list = Category.objects.order_by('-views')[:5]

        context_dict['categories'] = category_list

        article_list = Article.objects.order_by('-points')[:5]

        context_dict['articles'] = article_list
        
        comments = Comment.objects.order_by('-written_on')[:5]

        context_dict['comments'] = comments

        threads = Thread.objects.annotate(post_count=Count('post')).order_by('-updated_on')[:5]
        
        context_dict['threads'] = threads

        university_articles = []
        
        university_threads = []
        
        if request.user.is_authenticated and request.user.userprofile.university:
        
            user_university = request.user.userprofile.university
        
            university_articles = Article.objects.filter(related_university=user_university).order_by('-created_on')[:3]
        
            university_threads = Thread.objects.annotate(post_count=Count('post')).filter(related_university=user_university).order_by('-updated_on')[:3]

        context_dict['university_articles'] = university_articles
        
        context_dict['university_threads'] = university_threads
        
        context_dict['user_has_university'] = bool(request.user.is_authenticated and request.user.userprofile.university)
        
        visitor_cookie_handler(request)

        return render(request, 'rango/index.html', context=context_dict)

class AboutView(View):

    def get(self, request):
 
        context_dict = {}

        context_dict['founder_profile'] = UserProfile.objects.filter(user__username='aaronhxx_1').first()

        context_dict['developer_profile'] = UserProfile.objects.filter(user__username='phoebe6504').first()

        context_dict['marketing_profile'] = UserProfile.objects.filter(user__username='euan_galloway').first()

        context_dict['system_profile'] = UserProfile.objects.filter(user__username='urangoo123').first()

        visitor_cookie_handler(request)

        context_dict['visits'] = request.session.get('visits', 0)

        return render(request, 'rango/about.html', context_dict)

class PrivacyView(View):

    def get(self, request):

        return render(request, 'rango/privacy.html')
    
class TermsView(View):  

    def get(self, request):

        return render(request, 'rango/terms.html')
    
class MissionVisionView(View):
    
    def get(self, request):

        return render(request, 'rango/mission_vision.html')

class ContactView(View):

    def get(self, request):

        return render(request, 'rango/contact.html')

class ValuesView(View):

    def get(self, request):

        return render(request, 'rango/values.html')

class StatsView(View):

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def get(self, request):
        
        context_dict = {}
        
        context_dict['total_cats'] = Category.objects.count()
        
        context_dict['total_articles'] = Article.objects.count()
        
        context_dict['total_comments'] = Comment.objects.count()
        
        context_dict['total_users'] = User.objects.count()
        
        context_dict['total_forums'] = Forum.objects.count()
        
        context_dict['total_threads'] = Thread.objects.count()
        
        context_dict['total_posts'] = Post.objects.count()

        total_points = sum(article.points for article in Article.objects.all())
        
        total_views = sum(article.views for article in Article.objects.all())

        context_dict['total_points'] = total_points
        
        context_dict['total_views'] = total_views

        category_stats = {}
        
        category_names, category_points, category_views = [], [], []

        for category in Category.objects.all():
        
            articles_sum = category.article_set.count()
        
            category_points_sum = sum(article.points for article in category.article_set.all())
        
            category_views_sum = sum(article.views for article in category.article_set.all())

            category_stats[category.name] = {
                'number': articles_sum,
                'points': category_points_sum,
                'views': category_views_sum
            }

            category_names.append(category.name)
        
            category_points.append(category_points_sum)

            category_views.append(category_views_sum)

        context_dict['category_stats'] = category_stats

        context_dict['category_points'] = mark_safe(json.dumps(category_points))

        context_dict['category_views'] = mark_safe(json.dumps(category_views))

        context_dict['category_names'] = mark_safe(json.dumps(category_names))

        return render(request, 'rango/stats.html', context_dict)

class RegisterProfileView(View):

    @method_decorator(login_required)
    def get(self, request):

        form = UserProfileForm()

        context_dict = {'form': form}

        return render(request, 'rango/profile_registration.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request):

        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():

            user_profile = form.save(commit=False)

            user_profile.user = request.user

            user_profile.save()

            return redirect(reverse('rango:index'))
        
        else:
        
            print(form.errors)
        
        context_dict = {'form': form}
        
        return render(request, 'rango/profile_registration.html', context_dict)

class ProfileView(View):
    
    def get_user_details(self, username):
    
        try:
    
            user = User.objects.get(username=username)
    
        except User.DoesNotExist:
    
            return None
        
        user_profile = UserProfile.objects.get_or_create(user=user)[0]

        articles = Article.objects.filter(author=user).select_related("category").order_by('created_on')

        threads = Thread.objects.filter(author=user).select_related("forum").order_by('created_on')

        if user.is_authenticated and user.userprofile.university:
        
            user_university = user.userprofile.university
        
        user_has_university = bool(user.is_authenticated and user.userprofile.university)
        
        return (user, user_profile, articles, threads, user_has_university)
    
    @method_decorator(login_required)
    def get(self, request, username):

        try:
        
            (user, user_profile, articles, threads, user_has_university) = self.get_user_details(username)
        
        except TypeError:
        
            return redirect(reverse('rango:index'))
        
        context_dict = {'user_profile': user_profile, 'selected_user': user, 'articles': articles, 'threads': threads, 'user_has_university': user_has_university}
        
        return render(request, 'rango/profile.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, username):

        try:

            (user, user_profile, articles, threads, user_has_university) = self.get_user_details(username)

        except TypeError:

            return redirect(reverse('rango:index'))
        
        context_dict = {'user_profile': user_profile, 'selected_user': user, 'articles': articles, 'threads': threads, 'user_has_university': user_has_university}
        
        return render(request, 'rango/profile.html', context_dict)

class ListProfilesView(View):

    @method_decorator(login_required)
    def get(self, request):

        profiles = UserProfile.objects.all()

        return render(request, 'rango/list_profiles.html', {'users_list': profiles})

class DeleteAccountConfirmationView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
  
        return render(request, 'rango/confirm_delete_account.html')


class DeleteAccountView(View):

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
  
        user = request.user
  
        logout(request)
  
        user.delete()
  
        messages.success(request, "Your account has been successfully deleted.")
  
        return redirect('rango:index')

class CategoryListView(View):

    def get(self, request):

        context_dict = {}

        categories = Category.objects.all()
        
        context_dict['categories'] = categories

        return render(request, 'rango/category_list.html', context_dict)

class ShowCategoryView(View):

    def create_context_dict(self, category_name_slug):

        context_dict = {}

        try:

            category = Category.objects.get(slug=category_name_slug)

            category.views += 1

            category.save()

            articles = Article.objects.filter(category=category).order_by('-views')

            context_dict['articles'] = articles

            context_dict['category'] = category

        except Category.DoesNotExist:

            context_dict['articles'] = None

            context_dict['category'] = None
        
        return context_dict
    
    def get(self, request, category_name_slug):

        context_dict = self.create_context_dict(category_name_slug)

        return render(request, 'rango/category.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, category_name_slug):

        context_dict = self.create_context_dict(category_name_slug)

        query = request.POST['query'].strip()

        if query:

            context_dict['result_list'] = run_query(query)

            context_dict['query'] = query
        
        return render(request, 'rango/category.html', context_dict)

class AddCategoryView(View):

    @method_decorator(login_required)
    def get(self, request):
        
        if not request.user.is_staff:

            return redirect(reverse('rango:index'))

        form = CategoryForm()

        return render(request, 'rango/add_category.html', {'form': form})
    
    @method_decorator(login_required)
    def post(self, request):
        
        if not request.user.is_staff:

            return redirect(reverse('rango:index'))

        form = CategoryForm(request.POST)

        if form.is_valid():

            form.save(commit=True)

            return redirect(reverse('rango:index'))
        
        else:

            print(form.errors)
        
        return render(request, 'rango/add_category.html', {'form': form})

class LikeCategoryView(View):

    @method_decorator(login_required)
    def get(self, request):

        category_id = request.GET['category_id']

        try:

            category = Category.objects.get(id=int(category_id))

        except Category.DoesNotExist:

            return HttpResponse(-1)
        
        except ValueError:

            return HttpResponse(-1)
        
        category.points = category.points + 1

        category.save()

        return HttpResponse(category.points)

class DislikeCategoryView(View):

    @method_decorator(login_required)
    def get(self, request):

        category_id = request.GET['category_id']

        try:

            category = Category.objects.get(id=int(category_id))

        except Category.DoesNotExist:

            return HttpResponse(-1)
        
        except ValueError:

            return HttpResponse(-1)
        
        category.points = category.points - 1

        category.save()

        return HttpResponse(category.points)

def get_category_list(max_results=0, starts_with=''):

    category_list = []

    if starts_with:

        category_list = Category.objects.filter(name__istartswith=starts_with).order_by('-views')

    else:
        
        category_list = Category.objects.order_by('name')
    
    if max_results > 0:

        if len(category_list) > max_results:

            category_list = category_list[:max_results]
    
    return category_list

class CategorySuggestionView(View):

    def get(self, request):

        if 'suggestion' in request.GET:

            suggestion = request.GET['suggestion']
        
        else:

            suggestion = ''

        category_list = get_category_list(max_results=5, starts_with=suggestion)

        if len(category_list) == 0:

            category_list = Category.objects.order_by('name')
        
        return render(request, 'rango/categories.html', {'categories': category_list})

class ShowArticleView(View):

    def create_context_dict(self, category_name_slug, article_title_slug):

        context_dict = {}

        try:

            category = Category.objects.get(slug=category_name_slug)
            
            context_dict['category'] = category

            article = Article.objects.get(slug=article_title_slug)
            
            context_dict['article'] = article

            article.views += 1
            
            article.save()

            comments = Comment.objects.filter(article=article).order_by('-written_on')
            
            context_dict['comments'] = comments

        except Category.DoesNotExist:

            context_dict['category'] = None

            context_dict['article'] = None

            context_dict['comments'] = None

        except Article.DoesNotExist:
            
            context_dict['article'] = None

            context_dict['comments'] = None

        return context_dict

    def get(self, request, category_name_slug, article_title_slug):
        
        context_dict = self.create_context_dict(category_name_slug, article_title_slug)
        
        context_dict['form'] = CommentForm()
        
        return render(request, 'rango/article.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, category_name_slug, article_title_slug):
        
        context_dict = self.create_context_dict(category_name_slug, article_title_slug)

        form = CommentForm(request.POST)
        
        if form.is_valid():

            content = form.cleaned_data['content']

            if any(word in content.lower() for word in BANNED_WORDS):

                storage = messages.get_messages(request)
                
                storage.used = True

                messages.error(request, "Your comment contains innappropriate content and was not posted.")
        
            else:

                comment = form.save(commit=False)
            
                comment.article = context_dict['article']
            
                comment.user = request.user
            
                comment.save()

                messages.success(request, "Your comment has been posted successfully.")
        
            return redirect('rango:show_article', category_name_slug=category_name_slug, article_title_slug=article_title_slug)
        
        context_dict['form'] = form
        
        return render(request, 'rango/article.html', context_dict)

class AddArticleView(View):

    def get_category_name(self, category_name_slug):

        try:

            category = Category.objects.get(slug=category_name_slug)

        except Category.DoesNotExist:

            category = None
        
        return category
    
    @method_decorator(login_required)
    def get(self, request, category_name_slug):

        form = ArticleForm()

        category = self.get_category_name(category_name_slug)

        if category is None:

            return redirect(reverse('rango:index'))
        
        context_dict = {'form': form, 'category': category}

        return render(request, 'rango/add_article.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, category_name_slug):

        form = ArticleForm(request.POST, request.FILES)

        category = self.get_category_name(category_name_slug)

        if category is None:

            return redirect(reverse('rango:index'))
        
        if form.is_valid():

            article = form.save(commit=False)

            article.category = category

            article.views = 0

            article.points = 0

            article.save()

            return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        
        else:

            print(form.errors)
        
        context_dict = {'form': form, 'category': category}

        return render(request, 'rango/add_article.html', context=context_dict)

class LikeArticleView(View):

    @method_decorator(login_required)
    def get(self, request):

        article_id = request.GET['article_id']

        try:

            article = Article.objects.get(id=int(article_id))

        except Article.DoesNotExist:

            return HttpResponse(-1)
        
        except ValueError:

            return HttpResponse(-1)
        
        article.points = article.points + 1

        article.save()

        return HttpResponse(article.points)

class DislikeArticleView(View):

    @method_decorator(login_required)
    def get(self, request):

        article_id = request.GET['article_id']

        try:

            article = Article.objects.get(id=int(article_id))

        except Article.DoesNotExist:

            return HttpResponse(-1)
        
        except ValueError:

            return HttpResponse(-1)
        
        article.points = article.points - 1

        article.save()

        return HttpResponse(article.points)

@login_required
def favourite_article(request, article_slug):
    
    article = get_object_or_404(Article, slug=article_slug)
    
    user_profile = request.user.userprofile

    if article in user_profile.favourite_articles.all():
    
        user_profile.favourite_articles.remove(article)
    
    else:
    
        user_profile.favourite_articles.add(article)

    return redirect('rango:show_article', category_name_slug=article.category.slug, article_title_slug=article.slug)

class ForumListView(View):

    def get(self, request):

        context_dict = {}

        forums = Forum.objects.all()
        
        context_dict['forums'] = forums

        return render(request, 'rango/forum_list.html', context_dict)
    
class AddForumView(View):

    @method_decorator(login_required)
    def get(self, request):
        
        if not request.user.is_staff:

            return redirect(reverse('rango:index'))

        form = ForumForm()

        return render(request, 'rango/add_forum.html', {'form': form})
    
    @method_decorator(login_required)
    def post(self, request):
        
        if not request.user.is_staff:

            return redirect(reverse('rango:index'))

        form = ForumForm(request.POST)

        if form.is_valid():

            form.save(commit=True)

            return redirect(reverse('rango:index'))
        
        else:

            print(form.errors)
        
        return render(request, 'rango/add_forum.html', {'form': form})

class ThreadListView(View):

    def get(self, request, forum_name_slug):

        context_dict = {}

        try:

            forum = Forum.objects.get(slug=forum_name_slug)

            threads = Thread.objects.filter(forum=forum)

            context_dict['threads'] = threads

            context_dict['forum'] = forum

        except Forum.DoesNotExist:

            context_dict['threads'] = None

            context_dict['forum'] = None

        return render(request, 'rango/thread_list.html', context_dict)

class CreateThreadView(View):

    def get_forum_name(self, forum_name_slug):
    
        try:
    
            forum = Forum.objects.get(slug=forum_name_slug)
    
        except Forum.DoesNotExist:
    
            forum = None
    
        return forum

    @method_decorator(login_required)
    def get(self, request, forum_name_slug):
    
        forum = self.get_forum_name(forum_name_slug)

        if forum is None:
    
            return redirect(reverse('rango:index'))

        form = ThreadForm()
    
        return render(request, 'rango/create_thread.html', {'form': form, 'forum': forum})

    @method_decorator(login_required)
    def post(self, request, forum_name_slug):
    
        forum = self.get_forum_name(forum_name_slug)

        if forum is None:
    
            return redirect(reverse('rango:index'))

        form = ThreadForm(request.POST)

        if form.is_valid():
    
            thread = form.save(commit=False)
    
            thread.forum = forum
    
            thread.author = request.user
    
            thread.save()

            return redirect(reverse('rango:thread_list', kwargs={'forum_name_slug': forum.slug}))

        return render(request, 'rango/create_thread.html', {'form': form, 'forum': forum})

@method_decorator(login_required, name='dispatch')
class ThreadDetailView(View):

    def create_context_dict(self, forum_name_slug, thread_title_slug):
        
        context_dict = {}

        try:

            forum = Forum.objects.get(slug=forum_name_slug)

            context_dict['forum'] = forum

            thread = Thread.objects.get(slug=thread_title_slug, forum=forum)

            context_dict['thread'] = thread

            posts = Post.objects.filter(thread=thread).order_by('created_on')

            context_dict['posts'] = posts

            poll = Poll.objects.filter(thread=thread).first()

            context_dict['poll'] = poll

        except Forum.DoesNotExist:

            context_dict['forum'] = None

            context_dict['thread'] = None

            context_dict['posts'] = None

            context_dict['poll'] = None

        except Thread.DoesNotExist:

            context_dict['thread'] = None

            context_dict['posts'] = None

            context_dict['poll'] = None

        except Poll.DoesNotExist:

            context_dict['poll'] = None

        return context_dict

    def get(self, request, forum_name_slug, thread_title_slug):

        context_dict = self.create_context_dict(forum_name_slug, thread_title_slug)
        
        if context_dict['thread'] is None:

            context_dict['thread_not_found'] = True

        else:

            context_dict['thread_not_found'] = False
        
        form = PostForm()

        context_dict['form'] = form

        poll = context_dict.get('poll')

        if poll:

            poll_options = poll.options.all()

            context_dict['poll_options'] = poll_options

        return render(request, "rango/thread_detail.html", context_dict)

    def post(self, request, forum_name_slug, thread_title_slug):

        context_dict = self.create_context_dict(forum_name_slug, thread_title_slug)

        form = PostForm(request.POST)

        if form.is_valid():

            post = form.save(commit=False)

            post.thread = context_dict.get('thread')

            post.author = request.user

            post.save()

            thread = context_dict.get('thread')

            if thread:

                thread.updated_on = timezone.now()

                thread.save()

            return redirect("rango:thread_detail", forum_name_slug=context_dict['category'].slug, thread_title_slug=thread.slug)

        context_dict['form'] = form
        
        return render(request, "rango/thread_detail.html", context_dict)

@login_required
def save_thread(request, thread_slug):

    thread = get_object_or_404(Thread, slug=thread_slug)

    user_profile = request.user.userprofile

    if thread in user_profile.saved_threads.all():

        user_profile.saved_threads.remove(thread)
    
    else:

        user_profile.saved_threads.add(thread)

    return redirect('rango:thread_detail', forum_name_slug=thread.forum.slug, thread_title_slug=thread.slug)

@method_decorator(login_required, name='dispatch')
class PollVoteView(View):

    def get_forum(self, forum_name_slug):
    
        try:
    
            return Forum.objects.get(slug=forum_name_slug)
    
        except Forum.DoesNotExist:
    
            return None

    def get_thread(self, forum, thread_title_slug):
    
        try:
    
            return Thread.objects.get(slug=thread_title_slug, forum=forum)
    
        except Thread.DoesNotExist:
    
            return None

    def get_poll(self, thread):
    
        try:
    
            return Poll.objects.get(thread=thread)
    
        except Poll.DoesNotExist:
    
            return None

    def get_option(self, poll, option_id):
    
        try:
    
            return PollOption.objects.get(id=option_id, poll=poll)
    
        except PollOption.DoesNotExist:
    
            return None

    def post(self, request, forum_name_slug, thread_title_slug):
    
        forum = self.get_forum(forum_name_slug)
    
        if not forum:
    
            return JsonResponse({'status': 'error', 'message': 'Forum not found'}, status=404)

        thread = self.get_thread(forum, thread_title_slug)
    
        if not thread:
    
            return JsonResponse({'status': 'error', 'message': 'Thread not found'}, status=404)

        poll = self.get_poll(thread)
    
        if not poll:
    
            return JsonResponse({'status': 'error', 'message': 'Poll not found'}, status=404)

        option_id = request.POST.get('option_id')
    
        if not option_id:
    
            return JsonResponse({'status': 'error', 'message': 'Invalid vote'}, status=400)

        option = self.get_option(poll, option_id)
    
        if not option:
    
            return JsonResponse({'status': 'error', 'message': 'Poll option not found'}, status=404)

        if request.user in option.voted_users.all():
    
            return JsonResponse({'status': 'error', 'message': 'You have already voted!'}, status=400)

        option.votes += 1
    
        option.voted_users.add(request.user)
    
        option.save()

        return JsonResponse({'status': 'success', 'votes': option.votes})

@method_decorator(login_required, name='dispatch')
class AddPollView(View):

    def get_forum(self, forum_name_slug):
    
        try:
    
            return Forum.objects.get(slug=forum_name_slug)
    
        except Forum.DoesNotExist:
    
            return None

    def get_thread(self, forum, thread_title_slug):
    
        try:
    
            return Thread.objects.get(slug=thread_title_slug, forum=forum)
    
        except Thread.DoesNotExist:
    
            return None

    def get(self, request, forum_name_slug, thread_title_slug):
        
        if not request.user.is_staff:

            return redirect(reverse('rango:index'))
    
        forum = self.get_forum(forum_name_slug)
    
        if not forum:
    
            return redirect('rango:index')

        thread = self.get_thread(forum, thread_title_slug)
    
        if not thread:
    
            return redirect('rango:index')

        poll_form = PollForm()
    
        PollOptionFormSet = formset_factory(PollOptionForm, extra=3)
    
        option_formset = PollOptionFormSet()

        context_dict = {
            'forum': forum,
            'thread': thread,
            'poll_form': poll_form,
            'option_formset': option_formset,
        }
    
        return render(request, 'rango/add_poll.html', context_dict)

    def post(self, request, forum_name_slug, thread_title_slug):
        
        if not request.user.is_staff:

            return redirect(reverse('rango:index'))
    
        forum = self.get_forum(forum_name_slug)
    
        if not forum:
    
            return redirect('rango:index')

        thread = self.get_thread(forum, thread_title_slug)
    
        if not thread:
    
            return redirect('rango:index')

        poll_form = PollForm(request.POST)

        PollOptionFormSet = formset_factory(PollOptionForm, extra=3)

        option_formset = PollOptionFormSet(request.POST)

        if poll_form.is_valid() and option_formset.is_valid():

            poll = poll_form.save(commit=False)

            poll.thread = thread

            poll.save()

            for option_form in option_formset:

                if option_form.cleaned_data.get("option_text"):

                    option = option_form.save(commit=False)

                    option.poll = poll

                    option.save()

            return redirect('rango:thread_detail', forum_name_slug=forum.slug, thread_title_slug=thread.slug)

        context_dict = {
            'forum': forum,
            'thread': thread,
            'poll_form': poll_form,
            'option_formset': option_formset,
        }

        return render(request, 'rango/add_poll.html', context_dict)