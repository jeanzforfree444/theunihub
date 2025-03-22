from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from main.models import Category, Article, UserProfile, Comment, Forum, Thread, Post, Poll, PollOption, UNIVERSITY_CHOICES
from main.forms import CategoryForm, ArticleForm, UserProfileForm, ProfilePictureForm, CommentForm, ForumForm, ThreadForm, PostForm, PollForm, PollOptionForm
from datetime import datetime, timedelta
from main.bing_search import run_query
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.utils.safestring import mark_safe
from django.forms import formset_factory
from django.template.loader import render_to_string
from django.conf import settings
import json

# List of banned words used for content filtering
BANNED_WORDS = [
    # Profanity and Offensive Language
    "fuck", "shit", "damn", "bitch", "ass", "asshole", "bastard", "prick", "wanker",
    "bollocks", "dick", "cunt", "twat", "arse", "arsehole", "motherfucker", "slut", "whore",
    "piss", "fag", "faggot", "cock", "pussy", "bastard", "douche", "cocksucker", "dickhead",
    "shithead", "fuckhead", "fucktard", "nigger", "nigga", "chink", "spic", "kike", "gook",

    # Sexual Content and Explicit Terms
    "porn", "hentai", "blowjob", "anal", "dildo", "vibrator", "cum", "orgasm",
    "pussy", "deepthroat", "threesome", "gangbang", "incest", "sex", "shag", "fucking",
    "sexually", "bukkake", "fisting", "rape", "fetish", "sexting", "cunnilingus", "masturbation",
    "moaning", "orgy", "ejaculate", "cumshot", "penis", "vagina", "erection", "busty", "boobs", "tits", 

    # Violence, Threats, and Harmful Content
    "kill yourself", "die", "murder you", "bomb", "terrorist", "execute", "massacre", 
    "suicide", "genocide", "kill you", "murder", "gun", "shoot", "blood", "knife", "stab", 
    "explode", "rape", "attack", "abuse", "torture", "slaughter", "slit my wrists", "overdose", 
    "self harm", "hurt myself", "decapitate", "behead", "explode", "sniper", "violence", "war", "bloodshed",

    # Ableism, Discriminatory Terms, and Insults
    "retard", "cripple", "faggot", "dyke", "tranny", "spastic", "gimp", "moron", "idiot", "dumb", 
    "stupid", "imbecile", "imbecilic", "simpleton", "mongo", "idiotic", "retarded", "lunatic", 
    "psycho", "schizo", "bipolar", "autistic", "autism", "hysteric", "mentally ill", "psychiatric", 

    # Drug-Related Terms and Substance Abuse
    "weed", "cocaine", "heroin", "meth", "ecstasy", "lsd", "shrooms", "ketamine", "overdose", 
    "marijuana", "opiate", "crack", "pill popper", "junkie", "high", "stoned", "blunt", "crackhead",
    "addiction", "substance abuse", "snort", "dab", "trip", "needle", "suboxone", "poppers"

    # Suicide and Self-Harm Related Content
    "cut myself", "end my life", "overdose", "slit my wrists", "i want to die", "kill myself", "kms",
    "suicidal", "suicide pact", "suicide hotline", "self injury", "self-harm", "overdose", "end it all",
    "i'm done", "feeling empty", "kill me", "ending my life",

    # Spam, Scams, and Fraudulent Content
    "free money", "click here", "earn cash", "work from home", "make millions", "hot singles", 
    "win a prize", "unsecured loan", "credit repair", "pyramid scheme", "get rich quick", 
    "sign up now", "invest now", "bitcoin", "free gift card", "earn money fast", "no upfront fee",
    "referral link", "clickbait", "giveaway", "job offer", "lottery winner", "prize",

    # Hateful Speech and Discrimination
    "racist", "xenophobe", "homophobe", "sexist", "misogynist", "bigot", "transphobic", "antisemitic", 
    "homo", "fag", "colored", "minority", "gypsy", "redneck", "illegal immigrant", "slur", 
    "nazi", "white supremacist", "KKK", "N-word", "cracker", "white trash", "wetback", "sand nigger", 
    "cholo", "beaner", "terrorist", "bitch", "jew", "kike", "kuffar", "chink", "gook",

    # Harmful or Inflammatory Phrases
    "shut up", "fuck off", "piss off", "get lost", "drop dead", "go to hell", "suck my dick", "shut your mouth",
    "eat shit", "go away", "off yourself", "you're useless", "no one cares", "nobody loves you", 
    "you're pathetic", "you're a waste of space", "no one will miss you", "go kill yourself", 
    "you'll never amount to anything", "end it already",

    # Inappropriate or Offensive Jokes, Memes, and Humor
    "yo mama", "your mom", "retarded joke", "cripple joke", "gay joke", "racist joke",
    "homophobic joke", "sexist joke", "offensive humor", "insensitive humor",
    "shock value", "inappropriate joke", "distasteful joke", "derogatory humor", "disrespectful",

    # Offensive Terms and Slang (for any additional slurs, hate speech, or insults)
    "bastard", "slut", "whore", "bimbo", "bastard", "asswipe", "shithead", "dickhead", "suck",
    "douchebag", "cockface", "cumdumpster", "fistfucker", "slutbag", "faggotbag", "pussyass", 
    "doucheass", "cockass", "assholeface", "twatwaffle", "assclown", "numbnuts", "dicktard", 
    "assmunch", "shitstain", "cockknocker", "motherfucker",

    # Malicious Content (cyberbullying, harmful advice, etc.)
    "bitchslap", "kill himself", "kill herself", "kill themself", "slay yourself", "cut deep", "hang yourself",
    "self destruct", "self loathe", "destroy yourself", "cyberbully", "send nudes", "fuck you", "die in a hole", 
    "go die", "get lost", "no one cares", "your life is worthless", "empty shell", "kill me now",
    "suck my balls", "eat my ass", "go suck a dick", "die already", "shut the hell up",

    # Offensive Religious Terms (e.g., insults against religion, blasphemy, etc.)
    "goddamn", "jesus christ", "holy shit", "christ on a cracker", "fucking hell", "god is dead", 
    "blasphemy", "atheism", "hellfire", "burn in hell", "damnation", "satanist", "devil worshipper",
    "god hate", "jesus freak", "holy fuck"
]

# Mapping from university keys to their website URLs
UNIVERSITY_WEBSITES = {
    "aberdeen": "https://www.abdn.ac.uk/",
    "abertay": "https://www.abertay.ac.uk/",
    "caledonian": "https://www.gcu.ac.uk/",
    "dundee": "https://www.dundee.ac.uk/",
    "edinburgh": "https://www.ed.ac.uk/",
    "glasgow": "https://www.gla.ac.uk/",
    "heriot_watt": "https://www.hw.ac.uk/",
    "napier": "https://www.napier.ac.uk/",
    "queen_margaret": "https://www.qmu.ac.uk/",
    "robert_gordon": "https://www.rgu.ac.uk/",
    "st_andrews": "https://www.st-andrews.ac.uk/",
    "stirling": "https://www.stir.ac.uk/",
    "strathclyde": "https://www.strath.ac.uk/",
    "uws": "https://www.uws.ac.uk/",
    "uhi": "https://www.uhi.ac.uk/",
    "queens": "https://www.qub.ac.uk/",
    "ulster": "https://www.ulster.ac.uk/",
    "aberystwyth": "https://www.aber.ac.uk/",
    "bangor": "https://www.bangor.ac.uk/",
    "cardiff": "https://www.cardiff.ac.uk/",
    "cardiff_met": "https://www.cardiffmet.ac.uk/",
    "usw": "https://www.southwales.ac.uk/",
    "swansea": "https://www.swansea.ac.uk/",
    "tsd": "https://www.uwtsd.ac.uk/",
    "wrexham": "https://www.wrexham.ac.uk/",
    "oxford": "https://www.ox.ac.uk/",
    "cambridge": "https://www.cam.ac.uk/",
    "imperial": "https://www.imperial.ac.uk/",
    "ucl": "https://www.ucl.ac.uk/",
    "kcl": "https://www.kcl.ac.uk/",
    "lse": "https://www.lse.ac.uk/",
    "harvard": "https://www.harvard.edu/",
    "mit": "https://www.mit.edu/",
    "stanford": "https://www.stanford.edu/",
    "berkeley": "https://www.berkeley.edu/",
}

# ---------------------------
# Cookie and Session Helpers
# ---------------------------

def get_server_side_cookie(request, cookie, default_val=None):
    # Retrieve a cookie value from the session, or return the default if not set
    val = request.session.get(cookie)
    
    if not val:
    
        val = default_val
    
    return val

def visitor_cookie_handler(request):
    # Manage the 'visits' and 'last_visit' cookies stored in the session
    # Increments the visit count if a new day has started
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now())) 
    
    last_visit_time = datetime.strptime(last_visit_cookie, '%Y-%m-%d %H:%M:%S.%f')  

    # If more than a day has passed, increment the visits count
    if (datetime.now() - last_visit_time).days > 0:
        
        visits += 1
        
        request.session['last_visit'] = str(datetime.now())  
    
    else:
    
        request.session['last_visit'] = last_visit_cookie
    
    request.session['visits'] = visits

# ----------------
# Main App Views
#-----------------

class IndexView(View):
    """
    Display the home page with the top categories, articles, comments, threads, and
    any university-specific content for logged-in users.
    """
    def get(self, request):

        context_dict = {}
        # Finding the top 5 categories, articles by points, comments and threads (ordered by recent updates)
        category_list = Category.objects.order_by('-views')[:5]

        context_dict['categories'] = category_list

        article_list = Article.objects.order_by('-points')[:5]

        context_dict['articles'] = article_list
        
        comments = Comment.objects.order_by('-edited_on', '-written_on')[:5]

        context_dict['comments'] = comments

        threads = Thread.objects.annotate(post_count=Count('post')).order_by('-updated_on', '-started_on')[:5]
        
        context_dict['threads'] = threads

        university_articles = []
        
        university_threads = []

        university_website = None

        # Filter university-related content for authenticated users with  a university set
        if request.user.is_authenticated and request.user.userprofile.university:
        
            user_university = request.user.userprofile.university
        
            university_articles = Article.objects.filter(related_university=user_university).order_by('-updated_on', '-created_on')[:3]
        
            university_threads = Thread.objects.annotate(post_count=Count('post')).filter(related_university=user_university).order_by('-updated_on', '-started_on')[:3]

            university_website = UNIVERSITY_WEBSITES.get(user_university)

        context_dict['university_articles'] = university_articles
        
        context_dict['university_threads'] = university_threads

        # Boolean flag to indicate if the user has a university set
        context_dict['user_has_university'] = bool(request.user.is_authenticated and request.user.userprofile.university)
        
        context_dict['university_website'] = university_website

        # Update session cookies related to visits
        visitor_cookie_handler(request)

        return render(request, 'main/index.html', context_dict)

class AboutView(View):
    """
    Display the About page with team member profiles
    """
    def get(self, request):
        # Prepare context with team member profiles for the About page
        context_dict = {}

        team_members = [
            ('aaronhxx_1', 'founder_profile'),
            ('phoebe6504', 'developer_profile'),
            ('euan_galloway', 'marketing_profile'),
            ('urangoo123', 'system_profile'),
        ]

        profiles = []

        for username, key in team_members:

            profile = UserProfile.objects.filter(user__username=username).first()

            if profile:

                profiles.append(profile)

        context_dict['team_members'] = profiles

        visitor_cookie_handler(request)

        context_dict['visits'] = request.session.get('visits', 0)

        return render(request, 'main/about.html', context_dict)

class PrivacyView(View):
    # Render the Privacy Policy Page
    def get(self, request):

        return render(request, 'main/privacy.html')
    
class TermsView(View):  
    # Render the Terms and Conditions page
    def get(self, request):

        return render(request, 'main/terms.html')
    
class MissionVisionView(View):
    # Render the Mission and Vision page
    def get(self, request):

        return render(request, 'main/mission_vision.html')

class ContactView(View):
    """
    Display and process the Contact form
    GET: Render the contact form
    POST: Process the form, send an email, and display success or error messages
    """
    def get(self, request):
        
        return render(request, 'main/contact.html')

    def post(self, request):
        # Process contact form submission and send an email
        name = request.POST.get('name')

        email = request.POST.get('email')

        message = request.POST.get('message')

        subject = f"New message from {name}"

        message_body = f"Message from: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:

            send_mail(
                subject,
                message_body,
                email,
                [settings.CONTACT_EMAIL],
                fail_silently=False
            )

            messages.success(request, "Your message has been sent successfully!")

        except Exception as e:

            messages.error(request, f"Something went wrong. Please try again later. Error: {e}", extra_tags="danger")

        return render(request, 'main/contact.html', {
            'name': name,
            'email': email,
            'message': message
        })

class ValuesView(View):
    # Render the Values page
    def get(self, request):

        return render(request, 'main/values.html')

class FAQsView(View):
    # Render the FAQs page
    def get(self, request):

        return render(request, 'main/faqs.html')

class StatsView(View):
    """
    Display various statistics (for staff only)
    Statistics include counts of categories, articles, comments, users, forums, threads, posts
    as well as aggregated points, views and likes
    """

    @method_decorator(login_required)
    def get(self, request):
        # Only allow staff to access statistics
        context_dict = {}
        
        if not request.user.is_staff:

            return redirect(reverse('main:index'))
        
        context_dict['total_categories'] = Category.objects.count()
        
        context_dict['total_articles'] = Article.objects.count()
        
        context_dict['total_comments'] = Comment.objects.count()
        
        context_dict['total_users'] = User.objects.count()
        
        context_dict['total_forums'] = Forum.objects.count()
        
        context_dict['total_threads'] = Thread.objects.count()
        
        context_dict['total_posts'] = Post.objects.count()

        total_points = sum(article.points for article in Article.objects.all())
        
        total_views = sum(article.views for article in Article.objects.all())

        total_likes = sum(post.likes for post in Post.objects.all())

        context_dict['total_points'] = total_points
        
        context_dict['total_views'] = total_views

        context_dict['total_likes'] = total_likes

        # Prepare per-category and per-forum statistics
        category_stats = {}
        
        category_names, category_points, category_views = [], [], []

        for category in Category.objects.all():
        
            articles_sum = category.article_set.count()
        
            category_points_sum = sum(article.points for article in category.article_set.all())
        
            category_views_sum = sum(article.views for article in category.article_set.all())

            category_stats[category.name] = {
                'articles': articles_sum,
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

        forum_stats = {}

        forum_names = []

        for forum in Forum.objects.all():

            threads_sum = forum.thread_set.count()

            posts_sum = sum(thread.post_set.count() for thread in forum.thread_set.all())

            forum_stats[forum.name] = {
                'threads': threads_sum,
                'posts': posts_sum
            }

            forum_names.append(forum.name)
        
        context_dict['forum_stats'] = forum_stats
        
        context_dict['forum_names'] = forum_names

        return render(request, 'main/stats.html', context_dict)

class RegisterProfileView(View):

    """
    Allow logged-in users to register or update their user profile
    GET: Render the profile registration form
    POST: Process the form and save the profile
    """

    @method_decorator(login_required)
    def get(self, request):

        form = UserProfileForm()

        context_dict = {'form': form}

        return render(request, 'main/profile_registration.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request):

        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():

            userprofile = form.save(commit=False)

            userprofile.user = request.user

            userprofile.save()

            return redirect(reverse('main:index'))
        
        else:
        
            print(form.errors)
        
        context_dict = {'form': form}
        
        return render(request, 'main/profile_registration.html', context_dict)

class ProfileView(View):

    """
    Display the profile page of a given user
    Retrieves user details, articles, threads, and university information
    """

    def get_user_details(self, username):

        context_dict = {}
    
        try:
    
            user = User.objects.get(username=username)

            context_dict['selected_user'] = user
    
        except User.DoesNotExist:

            context_dict['selected_user'] = None

            return context_dict
        
        userprofile = UserProfile.objects.get_or_create(user=user)[0]

        context_dict['userprofile'] = userprofile

        articles = Article.objects.filter(author=user).select_related("category").order_by('created_on')

        context_dict['articles'] = articles

        threads = Thread.objects.filter(author=user).select_related("forum").order_by('started_on')

        context_dict['threads'] = threads

        university_website = None

        if user.is_authenticated and user.userprofile.university:
        
            user_university = user.userprofile.university
            
            university_website = UNIVERSITY_WEBSITES.get(user_university)
        
        user_has_university = bool(user.is_authenticated and user.userprofile.university)

        context_dict['user_has_university'] = user_has_university

        context_dict['university_website'] = university_website
        
        return context_dict
    
    @method_decorator(login_required)
    def get(self, request, username):
        
        context_dict = self.get_user_details(username)
                
        return render(request, 'main/profile.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, username):

        context_dict = self.get_user_details(username)
                
        return render(request, 'main/profile.html', context_dict)

class EditProfileView(View):

    # Allow the logged-in user to edit their own profile

    def get_user_profile(self, user):

        user_profile, created = UserProfile.objects.get_or_create(user=user)

        return user_profile

    @method_decorator(login_required)
    def get(self, request):

        user_profile = self.get_user_profile(request.user)

        form = UserProfileForm(instance=user_profile)

        return render(request, 'main/edit_profile.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):

        user_profile = self.get_user_profile(request.user)

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():

            form.save()

            return redirect(reverse('main:profile', kwargs={'username': request.user.username}))  

        return render(request, 'main/edit_profile.html', {'form': form})

class ListUsersView(View):

    """
    List all user profiles with optional filtering by username or university.
    Supports AJAX requests for dynamic loading of user profiles.
    """
    @method_decorator(login_required)
    def get(self, request):

        profiles = UserProfile.objects.all()

        university_keys = UserProfile.objects.exclude(university__isnull=True).exclude(university="").values_list('university', flat=True).distinct()

        university_dict = dict(UNIVERSITY_CHOICES)

        universities = [(key, university_dict.get(key, key)) for key in university_keys]

        search_query = request.GET.get('search', '').strip().lower()
        
        university_filter = request.GET.get('university', '').strip()

        if search_query:
        
            profiles = profiles.filter(user__username__icontains=search_query)

        if university_filter:
        
            profiles = profiles.filter(university=university_filter)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

            profiles_html = render_to_string('main/profiles.html', {'profiles': profiles, 'MEDIA_URL': settings.MEDIA_URL})
            
            return JsonResponse({'profiles_html': profiles_html})

        return render(request, 'main/list_users.html', {'profiles': profiles, 'universities': universities})

class DeleteAccountConfirmationView(View):
    """
    Render a confirmation page for users who wish to delete their account.
    """
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
  
        return render(request, 'main/confirm_delete_account.html')

class DeleteAccountView(View):

    """
    Process the deletion of the current user's account.
    Logs the user out and then deletes the account.
    """

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
  
        user = request.user
  
        logout(request)
  
        user.delete()
  
        messages.success(request, "Your account has been successfully deleted.")
  
        return redirect('main:index')

class CategoryListView(View):

    """
    Display a list of all categories.
    """

    def get(self, request):

        context_dict = {}

        categories = Category.objects.all()
        
        context_dict['categories'] = categories

        return render(request, 'main/category_list.html', context_dict)

class ShowCategoryView(View):

    """
    Display a single category along with its associated articles.
    Increments the view count for the category.
    """

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

        return render(request, 'main/category.html', context_dict)

class AddCategoryView(View):

    """
    Allow staff to add a new category.
    """

    @method_decorator(login_required)
    def get(self, request):
        
        if not request.user.is_staff:

            return redirect(reverse('main:index'))

        form = CategoryForm()

        return render(request, 'main/add_category.html', {'form': form})
    
    @method_decorator(login_required)
    def post(self, request):
        
        if not request.user.is_staff:

            return redirect(reverse('main:index'))

        form = CategoryForm(request.POST)

        if form.is_valid():

            form.save(commit=True)

            return redirect(reverse('main:index'))
        
        else:

            print(form.errors)
        
        return render(request, 'main/add_category.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class EditCategoryView(View):

    """
    Allows staff users to edit an existing category.
    Retrieves the category by its slug, populates a form for editing,
    and saves changes if the form is valid.
    """

    def get_category(self, category_name_slug):

        try:

            return Category.objects.get(slug=category_name_slug)
        
        except Category.DoesNotExist:

            return None

    def create_context_dict(self, category):
        # Prepare the context with the current category and pre-populated form.
        return {'category': category, 'form': CategoryForm(instance=category)}

    def get(self, request, category_name_slug):
        
        if not request.user.is_staff:

            return redirect('main:show_category', category_name_slug=category_name_slug)

        category = self.get_category(category_name_slug)

        context_dict = self.create_context_dict(category)
        
        return render(request, 'main/edit_category.html', context_dict)

    def post(self, request, category_name_slug):

        if not request.user.is_staff:

            return redirect('main:show_category', category_name_slug=category_name_slug)

        category = self.get_category(category_name_slug)

        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():

            updated_category = form.save()
            
            return redirect('main:show_category', category_name_slug=updated_category.slug)

        context_dict = self.create_context_dict(category)
        
        context_dict['form'] = form  
        
        return render(request, 'main/edit_category.html', context_dict)

@method_decorator(login_required, name='dispatch')
class DeleteCategoryView(View):

    """
    Allow staff users to delete a category.
    Displays a confirmation page and, upon confirmation, deletes the category.
    """

    def get_category(self, category_name_slug):
        
        try:
        
            return Category.objects.get(slug=category_name_slug)
        
        except Category.DoesNotExist:
        
            return None

    def get(self, request, category_name_slug):

        if not request.user.is_staff:

            return redirect('main:show_category', category_name_slug=category_name_slug)
        
        category = self.get_category(category_name_slug)

        if category is None:
        
            return render(request, 'main/delete_category.html', {'category': None})

        return render(request, 'main/delete_category.html', {'category': category})

    def post(self, request, category_name_slug):

        if not request.user.is_staff:

            return redirect('main:show_category', category_name_slug=category_name_slug)
        
        category = self.get_category(category_name_slug)

        if category is None:
        
            return render(request, 'main/delete_category.html', {'category': None})
        
        category.delete()

        return redirect('main:category_list')

class LikeCategoryView(View):

    """
    Increase the 'points' for a category via an AJAX GET request.
    """

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

    """
    Decrease the 'point' for a category via an AJAX GET request.
    """
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

class ShowArticleView(View):

    """
    Display a single article along with its comments.
    Increments the article's view count and prepares a comment form.
    """

    def create_context_dict(self, category_name_slug, article_title_slug):

        context_dict = {}

        try:

            category = Category.objects.get(slug=category_name_slug)
            
            context_dict['category'] = category

            article = Article.objects.get(slug=article_title_slug)
            
            context_dict['article'] = article
            # Increment view count for the article
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
        # Add an empty comment form to the context
        context_dict['form'] = CommentForm()
        
        return render(request, 'main/article.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, category_name_slug, article_title_slug):
        
        context_dict = self.create_context_dict(category_name_slug, article_title_slug)

        form = CommentForm(request.POST)
        
        if form.is_valid():

            content = form.cleaned_data['content']
            # Check for banned words in the comment

            if any(word in content.lower() for word in BANNED_WORDS):

                storage = messages.get_messages(request)
                
                storage.used = True

                messages.error(request, "Your comment contains innappropriate content and was not submitted.", extra_tags="danger")
        
            else:

                comment = form.save(commit=False)
            
                comment.article = context_dict['article']
            
                comment.author = request.user
            
                comment.save()
                # Update the article's updated timestamp
                article = context_dict.get('article')

                if article:

                    article.updated_on = timezone.now()

                    article.save()

                messages.success(request, "Your comment has been submitted successfully.")
        
            return redirect('main:show_article', category_name_slug=category_name_slug, article_title_slug=article_title_slug)
        
        context_dict['form'] = form
        
        return render(request, 'main/article.html', context_dict)

class AddArticleView(View):

    """
    Allow a logged-in user to add a new article to a given category.
    Also supports an external search query for related content.
    """

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
        
        context_dict = {'form': form, 'category': category}

        query = request.GET.get('query', '').strip()
        
        if query:
        
            context_dict['query'] = query
        
            context_dict['result_list'] = run_query(query)

        return render(request, 'main/add_article.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, category_name_slug):
        
        form = ArticleForm(request.POST, request.FILES)
        
        category = self.get_category_name(category_name_slug)

        if form.is_valid():

            title = form.cleaned_data['title']

            summary = form.cleaned_data['summary']

            content = form.cleaned_data['content']

            #Check for banned words in title, summary, and content.
            if any(word in title.lower() for word in BANNED_WORDS):

                storage = messages.get_messages(request)

                storage.used = True

                messages.error(request, "The title of your article contains innappropriate content and was not submitted.", extra_tags="danger")

            elif any(word in summary.lower() for word in BANNED_WORDS):

                storage = messages.get_messages(request)

                storage.used = True

                messages.error(request, "The summary of your article contains innappropriate content and was not submitted.", extra_tags="danger")

            elif any(word in content.lower() for word in BANNED_WORDS):

                storage = messages.get_messages(request)
                
                storage.used = True

                messages.error(request, "The content of your article contains innappropriate content and was not submitted.", extra_tags="danger")
        
            else:
        
                article = form.save(commit=False)
            
                article.author = request.user
            
                article.category = category
            
                article.views = 0
            
                article.points = 0
            
                article.save()

                messages.success(request, "Your article has been submitted successfully.")
        
                return redirect('main:show_article', category_name_slug=category_name_slug, article_title_slug=article.slug)
        
        context_dict = {'form': form, 'category': category}

        query = request.POST.get('query', '').strip()
        
        if query:
        
            context_dict['query'] = query
        
            context_dict['result_list'] = run_query(query)

        return render(request, 'main/add_article.html', context_dict)

@method_decorator(login_required, name='dispatch')
class EditArticleView(View):

    """
    Allow an article's author to edit the article.
    Validates form data and checks for banned words before saving changes.
    """

    def get_category(self, category_name_slug):

        try:

            return Category.objects.get(slug=category_name_slug)
        
        except Category.DoesNotExist:

            return None

    def get_article(self, article_title_slug):
        
        try:
        
            return Article.objects.get(slug=article_title_slug)
        
        except Article.DoesNotExist:
        
            return None

    def create_context_dict(self, article):
        
        return {'article': article, 'form': ArticleForm(instance=article)}

    def get(self, request, category_name_slug, article_title_slug):

        category = self.get_category(category_name_slug)

        article = self.get_article(article_title_slug)

        if article is None:
            
            return render(request, 'main/edit_article.html', {'article': None})

        # Only allow author to edit the article.
        if request.user != article.author:

            return redirect('main:show_article', category_name_slug=category_name_slug, article_title_slug=article_title_slug)

        context_dict = self.create_context_dict(article)
        
        return render(request, 'main/edit_article.html', context_dict)

    def post(self, request, category_name_slug, article_title_slug):

        category = self.get_category(category_name_slug)

        article = self.get_article(article_title_slug)

        if article is None:
            
            return render(request, 'main/edit_article.html', {'article': None})

        if request.user != article.author:

            return redirect('main:show_article', category_name_slug=category_name_slug, article_title_slug=article_title_slug)

        form = ArticleForm(request.POST, request.FILES, instance=article)

        if form.is_valid():
            
            title = form.cleaned_data['title']

            summary = form.cleaned_data['summary']

            content = form.cleaned_data['content']

            #Validate that none of the fields contain banned words.
            if any(word in title.lower() for word in BANNED_WORDS):

                storage = messages.get_messages(request)

                storage.used = True

                messages.error(request, "The title of your article contains innappropriate content and was not edited.", extra_tags="danger")

            elif any(word in summary.lower() for word in BANNED_WORDS):

                storage = messages.get_messages(request)

                storage.used = True

                messages.error(request, "The summary of your article contains innappropriate content and was not edited.", extra_tags="danger")

            elif any(word in content.lower() for word in BANNED_WORDS):

                storage = messages.get_messages(request)
                
                storage.used = True

                messages.error(request, "The content of your article contains innappropriate content and was not edited.", extra_tags="danger")
        
            else:

                updated_article = form.save()
                
                messages.success(request, "Your article has been edited successfully.")
                
                return redirect('main:show_article', category_name_slug=category_name_slug, article_title_slug=updated_article.slug)

        context_dict = self.create_context_dict(article)
        
        context_dict['form'] = form  
        
        return render(request, 'main/edit_article.html', context_dict)

@method_decorator(login_required, name='dispatch')
class DeleteArticleView(View):

    """
    Allow an article's author to delete the article.
    Displays a confirmation page and deletes the article upon confirmation.
    """
    def get_article(self, category_name_slug, article_title_slug):
        
        try:
        
            return Article.objects.get(category__slug=category_name_slug, slug=article_title_slug)
        
        except Article.DoesNotExist:
        
            return None

    def get(self, request, category_name_slug, article_title_slug):
        
        article = self.get_article(category_name_slug, article_title_slug)

        if article is None:
        
            return render(request, 'main/delete_article.html', {'article': None})

        if request.user != article.author:
        
            return redirect('main:show_article', category_name_slug=category_name_slug, article_title_slug=article_title_slug)

        return render(request, 'main/delete_article.html', {'article': article})

    def post(self, request, category_name_slug, article_title_slug):
        
        article = self.get_article(category_name_slug, article_title_slug)

        if article is None or request.user != article.author:
        
            return redirect('main:show_article', category_name_slug=category_name_slug, article_title_slug=article_title_slug)

        category_slug = article.category.slug
        
        article.delete()

        return redirect('main:show_category', category_name_slug=category_slug)

@method_decorator(login_required, name='dispatch')
class EditCommentView(View):

    """
    Allow a comment's author to edit their comment within 24 hours of posting.
    Checks if the comment is still editable and validates for banned words.
    """

    def get_article(self, category_name_slug, article_title_slug):
        
        try:
        
            return Article.objects.get(category__slug=category_name_slug, slug=article_title_slug)
        
        except Article.DoesNotExist:
        
            return None

    def get_comment(self, comment_id):
        
        try:
        
            return Comment.objects.get(id=comment_id)
        
        except Comment.DoesNotExist:
        
            return None

    def is_editable(self, comment):
        # Allow editing if the comment is less than 24 hours old.
        return (timezone.now() - comment.written_on) < timedelta(hours=24)

    def create_context_dict(self, article, comment, can_edit):
        
        return {'article': article, 'comment': comment, 'can_edit': can_edit, 'form': CommentForm(instance=comment)}

    def get(self, request, category_name_slug, article_title_slug, comment_id):
        
        article = self.get_article(category_name_slug, article_title_slug)
        
        comment = self.get_comment(comment_id)

        can_edit = self.is_editable(comment)

        if article is None or comment is None:
        
            return render(request, 'main/edit_comment.html', {'comment': None})

        if request.user != comment.author:
        
            return redirect('main:show_article', category_name_slug=category_name_slug, article_title_slug=article_title_slug)

        context_dict = self.create_context_dict(article, comment, can_edit)
        
        return render(request, 'main/edit_comment.html', context_dict)

    def post(self, request, category_name_slug, article_title_slug, comment_id):
        
        article = self.get_article(category_name_slug, article_title_slug)
        
        comment = self.get_comment(comment_id)

        can_edit = self.is_editable(comment)

        if article is None or comment is None:
        
            return render(request, 'main/edit_comment.html', {'comment': None})

        if request.user != comment.author:
        
            return redirect('main:show_article', category_name_slug=category_name_slug, article_title_slug=article_title_slug)

        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():

            content = form.cleaned_data['content']
            # Check for banned words in the comment.
            if any(word in content.lower() for word in BANNED_WORDS):

                storage = messages.get_messages(request)
                
                storage.used = True

                messages.error(request, "Your comment contains innappropriate content and was not edited.", extra_tags="danger")
        
            else:

                form.save()

                article.updated_on = timezone.now()

                article.save()

                messages.success(request, "Your comment has been edited successfully.")
        
                return redirect('main:show_article', category_name_slug=category_name_slug, article_title_slug=article_title_slug)

        context_dict = self.create_context_dict(article, comment, can_edit)

        context_dict['form'] = form

        return render(request, 'main/edit_comment.html', context_dict)

@method_decorator(login_required, name='dispatch')
class DeleteCommentView(View):

    """
    Allow a comment's author to delete their comment within 24 hours of posting.
    Displays a confirmation page before deletion
    """

    def get_article(self, category_name_slug, article_title_slug):
        
        try:
        
            return Article.objects.get(category__slug=category_name_slug, slug=article_title_slug)
        
        except Article.DoesNotExist:
        
            return None

    def get_comment(self, comment_id):
        
        try:
        
            return Comment.objects.get(id=comment_id)
        
        except Comment.DoesNotExist:
        
            return None

    def is_deletable(self, comment):
        # Allow deletion if the comment is less than 24 hours old.
        return (timezone.now() - comment.written_on) < timedelta(hours=24)

    def create_context_dict(self, article, comment, can_delete):

        return {'article': article, 'comment': comment, 'can_delete': can_delete}

    def get(self, request, category_name_slug, article_title_slug, comment_id):
        
        article = self.get_article(category_name_slug, article_title_slug)

        comment = self.get_comment(comment_id)

        can_delete = self.is_deletable(comment)

        if article is None or comment is None:
        
            return render(request, 'main/delete_comment.html', {'comment': None})

        if request.user != comment.author:
        
            return redirect('main:show_article', category_name_slug=category_name_slug, article_title_slug=article_title_slug)

        context_dict = self.create_context_dict(article, comment, can_delete)

        return render(request, 'main/delete_comment.html', context_dict)

    def post(self, request, category_name_slug, article_title_slug, comment_id):
        
        article = self.get_article(category_name_slug, article_title_slug)

        comment = self.get_comment(comment_id)

        if article is None or comment is None:

            return render(request, 'main/delete_comment.html', {'comment': None})
        
        if request.user != comment.author:
        
            return redirect('main:show_article', category_name_slug=category_name_slug, article_title_slug=article_title_slug)

        article_slug = article.slug
        
        comment.delete()

        article.updated_on = timezone.now()

        article.save()

        return redirect('main:show_article', category_name_slug=category_name_slug, article_title_slug=article_slug)

class LikeArticleView(View):
    """
    Increase the points of an article via an AJAX GET request.
    """

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

    """
    Decrease the points of an article via an AJAX GET request.
    """

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
def favourite_article(request, article_title_slug):

    """
    Toggle the favourite status of an article for the current user.
    If the article is already favourited, it is removed; otherwise, it is added.
    """

    article = get_object_or_404(Article, slug=article_title_slug)
    
    userprofile = request.user.userprofile

    if article in userprofile.favourite_articles.all():
    
        userprofile.favourite_articles.remove(article)
    
    else:
    
        userprofile.favourite_articles.add(article)

    return redirect('main:show_article', category_name_slug=article.category.slug, article_title_slug=article.slug)

class ForumListView(View):

    """
    Display a list of all forums.
    """

    def get(self, request):

        context_dict = {}

        forums = Forum.objects.all()
        
        context_dict['forums'] = forums

        return render(request, 'main/forum_list.html', context_dict)
    
class AddForumView(View):

    """
    Allow staff users to add a new forum
    """

    @method_decorator(login_required)
    def get(self, request):
        
        if not request.user.is_staff:

            return redirect(reverse('main:index'))

        form = ForumForm()

        return render(request, 'main/add_forum.html', {'form': form})
    
    @method_decorator(login_required)
    def post(self, request):
        
        if not request.user.is_staff:

            return redirect(reverse('main:index'))

        form = ForumForm(request.POST)

        if form.is_valid():

            form.save(commit=True)

            return redirect(reverse('main:index'))
        
        else:

            print(form.errors)
        
        return render(request, 'main/add_forum.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class EditForumView(View):

    """
    Allow staff users to edit an existing forum.
    """

    def get_forum(self, forum_name_slug):

        try:

            return Forum.objects.get(slug=forum_name_slug)
        
        except Forum.DoesNotExist:

            return None

    def create_context_dict(self, forum):
        
        return {'forum': forum, 'form': ForumForm(instance=forum)}

    def get(self, request, forum_name_slug):
        
        if not request.user.is_staff:

            return redirect('main:thread_list', forum_name_slug)

        forum = self.get_forum(forum_name_slug)

        context_dict = self.create_context_dict(forum)
        
        return render(request, 'main/edit_forum.html', context_dict)

    def post(self, request, forum_name_slug):

        if not request.user.is_staff:

            return redirect('main:thread_list', forum_name_slug)

        forum = self.get_forum(forum_name_slug)

        form = ForumForm(request.POST, instance=forum)

        if form.is_valid():

            updated_forum = form.save()
            
            return redirect('main:thread_list', forum_name_slug=updated_forum.slug)

        context_dict = self.create_context_dict(forum)
        
        context_dict['form'] = form  
        
        return render(request, 'main/edit_forum.html', context_dict)

@method_decorator(login_required, name='dispatch')
class DeleteForumView(View):

    """
    Allow staff users to delete an existing forum.
    """

    def get_forum(self, forum_name_slug):
        
        try:
        
            return Forum.objects.get(slug=forum_name_slug)
        
        except Forum.DoesNotExist:
        
            return None

    def get(self, request, forum_name_slug):

        if not request.user.is_staff:

            return redirect('main:thread_list', forum_name_slug=forum_name_slug)
        
        forum = self.get_forum(forum_name_slug)

        if forum is None:
        
            return render(request, 'main/delete_forum.html', {'forum': None})

        return render(request, 'main/delete_forum.html', {'forum': forum})

    def post(self, request, forum_name_slug):

        if not request.user.is_staff:

            return redirect('main:thread_list', forum_name_slug=forum_name_slug)
        
        forum = self.get_forum(forum_name_slug)

        if forum is None:
        
            return render(request, 'main/delete_forum.html', {'forum': None})
        
        forum.delete()

        return redirect('main:forum_list')

class ThreadListView(View):

    """
    Display a list of threads for a given forum.
    """

    def create_context_dict(self, forum_name_slug):
        
        context_dict = {}

        try:

            forum = Forum.objects.get(slug=forum_name_slug)

            threads = Thread.objects.filter(forum=forum)

            context_dict['threads'] = threads

            context_dict['forum'] = forum

        except Forum.DoesNotExist:

            context_dict['threads'] = None

            context_dict['forum'] = None

        return context_dict

    def get(self, request, forum_name_slug):

        context_dict = self.create_context_dict(forum_name_slug)

        return render(request, 'main/thread_list.html', context_dict)

@method_decorator(login_required, name='dispatch')
class ThreadDetailView(View):

    """
    Display the details of a thread, including its posts and any attached poll.
    Also provides a form for adding new posts and, if applicable, shows poll options.
    """

    def create_context_dict(self, forum_name_slug, thread_title_slug):

        context_dict = {}

        try:

            forum = Forum.objects.get(slug=forum_name_slug)

            context_dict['forum'] = forum

            thread = Thread.objects.get(slug=thread_title_slug, forum=forum)

            context_dict['thread'] = thread

            posts = Post.objects.filter(thread=thread).order_by('written_on')

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
        # Flag to indicate if the thread was not found.
        if context_dict['thread'] is None:

            context_dict['thread_not_found'] = True

        else:

            context_dict['thread_not_found'] = False

        form = PostForm()

        context_dict['form'] = form

        query = request.GET.get('query', '').strip()

        if query:

            context_dict['query'] = query

            context_dict['result_list'] = run_query(query)

        poll = context_dict.get('poll')

        if poll:

            poll_options = poll.options.all()

            context_dict['poll_options'] = poll_options

        return render(request, "main/thread_detail.html", context_dict)

    def post(self, request, forum_name_slug, thread_title_slug):
        
        context_dict = self.create_context_dict(forum_name_slug, thread_title_slug)

        form = PostForm(request.POST)

        query = request.POST.get('query', '').strip()

        if query:

            context_dict['query'] = query

            context_dict['result_list'] = run_query(query)

        if form.is_valid():

            content = form.cleaned_data['content']
            # Check for banned words in the post content.
            if any(word in content.lower() for word in BANNED_WORDS):

                storage = messages.get_messages(request)
                
                storage.used = True

                messages.error(request, "Your post contains innappropriate content and was not submitted.", extra_tags="danger")
        
            else:

                post = form.save(commit=False)

                post.thread = context_dict.get('thread')

                post.author = request.user

                post.save()

                thread = context_dict.get('thread')

                if thread:

                    thread.updated_on = timezone.now()

                    thread.save()

                messages.success(request, "Your post has been submitted successfully.")

                return redirect("main:thread_detail", forum_name_slug=context_dict['forum'].slug, thread_title_slug=thread.slug)

        context_dict['form'] = form

        return render(request, "main/thread_detail.html", context_dict)

class CreateThreadView(View):

    """
    Allow a logged-in user to create a new thread in a given forum.
    Supports an external query search to help generate thread content.
    """

    def get_forum_name(self, forum_name_slug):

        try:

            forum = Forum.objects.get(slug=forum_name_slug)

        except Forum.DoesNotExist:

            forum = None

        return forum

    @method_decorator(login_required)
    def get(self, request, forum_name_slug):

        forum = self.get_forum_name(forum_name_slug)

        form = ThreadForm()

        context_dict = {'form': form, 'forum': forum}

        query = request.GET.get('query', '').strip()

        if query:

            context_dict['query'] = query

            context_dict['result_list'] = run_query(query)

        return render(request, 'main/create_thread.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, forum_name_slug):

        forum = self.get_forum_name(forum_name_slug)

        form = ThreadForm(request.POST)

        context_dict = {'form': form, 'forum': forum}

        query = request.POST.get('query', '').strip()

        if query:

            context_dict['query'] = query

            context_dict['result_list'] = run_query(query)

        if form.is_valid():

            title = form.cleaned_data['title']

            topic = form.cleaned_data['topic']
            # Validate that title and topic do not contain banned words.
            if any(word in title.lower() for word in BANNED_WORDS):

                storage = messages.get_messages(request)

                storage.used = True

                messages.error(request, "The title of your thread contains innappropriate content and was not submitted.", extra_tags="danger")

            elif any(word in topic.lower() for word in BANNED_WORDS):

                storage = messages.get_messages(request)

                storage.used = True

                messages.error(request, "The topic of your thread contains innappropriate content and was not submitted.", extra_tags="danger")

            else:

                thread = form.save(commit=False)

                thread.author = request.user

                thread.forum = forum

                thread.save()

                messages.success(request, "Your thread has been submitted successfully.")

                return redirect('main:thread_detail', forum_name_slug=forum_name_slug, thread_title_slug=thread.slug)

        return render(request, 'main/create_thread.html', context_dict)

@method_decorator(login_required, name='dispatch')
class EditThreadView(View):

    """
    Allow the author of a thread to edit it.
    Validates that the current user is the author and checks for banned words.
    """

    def get_forum(self, forum_name_slug):

        try:

            return Forum.objects.get(slug=forum_name_slug)
        
        except Forum.DoesNotExist:

            return None

    def get_thread(self, thread_title_slug):
        
        try:
        
            return Thread.objects.get(slug=thread_title_slug)
        
        except Thread.DoesNotExist:
        
            return None

    def create_context_dict(self, thread):
        
        return {'thread': thread, 'form': ThreadForm(instance=thread)}

    def get(self, request, forum_name_slug, thread_title_slug):

        forum = self.get_forum(forum_name_slug)

        thread = self.get_thread(thread_title_slug)

        if thread is None:

            return render(request, 'main/edit_thread.html', {'thread': None})

        if request.user != thread.author:

            return redirect('main:thread_detail', forum_name_slug=forum_name_slug, thread_title_slug=thread_title_slug)

        context_dict = self.create_context_dict(thread)
        
        return render(request, 'main/edit_thread.html', context_dict)

    def post(self, request, forum_name_slug, thread_title_slug):

        forum = self.get_forum(forum_name_slug)

        thread = self.get_thread(thread_title_slug)

        if thread is None:

            return render(request, 'main/edit_thread.html', {'thread': None})

        if request.user != thread.author:

            return redirect('main:thread_detail', forum_name_slug=forum_name_slug, thread_title_slug=thread_title_slug)

        form = ThreadForm(request.POST, instance=thread)

        if form.is_valid():
            
            title = form.cleaned_data['title']

            topic = form.cleaned_data['topic']

            # Check for banned words in title and topic
            if any(word in title.lower() for word in BANNED_WORDS):

                storage = messages.get_messages(request)

                storage.used = True

                messages.error(request, "The title of your thread contains innappropriate content and was not edited.", extra_tags="danger")

            elif any(word in topic.lower() for word in BANNED_WORDS):

                storage = messages.get_messages(request)

                storage.used = True

                messages.error(request, "The topic of your thread contains innappropriate content and was not edited.", extra_tags="danger")

            else:

                updated_thread = form.save()

                messages.success(request, "Your thread has been edited successfully.")
                
                return redirect('main:thread_detail', forum_name_slug=forum_name_slug, thread_title_slug=updated_thread.slug)

        context_dict = self.create_context_dict(thread)
        
        context_dict['form'] = form  
        
        return render(request, 'main/edit_thread.html', context_dict)

@method_decorator(login_required, name='dispatch')
class DeleteThreadView(View):

    """
    Allow the author of a thread to delete it.
    Displays a confirmation page and deletes the thread if confirmed.
    """

    def get_thread(self, forum_name_slug, thread_title_slug):
        
        try:
        
            return Thread.objects.get(forum__slug=forum_name_slug, slug=thread_title_slug)
        
        except Thread.DoesNotExist:
        
            return None

    def get(self, request, forum_name_slug, thread_title_slug):
        
        thread = self.get_thread(forum_name_slug, thread_title_slug)
        
        if thread is None:
        
            return render(request, 'main/delete_thread.html', {'thread': None})

        if request.user != thread.author:
        
            return redirect('main:thread_detail', forum_name_slug=forum_name_slug, thread_title_slug=thread_title_slug)

        return render(request, 'main/delete_thread.html', {'thread': thread})

    def post(self, request, forum_name_slug, thread_title_slug):
        
        thread = self.get_thread(forum_name_slug, thread_title_slug)

        if thread is None or request.user != thread.author:
        
            return redirect('main:show_thread', forum_name_slug=forum_name_slug, thread_title_slug=thread_title_slug)

        forum_slug = thread.forum.slug
        
        thread.delete()

        return redirect('main:thread_list', forum_name_slug=forum_slug)

@method_decorator(login_required, name='dispatch')
class EditPostView(View):

    """
    Allow the author of a post to edit it within 24 hours.
    Checks that the post is editable, validates changes, and checks for banned words.
    """

    def get_thread(self, forum_name_slug, thread_title_slug):
        
        try:
        
            return Thread.objects.get(forum__slug=forum_name_slug, slug=thread_title_slug)
        
        except Thread.DoesNotExist:
        
            return None

    def get_post(self, post_id):
        
        try:
        
            return Post.objects.get(id=post_id)
        
        except Post.DoesNotExist:
        
            return None

    def is_editable(self, post):
        # A post is editable if it was written within the last 24 hours.
        return (timezone.now() - post.written_on) < timedelta(hours=24)

    def create_context_dict(self, thread, post, can_edit):
        
        return {'thread': thread, 'post': post, 'can_edit': can_edit, 'form': PostForm(instance=post)}

    def get(self, request, forum_name_slug, thread_title_slug, post_id):

        # Handle GET requests to display the edit post form. Retrieves thread and post objects

        #Retrieve the thread and post based on URL slugs and post_id
        thread = self.get_thread(forum_name_slug, thread_title_slug)

        post = self.get_post(post_id)

        # Determine if the post is editable
        can_edit = self.is_editable(post)

        if thread is None or post is None:
        
            return render(request, 'main/edit_post.html', {'post': None})

        # Ensure that only the author can edit the post
        if request.user != post.author:
        
            return redirect('main:thread_detail', forum_name_slug=forum_name_slug, thread_title_slug=thread_title_slug)

        # Build the context with the thread, post, edit flag, and the pre-populated form
        context_dict = self.create_context_dict(thread, post, can_edit)
        
        return render(request, 'main/edit_post.html', context_dict)

    def post(self, request, forum_name_slug, thread_title_slug, post_id):

        #Handle POST requests to process the edited post submission

        # Retrieve the thread and post objects
        thread = self.get_thread(forum_name_slug, thread_title_slug)
        
        post = self.get_post(post_id)

        # Determine if the post is still editable
        can_edit = self.is_editable(post)

        # OIf the thread or post doesn't exist, render the template with 'post': None.
        if thread is None or post is None:
        
            return render(request, 'main/edit_post.html', {'post': None})

        # Only allow the post's author to edit the post
        if request.user != post.author:
        
            return redirect('main:thread_detail', forum_name_slug=forum_name_slug, thread_title_slug=thread_title_slug)

        # Create a form instance with the submitted POST data, pre-populated with the existing post
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            # Extract the updated content from the form
            content = form.cleaned_data['content']

            # Check if the updated content contains any banned words
            if any(word in content.lower() for word in BANNED_WORDS):

                storage = messages.get_messages(request)
                
                storage.used = True # Mark messages as used so they don't duplicate

                messages.error(request, "Your post contains inappropriate content and was not edited.", extra_tags="danger")
        
            else:
                # Save the updated post and update the thread's 'updated_on' timestamp
                form.save()

                thread.updated_on = timezone.now()

                thread.save()

                messages.success(request, "Your post has been edited successfully.")

                return redirect("main:thread_detail", forum_name_slug=forum_name_slug, thread_title_slug=thread_title_slug)

        # If the form is invalid  or there was an error, rebuild the context and re-render the form
        context_dict = self.create_context_dict(thread, post, can_edit)

        context_dict['form'] = form

        return render(request, 'main/edit_post.html', context_dict)

@method_decorator(login_required, name='dispatch')
class DeletePostView(View):

    """
    Allow the author of a post to delete it if it was written within 24 hrs.
    Displays a confirmation page and deletes the post upon confirmation.
    """

    def get_thread(self, forum_name_slug, thread_title_slug):
        # Retrieve the thread based on forum and thread slugs
        try:
        
            return Thread.objects.get(forum__slug=forum_name_slug, slug=thread_title_slug)
        
        except Thread.DoesNotExist:
        
            return None

    def get_post(self, post_id):
        # Retrieve the post by its primary key
        try:
        
            return Post.objects.get(id=post_id)
        
        except Post.DoesNotExist:
        
            return None

    def is_deletable(self, post):
        # Check if post is eligible for deletion i.e. created within 24 hours
        return (timezone.now() - post.written_on) < timedelta(hours=24)

    def create_context_dict(self, thread, post, can_delete):

        return {'thread': thread, 'post': post, 'can_delete': can_delete}

    def get(self, request, forum_name_slug, thread_title_slug, post_id):
        # Handle GET request: display a confirmation page for deleting a post.
        thread = self.get_thread(forum_name_slug, thread_title_slug)

        post = self.get_post(post_id)

        can_delete = self.is_deletable(post)

        #If the thread or post is not found, render the template with no post.
        if thread is None or post is None:
        
            return render(request, 'main/delete_post.html', {'post': None})

        #Only the author can delete their post
        if request.user != post.author:
        
            return redirect('main:thread_detail', forum_name_slug=forum_name_slug, thread_title_slug=thread_title_slug)

        # Prepare the context with required details.
        context_dict = self.create_context_dict(thread, post, can_delete)

        return render(request, 'main/delete_post.html', context_dict)

    def post(self, request, forum_name_slug, thread_title_slug, post_id):
        # Handle POST request: process deletion of the post.
        thread = self.get_thread(forum_name_slug, thread_title_slug)

        post = self.get_post(post_id)

        # If either the thread or the post is missing, show error state
        if thread is None or post is None:

            return render(request, 'main/delete_post.html', {'post': None})

        # Ensure that only the author can perform deletion
        if request.user != post.author:
        
            return redirect('main:thread_detail', forum_name_slug=forum_name_slug, thread_title_slug=thread_title_slug)

        # Save the thread slug to use after deletion for redirection
        thread_slug = thread.slug
        
        post.delete()

        thread.updated_on = timezone.now()

        thread.save()

        return redirect('main:thread_detail', forum_name_slug=forum_name_slug, thread_title_slug=thread_slug)

@login_required
def save_thread(request, thread_title_slug):

    """
    Toggle saving a thread to the user's profile.
    If the thread is already saved, it is removed; otherwise, it is added.
    """

    # Retrieve the thread or return a 404 error if not found
    thread = get_object_or_404(Thread, slug=thread_title_slug)

    userprofile = request.user.userprofile

    #If the thread is already in the user's saved threads, remove it
    if thread in userprofile.saved_threads.all():

        userprofile.saved_threads.remove(thread)
    
    else:

        userprofile.saved_threads.add(thread)

    return redirect('main:thread_detail', forum_name_slug=thread.forum.slug, thread_title_slug=thread.slug)

@method_decorator(login_required, name='dispatch')
class PollVoteView(View):

    """
    Process a vote on a poll option.
    Validates that the forum, thread, poll, and poll option exist, and
    that the user has not already voted for that option.
    Returns a JSON response with the updated vote count.
    """
    def get_forum(self, forum_name_slug):
        # Retrieve forum using provided slug
        try:
    
            return Forum.objects.get(slug=forum_name_slug)
    
        except Forum.DoesNotExist:
    
            return None

    def get_thread(self, forum, thread_title_slug):
        # Retrieve the thread for the given forum
        try:
    
            return Thread.objects.get(slug=thread_title_slug, forum=forum)
    
        except Thread.DoesNotExist:
    
            return None

    def get_poll(self, thread):
        # Retrieve the poll attached to the thread.
        try:
    
            return Poll.objects.get(thread=thread)
    
        except Poll.DoesNotExist:
    
            return None

    def get_option(self, poll, option_id):
        # Retrieve the specific poll option by its ID
        try:
    
            return PollOption.objects.get(id=option_id, poll=poll)
    
        except PollOption.DoesNotExist:
    
            return None

    def post(self, request, forum_name_slug, thread_title_slug):
        # Process the vote submission
        forum = self.get_forum(forum_name_slug)
    
        if not forum:
            # Return error JSON if the forum doesn't exist
            return JsonResponse({'status': 'error', 'message': 'Forum not found'}, status=404)

        thread = self.get_thread(forum, thread_title_slug)
    
        if not thread:
    
            return JsonResponse({'status': 'error', 'message': 'Thread not found'}, status=404)

        poll = self.get_poll(thread)
    
        if not poll:
    
            return JsonResponse({'status': 'error', 'message': 'Poll not found'}, status=404)

        # Get the selected poll option from the POST data
        option_id = request.POST.get('option_id')
    
        if not option_id:
    
            return JsonResponse({'status': 'error', 'message': 'Invalid vote'}, status=400)

        option = self.get_option(poll, option_id)
    
        if not option:
    
            return JsonResponse({'status': 'error', 'message': 'Poll option not found'}, status=404)

        # Check if the user has already voted on this option.
        if request.user in option.voted_users.all():
    
            return JsonResponse({'status': 'error', 'message': 'You have already voted!'}, status=400)

        # Register the vote
        option.votes += 1
    
        option.voted_users.add(request.user)
    
        option.save()

        # Return success JSON with the updated vote count
        return JsonResponse({'status': 'success', 'votes': option.votes})

@method_decorator(login_required, name='dispatch')
class AddPollView(View):

    """
    Allow staff users to add a poll to a thread.
    Renders a form for the poll question and its options,
    then validates and saves the poll and its options.
    """

    def get_forum(self, forum_name_slug):

        # Retrieve the forum based on the slug.
        try:
    
            return Forum.objects.get(slug=forum_name_slug)
    
        except Forum.DoesNotExist:
    
            return None

    def get_thread(self, forum, thread_title_slug):

        # Retrieve the thread within the specified forum
        try:
    
            return Thread.objects.get(slug=thread_title_slug, forum=forum)
    
        except Thread.DoesNotExist:
    
            return None

    def get(self, request, forum_name_slug, thread_title_slug):

        # Only staff members are allowed to add a poll
        if not request.user.is_staff:
    
            return redirect(reverse('main:index'))

        forum = self.get_forum(forum_name_slug)

        thread = self.get_thread(forum, thread_title_slug)

        # Instantiate an empty poll form.
        poll_form = PollForm()

        # Create a formset for poll options with a minimum of 2 and maximum of 5 options
        PollOptionFormSet = formset_factory(PollOptionForm, extra=0, min_num=2, max_num=5)

        option_formset = PollOptionFormSet()

        context_dict = {
            'forum': forum,
            'thread': thread,
            'poll_form': poll_form,
            'option_formset': option_formset,
        }

        return render(request, 'main/add_poll.html', context_dict)

    def post(self, request, forum_name_slug, thread_title_slug):
        # Ensure only staff can post a poll
        if not request.user.is_staff:
        
            return redirect(reverse('main:index'))

        forum = self.get_forum(forum_name_slug)

        thread = self.get_thread(forum, thread_title_slug)

        # Bind the poll form and the option formset to the POST data
        poll_form = PollForm(request.POST)

        PollOptionFormSet = formset_factory(PollOptionForm, extra=0, min_num=2, max_num=5)
        
        option_formset = PollOptionFormSet(request.POST)

        # Validate both forms.
        if poll_form.is_valid() and option_formset.is_valid():
        
            poll = poll_form.save(commit=False)

            # Associate the poll with the current thread.
            poll.thread = thread
        
            poll.save()

            # Iterate over each poll option form and save if valid.
            for option_form in option_formset:
        
                if option_form.cleaned_data.get("option_text"):
        
                    option = option_form.save(commit=False)
        
                    option.poll = poll
        
                    option.save()

            # Redirect to the thread detail page after successful poll creation
            return redirect('main:thread_detail', forum_name_slug=forum.slug, thread_title_slug=thread.slug)

        # If validation fails, re-render the form with errors
        context_dict = {
            'forum': forum,
            'thread': thread,
            'poll_form': poll_form,
            'option_formset': option_formset,
        }

        return render(request, 'main/add_poll.html', context_dict)

class SearchView(View):

    """
    Process search queries across articles and threads.
    Filters articles and threads based on the query string and renders the search results
    """

    def get(self, request, *args, **kwargs):
        
        query = request.GET.get('q', '')
        
        if query:
            # Search for articles where the query is present in title, summary, or content
            articles = Article.objects.filter(
                Q(title__icontains=query) | 
                Q(summary__icontains=query) | 
                Q(content__icontains=query)
            ).distinct()

            # Search for threads where the query is present in the topic or title
            threads = Thread.objects.filter(
                Q(topic__icontains=query) | 
                Q(title__icontains=query)
            ).distinct()
        
        else:
        
            articles = []
        
            threads = []

        # Prepare the context with the query and results
        context_dict = {
            'query': query,
            'articles': articles,
            'threads': threads,
        }

        return render(request, 'main/search_results.html', context_dict)

def get_category_list(max_results=0, contains=''):

    """
    Return a list of categories
    If 'contains' is provided, filter categories whose names contain the term.
    Limit the number of results if max_results is set.
    """

    category_list = []
    
    if contains:
    
        category_list = Category.objects.filter(name__icontains=contains).order_by('name')
    
    else:
    
        category_list = Category.objects.order_by('name')
    
    if max_results > 0:
    
        if len(category_list) > max_results:
    
            category_list = category_list[:max_results]
    
    return category_list

def get_forum_list(max_results=0, contains=''):
    """
    Return a list of forums
    If 'contains' is provided, filter forums whose names contain the term.
    Limit the number of results if max_results is set.
    """
    forum_list = []
    
    if contains:
    
        forum_list = Forum.objects.filter(name__icontains=contains).order_by('name')
    
    else:
    
        forum_list = Forum.objects.order_by('name')
    
    if max_results > 0:
    
        if len(forum_list) > max_results:
    
            forum_list = forum_list[:max_results]
    
    return forum_list

class CategoryForumSuggestionView(View):

    """
    Provide suggestions for categories and forums based on a partial search term.
    Returns rendered HTML snippets for use in an AJAX response.
    """

    def get(self, request):
    
        suggestion = request.GET.get('suggestion', '')

        category_list = get_category_list(max_results=5, contains=suggestion)

        forum_list = get_forum_list(max_results=5, contains=suggestion)

        categories_html = render_to_string('main/categories.html', {'categories': category_list, 'current_category': None})

        forums_html = render_to_string('main/forums.html', {'forums': forum_list, 'current_forum': None})

        return JsonResponse({'categories': categories_html, 'forums': forums_html})