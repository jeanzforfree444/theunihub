from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from main.models import Category, Article, UserProfile, Comment, Forum, Thread, Post, Poll, PollOption, UNIVERSITY_CHOICES
from main.forms import CategoryForm, ArticleForm, UserProfileForm, CommentForm, ForumForm, ThreadForm, PostForm, PollForm, PollOptionForm
from datetime import datetime, timedelta
from main.bing_search import run_query
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.db import transaction
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.contrib.auth import logout
from django.utils.safestring import mark_safe
from django.forms import formset_factory
from django.template.loader import render_to_string
from django.conf import settings
import json

# Comprehensive list of banned words/phrases for content moderation across the platform
BANNED_WORDS = [
    # Profanity and Offensive Language: Common expletives and derogatory terms
    "fuck", "shit", "damn", "bitch", "ass", "asshole", "bastard", "prick", "wanker",
    "bollocks", "dick", "cunt", "twat", "arse", "arsehole", "motherfucker", "slut", "whore",
    "piss", "fag", "faggot", "cock", "pussy", "bastard", "douche", "cocksucker", "dickhead",
    "shithead", "fuckhead", "fucktard", "nigger", "nigga", "chink", "spic", "kike", "gook",

    # Sexual Content and Explicit Terms: Words related to explicit sexual acts or materials
    "porn", "hentai", "blowjob", "anal", "dildo", "vibrator", "cum", "orgasm",
    "pussy", "deepthroat", "threesome", "gangbang", "incest", "sex", "shag", "fucking",
    "sexually", "bukkake", "fisting", "rape", "fetish", "sexting", "cunnilingus", "masturbation",
    "moaning", "orgy", "ejaculate", "cumshot", "penis", "vagina", "erection", "busty", "boobs", "tits", 

    # Violence, Threats, and Harmful Content: Terms implying harm, violence, or threats
    "kill yourself", "die", "murder you", "bomb", "terrorist", "execute", "massacre", 
    "suicide", "genocide", "kill you", "murder", "gun", "shoot", "blood", "knife", "stab", 
    "explode", "rape", "attack", "abuse", "torture", "slaughter", "slit my wrists", "overdose", 
    "self harm", "hurt myself", "decapitate", "behead", "explode", "sniper", "violence", "war", "bloodshed",

    # Ableism, Discriminatory Terms, and Insults: Slurs and derogatory terms targeting disabilities or groups
    "retard", "cripple", "faggot", "dyke", "tranny", "spastic", "gimp", "moron", "idiot", "dumb", 
    "stupid", "imbecile", "imbecilic", "simpleton", "mongo", "idiotic", "retarded", "lunatic", 
    "psycho", "schizo", "bipolar", "autistic", "autism", "hysteric", "mentally ill", "psychiatric", 

    # Drug-Related Terms and Substance Abuse: References to illegal drugs and substance misuse
    "weed", "cocaine", "heroin", "meth", "ecstasy", "lsd", "shrooms", "ketamine", "overdose", 
    "marijuana", "opiate", "crack", "pill popper", "junkie", "high", "stoned", "blunt", "crackhead",
    "addiction", "substance abuse", "snort", "dab", "trip", "needle", "suboxone", "poppers",

    # Suicide and Self-Harm Related Content: Phrases indicating self-harm or suicidal intent
    "cut myself", "end my life", "overdose", "slit my wrists", "i want to die", "kill myself", "kms",
    "suicidal", "suicide pact", "suicide hotline", "self injury", "self-harm", "overdose", "end it all",
    "i'm done", "feeling empty", "kill me", "ending my life",

    # Spam, Scams, and Fraudulent Content: Terms often used in phishing or scam attempts
    "free money", "click here", "earn cash", "work from home", "make millions", "hot singles", 
    "win a prize", "unsecured loan", "credit repair", "pyramid scheme", "get rich quick", 
    "sign up now", "invest now", "bitcoin", "free gift card", "earn money fast", "no upfront fee",
    "referral link", "clickbait", "giveaway", "job offer", "lottery winner", "prize",

    # Hateful Speech and Discrimination: Terms promoting hate or targeting specific groups
    "racist", "xenophobe", "homophobe", "sexist", "misogynist", "bigot", "transphobic", "antisemitic", 
    "homo", "fag", "colored", "minority", "gypsy", "redneck", "illegal immigrant", "slur", 
    "nazi", "white supremacist", "KKK", "N-word", "cracker", "white trash", "wetback", "sand nigger", 
    "cholo", "beaner", "terrorist", "bitch", "jew", "kike", "kuffar", "chink", "gook",

    # Harmful or Inflammatory Phrases: Aggressive or demeaning phrases
    "shut up", "fuck off", "piss off", "get lost", "drop dead", "go to hell", "suck my dick", "shut your mouth",
    "eat shit", "go away", "off yourself", "you're useless", "no one cares", "nobody loves you", 
    "you're pathetic", "you're a waste of space", "no one will miss you", "go kill yourself", 
    "you'll never amount to anything", "end it already",

    # Inappropriate or Offensive Jokes, Memes, and Humor: Terms tied to offensive humor
    "yo mama", "your mom", "retarded joke", "cripple joke", "gay joke", "racist joke",
    "homophobic joke", "sexist joke", "offensive humor", "insensitive humor",
    "shock value", "inappropriate joke", "distasteful joke", "derogatory humor", "disrespectful",

    # Offensive Terms and Slang: Additional slurs and insults
    "bastard", "slut", "whore", "bimbo", "bastard", "asswipe", "shithead", "dickhead", "suck",
    "douchebag", "cockface", "cumdumpster", "fistfucker", "slutbag", "faggotbag", "pussyass", 
    "doucheass", "cockass", "assholeface", "twatwaffle", "assclown", "numbnuts", "dicktard", 
    "assmunch", "shitstain", "cockknocker", "motherfucker",

    # Malicious Content: Terms tied to cyberbullying or harmful intent
    "bitchslap", "kill himself", "kill herself", "kill themself", "slay yourself", "cut deep", "hang yourself",
    "self destruct", "self loathe", "destroy yourself", "cyberbully", "send nudes", "fuck you", "die in a hole", 
    "go die", "get lost", "no one cares", "your life is worthless", "empty shell", "kill me now",
    "suck my balls", "eat my ass", "go suck a dick", "die already", "shut the hell up",

    # Offensive Religious Terms: Blasphemous or religion-insulting phrases
    "goddamn", "jesus christ", "holy shit", "christ on a cracker", "fucking hell", "god is dead", 
    "blasphemy", "atheism", "hellfire", "burn in hell", "damnation", "satanist", "devil worshipper",
    "god hate", "jesus freak", "holy fuck"
]

# Dictionary mapping university identifiers to their official websites for easy linking
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

# ---------------------------#
# Cookie and Session Helpers #
# ---------------------------#

def get_server_side_cookie(request, cookie, default_val=None):
    """
    Retrieve a value stored in the session for a given cookie key.

    Args:
        request: The HTTP request object containing session data.
        cookie (str): The key to look up in the session.
        default_val: The value to return if the cookie is not found (defaults to None).

    Returns:
        The value associated with the cookie key in the session, or the default value if not found.
    """

    val = request.session.get(cookie)
    
    if not val:
    
        val = default_val
    
    return val

def visitor_cookie_handler(request):
    """
    Track visitor sessions by updating visit count and last visit timestamp in the session.

    Increments the visit count if a day has passed since the last visit. Stores the current
    timestamp as the last visit and updates the visit count in the session.

    Args:
        request: The HTTP request object containing session data.
    """

    # Get the current visit count from the session, defaulting to 0
    visits = int(get_server_side_cookie(request, 'visits', '0'))
    
    # Retrieve the last visit timestamp from the session
    last_visit_cookie = request.session.get('last_visit', None)

    if last_visit_cookie is None:

        # If no last visit is recorded, assume this is the first visit
        visits = 1

    else:

        try:
            
            # Parse the last visit timestamp from the session
            last_visit_time = datetime.strptime(last_visit_cookie, '%Y-%m-%d %H:%M:%S.%f')
        
        except ValueError:

            # If parsing fails, use the current time as a fallback
            last_visit_time = datetime.now()

        # Increment visits if more than a day has passed since the last visit
        if (datetime.now() - last_visit_time).days > 0:

            request.session['visits'] = visits

            visits += 1
    
    # Update the session with the current timestamp and visit count
    request.session['last_visit'] = str(datetime.now())

    request.session['visits'] = visits

# ---------------------------#
# View Classes               #
# ---------------------------#

class Custom404View(View):
    """
    Handle 404 errors by rendering a custom 404 page.

    This view is triggered when a requested URL does not match any defined route.
    """

    def get(self, request, *args, **kwargs):
        """
        Render the custom 404 error page.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: Rendered 404.html template with a 404 status code.
        """
    
        return render(request, 'main/404.html', status=404)

class IndexView(View):
    """
    Display the Jome page with top categories, articles, comments, and threads.

    Shows the top 5 categories and articles by views/points, recent comments, and threads
    with post counts. For authenticated users with a university, it also displays
    university-specific articles and threads.
    """

    def get(self, request):
        """
        Render the homepage with dynamic content based on user authentication.

        Updates the visitor session data and prepares context with popular content
        and university-specific data if applicable.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: Rendered index.html template with context data.
        """

        context_dict = {}

        # Fetch top 5 categories by views (descending order)
        category_list = Category.objects.order_by('-views')[:5]

        context_dict['categories'] = category_list

        # Fetch top 5 articles by points (descending order)
        article_list = Article.objects.order_by('-points')[:5]

        context_dict['articles'] = article_list
        
        # Fetch 5 most recent comments, prioritising edited ones
        comments = Comment.objects.order_by('-edited_on', '-written_on')[:5]

        context_dict['comments'] = comments

        # Fetch 5 most recently updated threads with post counts, prioritising updated ones
        threads = Thread.objects.annotate(post_count=Count('post')).order_by('-updated_on', '-started_on')[:5]
        
        context_dict['threads'] = threads

        university_articles = []
        
        university_threads = []

        university_website = None

        # If user is authenticated and has a university set, fetch related content
        if request.user.is_authenticated and request.user.userprofile.university:
        
            user_university = request.user.userprofile.university
        
            university_articles = Article.objects.filter(related_university=user_university).order_by('-updated_on', '-created_on')[:3]
        
            university_threads = Thread.objects.annotate(post_count=Count('post')).filter(related_university=user_university).order_by('-updated_on', '-started_on')[:3]

            university_website = UNIVERSITY_WEBSITES.get(user_university)

        context_dict['university_articles'] = university_articles
        
        context_dict['university_threads'] = university_threads

        context_dict['user_has_university'] = bool(request.user.is_authenticated and request.user.userprofile.university)
        
        context_dict['university_website'] = university_website

        # Track visitor session data
        visitor_cookie_handler(request)

        return render(request, 'main/index.html', context_dict)

class AboutView(View):
    """
    Display the About page with information about the team members.

    Shows profiles of predefined team members if they exist in the database.
    """
    def get(self, request):
        """
        Render the About page with team member profiles and visit count.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: Rendered about.html template with team member data.
        """
        
        context_dict = {}

        # List of team members with their usernames and profile keys
        team_members = [
            ('aaronhxx_1', 'founder_profile'),
            ('phoebe6504', 'developer_profile'),
            ('euan_galloway', 'marketing_profile'),
            ('worriless', 'system_profile'),
        ]

        profiles = []

        # Fetch profiles for each team member if they exist
        for username, key in team_members:

            profile = UserProfile.objects.filter(user__username=username).first()

            if profile:

                profiles.append(profile)

        context_dict['team_members'] = profiles

        # Update visitor session and include visit count
        visitor_cookie_handler(request)

        context_dict['visits'] = request.session.get('visits', 0)

        return render(request, 'main/about.html', context_dict)

class PrivacyView(View):
    """
    Display the Privacy Policy page.

    A static page outlining the platform's privacy policies.
    """

    def get(self, request):
        """
        Render the Privacy Policy page.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: Rendered privacy.html template.
        """

        return render(request, 'main/privacy.html')
    
class TermsView(View):
    """
    Display the Terms and Conditions page.

    A static page detailing the terms users must agree to for using the platform.
    """

    def get(self, request):
        """
        Render the Terms and Conditions page.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: Rendered terms.html template.
        """

        return render(request, 'main/terms.html')
    
class MissionVisionView(View):
    """
    Display the Mission and Vision page.

    A static page describing the platform's mission and vision statements.
    """

    def get(self, request):
        """
        Render the Mission and Vision page.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: Rendered mission_vision.html template.
        """

        return render(request, 'main/mission_vision.html')

class ContactView(View):
    """
    Handle the Contact page for users to send messages to the site administrators.

    GET: Displays an empty contact form.
    POST: Processes the form submission, sends an email, and provides feedback.
    """

    def get(self, request):
        """
        Render the Contact page with an empty form.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: Rendered contact.html template.
        """

        return render(request, 'main/contact.html')

    def post(self, request):
        """
        Process the contact form submission and send an email.

        Validates that all fields are filled, sends an email to the admin, and
        displays success or error messages accordingly.

        Args:
            request: The HTTP request object with POST data.

        Returns:
            HttpResponse: Rendered contact.html with feedback messages.
        """

        name = request.POST.get('name', '').strip()
        
        email = request.POST.get('email', '').strip()
        
        message = request.POST.get('message', '').strip()

        # Ensure all fields are provided
        if not all([name, email, message]):
        
            messages.error(request, "All fields are required.", extra_tags="danger")
            
            return render(request, 'main/contact.html', {
                'name': name,
                'email': email,
                'message': message
            })

        subject = f"New message from {name}"

        message_body = f"Message from: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:

            # Send email to the configured contact email address
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
    """
    Display the Values page.

    A static page outlining the core values of the platform.
    """

    def get(self, request):
        """
        Render the Values page.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: Rendered values.html template.
        """

        return render(request, 'main/values.html')

class FAQsView(View):
    """
    Display the Frequently Asked Questions (FAQs) page.

    A static page providing answers to common user questions.
    """

    def get(self, request):
        """
        Render the FAQs page.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: Rendered faqs.html template.
        """

        return render(request, 'main/faqs.html')

class StatsView(View):
    """
    Display platform statistics for staff users only.

    Shows counts of various entities (categories, articles, etc.) and aggregates
    like total points and views. Includes per-category and per-forum breakdowns.
    """

    @method_decorator(login_required)
    def get(self, request):
        """
        Render the statistics page if the user is staff.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: Rendered stats.html with statistics or redirect to index if not staff.
        """

        context_dict = {}

        # Restrict access to staff members only
        if not request.user.is_staff:

            return redirect(reverse('main:index'))
        
        # Basic counts of platform entities
        context_dict['total_categories'] = Category.objects.count()
        
        context_dict['total_articles'] = Article.objects.count()
        
        context_dict['total_comments'] = Comment.objects.count()
        
        context_dict['total_users'] = User.objects.count()
        
        context_dict['total_forums'] = Forum.objects.count()
        
        context_dict['total_threads'] = Thread.objects.count()
        
        context_dict['total_posts'] = Post.objects.count()

        # Aggregate metrics across all articles and posts
        total_points = sum(article.points for article in Article.objects.all())
        
        total_views = sum(article.views for article in Article.objects.all())

        context_dict['total_points'] = total_points
        
        context_dict['total_views'] = total_views

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
    Allow logged-in users to create or update their user profile.

    GET: Displays a blank profile form.
    POST: Processes the form submission and saves the profile.
    """

    @method_decorator(login_required)
    def get(self, request):
        """
        Render the profile registration form.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: Rendered profile_registration.html with an empty form.
        """

        form = UserProfileForm()

        context_dict = {'form': form}

        return render(request, 'main/profile_registration.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request):
        """
        Process the profile form submission and save the profile.

        Links the profile to the current user and redirects to the homepage on success.

        Args:
            request: The HTTP request object with POST data.

        Returns:
            HttpResponse: Redirect to index on success or re-render form with errors.
        """

        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():

            userprofile = form.save(commit=False)

            userprofile.user = request.user

            userprofile.save()

            return redirect(reverse('main:index'))
        
        else:
        
            print(form.errors) # Log errors for debugging
        
        context_dict = {'form': form}
        
        return render(request, 'main/profile_registration.html', context_dict)

class ProfileView(View):
    """
    Display a user's profile page with their details, articles, and threads.

    Shows the selected user's profile, their authored content, and university info if applicable.
    """

    def get_user_details(self, username):
        """
        Fetch user details and related content for the profile page.

        Args:
            username (str): The username of the user to display.

        Returns:
            dict: Context dictionary with user data or None if user not found.
        """

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
        """
        Render the profile page for the specified user.

        Args:
            request: The HTTP request object.
            username (str): The username of the user to display.

        Returns:
            HttpResponse: Rendered profile.html with user details.
        """
        
        context_dict = self.get_user_details(username)
                
        return render(request, 'main/profile.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, username):
        """
        Handle POST requests to the profile page (currently mirrors GET behavior).

        Args:
            request: The HTTP request object.
            username (str): The username of the user to display.

        Returns:
            HttpResponse: Rendered profile.html with user details.
        """

        context_dict = self.get_user_details(username)
                
        return render(request, 'main/profile.html', context_dict)

class EditProfileView(View):
    """
    Allow logged-in users to edit their own profile.

    GET: Displays the current profile data in a form.
    POST: Saves the updated profile data and redirects to the profile page.
    """

    def get_user_profile(self, user):
        """
        Fetch or create the user's profile.

        Args:
            user: The User object to fetch the profile for.

        Returns:
            UserProfile: The user's profile instance.
        """

        user_profile, created = UserProfile.objects.get_or_create(user=user)

        return user_profile

    @method_decorator(login_required)
    def get(self, request):
        """
        Render the profile edit form with current data.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: Rendered edit_profile.html with the form.
        """

        user_profile = self.get_user_profile(request.user)

        form = UserProfileForm(instance=user_profile)

        return render(request, 'main/edit_profile.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        """
        Process the profile edit form submission.

        Args:
            request: The HTTP request object with POST data.

        Returns:
            HttpResponse: Redirect to profile on success or re-render form with errors.
        """

        user_profile = self.get_user_profile(request.user)

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():

            form.save()

            return redirect(reverse('main:profile', kwargs={'username': request.user.username}))  

        return render(request, 'main/edit_profile.html', {'form': form})

class ListUsersView(View):
    """
    Display a list of all user profiles with filtering options.

    Supports filtering by username or university and provides AJAX support for dynamic updates.
    """

    @method_decorator(login_required)
    def get(self, request):
        """
        Render the user list page or return AJAX response with filtered profiles.

        Args:
            request: The HTTP request object with optional GET parameters (search, university).

        Returns:
            HttpResponse: Rendered list_users.html or JsonResponse for AJAX requests.
        """

        profiles = UserProfile.objects.all()

        # Get distinct university keys from profiles
        university_keys = UserProfile.objects.exclude(university__isnull=True).exclude(university="").values_list('university', flat=True).distinct()

        university_dict = dict(UNIVERSITY_CHOICES)

        universities = [(key, university_dict.get(key, key)) for key in university_keys]

        # Apply filters if provided
        search_query = request.GET.get('search', '').strip().lower()
        
        university_filter = request.GET.get('university', '').strip()

        if search_query:
        
            profiles = profiles.filter(user__username__icontains=search_query)

        if university_filter:
        
            profiles = profiles.filter(university=university_filter)

        # Handle AJAX requests for dynamic profile updates
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

            profiles_html = render_to_string('main/profiles.html', {'profiles': profiles, 'MEDIA_URL': settings.MEDIA_URL})
            
            return JsonResponse({'profiles_html': profiles_html})

        return render(request, 'main/list_users.html', {'profiles': profiles, 'universities': universities})

class DeleteAccountConfirmationView(View):
    """
    Display a confirmation page for account deletion.

    Allows users to confirm their intent to delete their account.
    """

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        Render the account deletion confirmation page.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: Rendered confirm_delete_account.html template.
        """
  
        return render(request, 'main/confirm_delete_account.html')

class DeleteAccountView(View):
    """
    Process the deletion of the current user's account.

    Logs out the user, deletes their account, and redirects to the homepage.
    """

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        Delete the user's account and log them out.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: Redirect to index with a success message.
        """
  
        user = request.user
  
        logout(request)
  
        user.delete()
  
        messages.success(request, "Your account has been successfully deleted.")
  
        return redirect('main:index')

class CategoryListView(View):
    """
    Display a list of all categories available on the platform.
    """

    def get(self, request):
        """
        Render the category list page.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: Rendered category_list.html with all categories.
        """

        context_dict = {}

        categories = Category.objects.all()
        
        context_dict['categories'] = categories

        return render(request, 'main/category_list.html', context_dict)

class ShowCategoryView(View):
    """
    Display details of a specific category and its articles.

    Increments the category's view count each time it is accessed.
    """

    def create_context_dict(self, category_name_slug):
        """
        Build the context dictionary for the category page.

        Args:
            category_name_slug (str): The slug of the category to display.

        Returns:
            dict: Context with category and article data or None if not found.
        """

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
        """
        Render the category page with its articles.

        Args:
            request: The HTTP request object.
            category_name_slug (str): The slug of the category.

        Returns:
            HttpResponse: Rendered category.html with category details.
        """

        context_dict = self.create_context_dict(category_name_slug)

        return render(request, 'main/category.html', context_dict)

class AddCategoryView(View):
    """
    Allow staff users to create a new category.

    GET: Displays an empty category form.
    POST: Processes the form and saves the new category.
    """

    @method_decorator(login_required)
    def get(self, request):
        """
        Render the add category form for staff users.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: Rendered add_category.html or redirect if not staff.
        """
        
        if not request.user.is_staff:

            return redirect(reverse('main:index'))

        form = CategoryForm()

        return render(request, 'main/add_category.html', {'form': form})
    
    @method_decorator(login_required)
    def post(self, request):
        """
        Process the category form submission and save the new category.

        Args:
            request: The HTTP request object with POST data.

        Returns:
            HttpResponse: Redirect to index on success or re-render form with errors.
        """
        
        if not request.user.is_staff:

            return redirect(reverse('main:index'))

        form = CategoryForm(request.POST)

        if form.is_valid():

            form.save(commit=True)

            return redirect(reverse('main:index'))
        
        else:

            print(form.errors) # Log errors for debugging
        
        return render(request, 'main/add_category.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class EditCategoryView(View):
    """
    Allow staff users to edit an existing category.

    Retrieves the category by slug, provides a pre-filled form, and saves changes.
    """

    def get_category(self, category_name_slug):
        """
        Fetch the category by its slug.

        Args:
            category_name_slug (str): The slug of the category.

        Returns:
            Category: The category object or None if not found.
        """

        try:

            return Category.objects.get(slug=category_name_slug)
        
        except Category.DoesNotExist:

            return None

    def create_context_dict(self, category):
        """
        Build the context dictionary for the edit form.

        Args:
            category: The Category object to edit.

        Returns:
            dict: Context with category and form data.
        """

        return {'category': category, 'form': CategoryForm(instance=category)}

    def get(self, request, category_name_slug):
        """
        Render the category edit form for staff users.

        Args:
            request: The HTTP request object.
            category_name_slug (str): The slug of the category.

        Returns:
            HttpResponse: Rendered edit_category.html or redirect if not staff.
        """
        
        if not request.user.is_staff:

            return redirect('main:show_category', category_name_slug=category_name_slug)

        category = self.get_category(category_name_slug)

        context_dict = self.create_context_dict(category)
        
        return render(request, 'main/edit_category.html', context_dict)

    def post(self, request, category_name_slug):
        """
        Process the category edit form submission.

        Args:
            request: The HTTP request object with POST data.
            category_name_slug (str): The slug of the category.

        Returns:
            HttpResponse: Redirect to category page on success or re-render form.
        """

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

    Displays a confirmation page and deletes the category upon confirmation.
    """

    def get_category(self, category_name_slug):
        """
        Fetch the category by its slug.

        Args:
            category_name_slug (str): The slug of the category.

        Returns:
            Category: The category object or None if not found.
        """
        
        try:
        
            return Category.objects.get(slug=category_name_slug)
        
        except Category.DoesNotExist:
        
            return None

    def get(self, request, category_name_slug):
        """
        Render the category deletion confirmation page.

        Args:
            request: The HTTP request object.
            category_name_slug (str): The slug of the category.

        Returns:
            HttpResponse: Rendered delete_category.html or redirect if not staff.
        """

        if not request.user.is_staff:

            return redirect('main:show_category', category_name_slug=category_name_slug)
        
        category = self.get_category(category_name_slug)

        if category is None:
        
            return render(request, 'main/delete_category.html', {'category': None})

        return render(request, 'main/delete_category.html', {'category': category})

    def post(self, request, category_name_slug):
        """
        Process the category deletion.

        Args:
            request: The HTTP request object.
            category_name_slug (str): The slug of the category.

        Returns:
            HttpResponse: Redirect to category list on success or redirect if not staff.
        """

        if not request.user.is_staff:

            return redirect('main:show_category', category_name_slug=category_name_slug)
        
        category = self.get_category(category_name_slug)

        if category is None:
        
            return render(request, 'main/delete_category.html', {'category': None})
        
        category.delete()

        return redirect('main:category_list')

class LikeCategoryView(View):
    """
    Increment the points of a category via an AJAX request.

    Used for user interaction to "like" a category.
    """

    @method_decorator(login_required)
    def get(self, request):
        """
        Increase the category's points and return the new count.

        Args:
            request: The HTTP request object with GET parameter 'category_id'.

        Returns:
            HttpResponse: New points value or -1 if category not found/invalid.
        """

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
    Decrease the points of a category via an AJAX request.

    Used for user interaction to "dislike" a category.
    """

    @method_decorator(login_required)
    def get(self, request):
        """
        Decrease the category's points and return the new count.

        Args:
            request: The HTTP request object with GET parameter 'category_id'.

        Returns:
            HttpResponse: New points value or -1 if category not found/invalid.
        """

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
    Display an article with its comments and a form to add new comments.

    Increments the article's view count each time it is accessed.
    """

    def create_context_dict(self, category_name_slug, article_title_slug):
        """
        Build the context dictionary for the article page.

        Args:
            category_name_slug (str): The slug of the article's category.
            article_title_slug (str): The slug of the article.

        Returns:
            dict: Context with article, category, and comments or None if not found.
        """

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
        """
        Render the article page with comments and a comment form.

        Args:
            request: The HTTP request object.
            category_name_slug (str): The slug of the category.
            article_title_slug (str): The slug of the article.

        Returns:
            HttpResponse: Rendered article.html with article details.
        """

        context_dict = self.create_context_dict(category_name_slug, article_title_slug)
        
        context_dict['form'] = CommentForm()
        
        return render(request, 'main/article.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, category_name_slug, article_title_slug):
        """
        Process a new comment submission for the article.

        Checks for banned words and updates the article's timestamp on success.

        Args:
            request: The HTTP request object with POST data.
            category_name_slug (str): The slug of the category.
            article_title_slug (str): The slug of the article.

        Returns:
            HttpResponse: Redirect to article page or re-render with form errors.
        """

        context_dict = self.create_context_dict(category_name_slug, article_title_slug)

        form = CommentForm(request.POST)
        
        if form.is_valid():

            content = form.cleaned_data['content']
            
            # Check for banned words in the comment's content
            if any(word in content.lower() for word in BANNED_WORDS):

                storage = messages.get_messages(request)
                
                storage.used = True

                messages.error(request, "Your comment contains innappropriate content and was not submitted.", extra_tags="danger")
        
            else:

                comment = form.save(commit=False)
            
                comment.article = context_dict['article']
            
                comment.author = request.user
            
                comment.save()
                
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
    Allow logged-in users to create a new article in a specified category.

    Supports an external Bing search query to assist with content creation.
    """

    def get_category_name(self, category_name_slug):
        """
        Fetch the category by its slug.

        Args:
            category_name_slug (str): The slug of the category.

        Returns:
            Category: The category object or None if not found.
        """

        try:

            category = Category.objects.get(slug=category_name_slug)

        except Category.DoesNotExist:

            category = None

        return category
    
    @method_decorator(login_required)
    def get(self, request, category_name_slug):
        """
        Render the add article form with optional search results.

        Args:
            request: The HTTP request object with optional 'query' GET parameter.
            category_name_slug (str): The slug of the category.

        Returns:
            HttpResponse: Rendered add_article.html with form and search results.
        """

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
        """
        Process the article form submission and save the new article.

        Checks for banned words in title, summary, and content.

        Args:
            request: The HTTP request object with POST data.
            category_name_slug (str): The slug of the category.

        Returns:
            HttpResponse: Redirect to article page on success or re-render form.
        """
        
        form = ArticleForm(request.POST, request.FILES)
        
        category = self.get_category_name(category_name_slug)

        if form.is_valid():

            title = form.cleaned_data['title']

            summary = form.cleaned_data['summary']

            content = form.cleaned_data['content']

            # Check for banned words in the article's title, summary, and content.
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
    Allow the article's author to edit its details.

    Ensures only the author can edit and checks for banned words in updated content.
    """

    def get_category(self, category_name_slug):
        """
        Fetch the category by its slug.

        Args:
            category_name_slug (str): The slug of the category.

        Returns:
            Category: The category object or None if not found.
        """

        try:

            return Category.objects.get(slug=category_name_slug)
        
        except Category.DoesNotExist:

            return None

    def get_article(self, article_title_slug):
        """
        Fetch the article by its slug.

        Args:
            article_title_slug (str): The slug of the article.

        Returns:
            Article: The article object or None if not found.
        """
        
        try:
        
            return Article.objects.get(slug=article_title_slug)
        
        except Article.DoesNotExist:
        
            return None

    def create_context_dict(self, article):
        """
        Build the context dictionary for the edit form.

        Args:
            article: The Article object to edit.

        Returns:
            dict: Context with article and form data.
        """
        
        return {'article': article, 'form': ArticleForm(instance=article)}

    def get(self, request, category_name_slug, article_title_slug):
        """
        Render the article edit form for the author.

        Args:
            request: The HTTP request object.
            category_name_slug (str): The slug of the category.
            article_title_slug (str): The slug of the article.

        Returns:
            HttpResponse: Rendered edit_article.html or redirect if not authorized.
        """

        category = self.get_category(category_name_slug)

        article = self.get_article(article_title_slug)

        if article is None:
            
            return render(request, 'main/edit_article.html', {'article': None})

        if request.user != article.author:

            return redirect('main:show_article', category_name_slug=category_name_slug, article_title_slug=article_title_slug)

        context_dict = self.create_context_dict(article)
        
        return render(request, 'main/edit_article.html', context_dict)

    def post(self, request, category_name_slug, article_title_slug):
        """
        Process the article edit form submission.

        Args:
            request: The HTTP request object with POST data.
            category_name_slug (str): The slug of the category.
            article_title_slug (str): The slug of the article.

        Returns:
            HttpResponse: Redirect to article page on success or re-render form.
        """

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

            # Check for banned words in the article's title, summary, and content.
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
    Allow the article's author to delete it.

    Displays a confirmation page and deletes the article if confirmed.
    """

    def get_article(self, category_name_slug, article_title_slug):
        """
        Fetch the article by its category and slug.

        Args:
            category_name_slug (str): The slug of the category.
            article_title_slug (str): The slug of the article.

        Returns:
            Article: The article object or None if not found.
        """

        try:
        
            return Article.objects.get(category__slug=category_name_slug, slug=article_title_slug)
        
        except Article.DoesNotExist:
        
            return None

    def get(self, request, category_name_slug, article_title_slug):
        """
        Render the article deletion confirmation page.

        Args:
            request: The HTTP request object.
            category_name_slug (str): The slug of the category.
            article_title_slug (str): The slug of the article.

        Returns:
            HttpResponse: Rendered delete_article.html or redirect if not authorized.
        """

        article = self.get_article(category_name_slug, article_title_slug)

        if article is None:
        
            return render(request, 'main/delete_article.html', {'article': None})

        if request.user != article.author:
        
            return redirect('main:show_article', category_name_slug=category_name_slug, article_title_slug=article_title_slug)

        return render(request, 'main/delete_article.html', {'article': article})

    def post(self, request, category_name_slug, article_title_slug):
        """
        Process the article deletion.

        Args:
            request: The HTTP request object.
            category_name_slug (str): The slug of the category.
            article_title_slug (str): The slug of the article.

        Returns:
            HttpResponse: Redirect to category page or redirect if not authorized.
        """

        article = self.get_article(category_name_slug, article_title_slug)

        if article is None or request.user != article.author:
        
            return redirect('main:show_article', category_name_slug=category_name_slug, article_title_slug=article_title_slug)

        category_slug = article.category.slug
        
        article.delete()

        return redirect('main:show_category', category_name_slug=category_slug)

@method_decorator(login_required, name='dispatch')
class EditCommentView(View):
    """
    Allow a comment's author to edit it within 24 hours of posting.

    Checks edit eligibility and validates content for banned words.
    """

    def get_article(self, category_name_slug, article_title_slug):
        """
        Fetch the article by its category and slug.

        Args:
            category_name_slug (str): The slug of the category.
            article_title_slug (str): The slug of the article.

        Returns:
            Article: The article object or None if not found.
        """
        
        try:
        
            return Article.objects.get(category__slug=category_name_slug, slug=article_title_slug)
        
        except Article.DoesNotExist:
        
            return None

    def get_comment(self, comment_id):
        """
        Fetch the comment by its ID.

        Args:
            comment_id (int): The ID of the comment.

        Returns:
            Comment: The comment object or None if not found.
        """
        
        try:
        
            return Comment.objects.get(id=comment_id)
        
        except Comment.DoesNotExist:
        
            return None

    def is_editable(self, comment):
        """
        Check if the comment can be edited (within 24 hours of posting).

        Args:
            comment: The Comment object to check.

        Returns:
            bool: True if editable, False otherwise.
        """

        return (timezone.now() - comment.written_on) < timedelta(hours=24)

    def create_context_dict(self, article, comment, can_edit):
        """
        Build the context dictionary for the edit form.

        Args:
            article: The Article object associated with the comment.
            comment: The Comment object to edit.
            can_edit (bool): Whether the comment is editable.

        Returns:
            dict: Context with article, comment, and form data.
        """
        
        return {'article': article, 'comment': comment, 'can_edit': can_edit, 'form': CommentForm(instance=comment)}

    def get(self, request, category_name_slug, article_title_slug, comment_id):
        """
        Render the comment edit form for the author.

        Args:
            request: The HTTP request object.
            category_name_slug (str): The slug of the category.
            article_title_slug (str): The slug of the article.
            comment_id (int): The ID of the comment.

        Returns:
            HttpResponse: Rendered edit_comment.html or redirect if not authorized.
        """

        article = self.get_article(category_name_slug, article_title_slug)
        
        comment = self.get_comment(comment_id)

        if article is None or comment is None:
        
            return render(request, 'main/edit_comment.html', {'comment': None})

        can_edit = self.is_editable(comment)

        if request.user != comment.author:
        
            return redirect('main:show_article', category_name_slug=category_name_slug, article_title_slug=article_title_slug)

        context_dict = self.create_context_dict(article, comment, can_edit)
        
        return render(request, 'main/edit_comment.html', context_dict)

    def post(self, request, category_name_slug, article_title_slug, comment_id):
        """
        Process the comment edit form submission.

        Args:
            request: The HTTP request object with POST data.
            category_name_slug (str): The slug of the category.
            article_title_slug (str): The slug of the article.
            comment_id (int): The ID of the comment.

        Returns:
            HttpResponse: Redirect to article page on success or re-render form.
        """

        article = self.get_article(category_name_slug, article_title_slug)
        
        comment = self.get_comment(comment_id)

        if article is None or comment is None:
        
            return render(request, 'main/edit_comment.html', {'comment': None})

        can_edit = self.is_editable(comment)

        if request.user != comment.author:
        
            return redirect('main:show_article', category_name_slug=category_name_slug, article_title_slug=article_title_slug)

        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():

            content = form.cleaned_data['content']
            
            # Check for banned words in the comment's content.
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
    Allow a comment's author to delete it within 24 hours of posting.

    Displays a confirmation page and deletes the comment if confirmed.
    """

    def get_article(self, category_name_slug, article_title_slug):
        """
        Fetch the article by its category and slug.

        Args:
            category_name_slug (str): The slug of the category.
            article_title_slug (str): The slug of the article.

        Returns:
            Article: The article object or None if not found.
        """

        try:
        
            return Article.objects.get(category__slug=category_name_slug, slug=article_title_slug)
        
        except Article.DoesNotExist:
        
            return None

    def get_comment(self, comment_id):
        """
        Fetch the comment by its ID.

        Args:
            comment_id (int): The ID of the comment.

        Returns:
            Comment: The comment object or None if not found.
        """

        try:
        
            return Comment.objects.get(id=comment_id)
        
        except Comment.DoesNotExist:
        
            return None

    def is_deletable(self, comment):
        """
        Check if the comment can be deleted (within 24 hours of posting).

        Args:
            comment: The Comment object to check.

        Returns:
            bool: True if deletable, False otherwise.
        """

        return (timezone.now() - comment.written_on) < timedelta(hours=24)

    def create_context_dict(self, article, comment, can_delete):
        """
        Build the context dictionary for the delete confirmation page.

        Args:
            article: The Article object associated with the comment.
            comment: The Comment object to delete.
            can_delete (bool): Whether the comment is deletable.

        Returns:
            dict: Context with article and comment data.
        """

        return {'article': article, 'comment': comment, 'can_delete': can_delete}

    def get(self, request, category_name_slug, article_title_slug, comment_id):
        """
        Render the comment deletion confirmation page.

        Args:
            request: The HTTP request object.
            category_name_slug (str): The slug of the category.
            article_title_slug (str): The slug of the article.
            comment_id (int): The ID of the comment.

        Returns:
            HttpResponse: Rendered delete_comment.html or redirect if not authorized.
        """

        article = self.get_article(category_name_slug, article_title_slug)

        comment = self.get_comment(comment_id)

        if article is None or comment is None:
        
            return render(request, 'main/delete_comment.html', {'comment': None})

        can_delete = self.is_deletable(comment)

        if request.user != comment.author:
        
            return redirect('main:show_article', category_name_slug=category_name_slug, article_title_slug=article_title_slug)

        context_dict = self.create_context_dict(article, comment, can_delete)

        return render(request, 'main/delete_comment.html', context_dict)

    def post(self, request, category_name_slug, article_title_slug, comment_id):
        """
        Process the comment deletion.

        Args:
            request: The HTTP request object.
            category_name_slug (str): The slug of the category.
            article_title_slug (str): The slug of the article.
            comment_id (int): The ID of the comment.

        Returns:
            HttpResponse: Redirect to article page or re-render if not found/authorized.
        """

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
    Increment the points of an article via an AJAX request.

    Used for user interaction to "like" an article.
    """

    @method_decorator(login_required)
    def get(self, request):
        """
        Increase the article's points and return the new count.

        Args:
            request: The HTTP request object with GET parameter 'article_id'.

        Returns:
            HttpResponse: New points value or -1 if article not found/invalid.
        """

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
    Decrease the points of an article via an AJAX request.

    Used for user interaction to "dislike" an article.
    """

    @method_decorator(login_required)
    def get(self, request):
        """
        Decrease the article's points and return the new count.

        Args:
            request: The HTTP request object with GET parameter 'article_id'.

        Returns:
            HttpResponse: New points value or -1 if article not found/invalid.
        """

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

    Adds or removes the article from the user's favourites list.

    Args:
        request: The HTTP request object.
        article_title_slug (str): The slug of the article to favourite/unfavourite.

    Returns:
        HttpResponse: Redirect to the article page.
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
    Display a list of all forums available on the platform.
    """

    def get(self, request):
        """
        Render the forum list page.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: Rendered forum_list.html with all forums.
        """

        context_dict = {}

        forums = Forum.objects.all()
        
        context_dict['forums'] = forums

        return render(request, 'main/forum_list.html', context_dict)
    
class AddForumView(View):
    """
    Allow staff users to create a new forum.

    GET: Displays an empty forum form.
    POST: Processes the form and saves the new forum.
    """

    @method_decorator(login_required)
    def get(self, request):
        """
        Render the add forum form for staff users.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: Rendered add_forum.html or redirect if not staff.
        """
        
        if not request.user.is_staff:

            return redirect(reverse('main:index'))

        form = ForumForm()

        return render(request, 'main/add_forum.html', {'form': form})
    
    @method_decorator(login_required)
    def post(self, request):
        """
        Process the forum form submission and save the new forum.

        Args:
            request: The HTTP request object with POST data.

        Returns:
            HttpResponse: Redirect to index on success or re-render form with errors.
        """

        if not request.user.is_staff:

            return redirect(reverse('main:index'))

        form = ForumForm(request.POST)

        if form.is_valid():

            form.save(commit=True)

            return redirect(reverse('main:index'))
        
        else:

            print(form.errors) # Log errors for debugging
        
        return render(request, 'main/add_forum.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class EditForumView(View):
    """
    Allow staff users to edit an existing forum.

    Retrieves the forum by slug, provides a pre-filled form, and saves changes.
    """

    def get_forum(self, forum_name_slug):
        """
        Fetch the forum by its slug.

        Args:
            forum_name_slug (str): The slug of the forum.

        Returns:
            Forum: The forum object or None if not found.
        """

        try:

            return Forum.objects.get(slug=forum_name_slug)
        
        except Forum.DoesNotExist:

            return None

    def create_context_dict(self, forum):
        """
        Build the context dictionary for the edit form.

        Args:
            forum: The Forum object to edit.

        Returns:
            dict: Context with forum and form data.
        """
        
        return {'forum': forum, 'form': ForumForm(instance=forum)}

    def get(self, request, forum_name_slug):
        """
        Render the forum edit form for staff users.

        Args:
            request: The HTTP request object.
            forum_name_slug (str): The slug of the forum.

        Returns:
            HttpResponse: Rendered edit_forum.html or redirect if not staff.
        """
        
        if not request.user.is_staff:

            return redirect('main:thread_list', forum_name_slug)

        forum = self.get_forum(forum_name_slug)

        context_dict = self.create_context_dict(forum)
        
        return render(request, 'main/edit_forum.html', context_dict)

    def post(self, request, forum_name_slug):
        """
        Process the forum edit form submission.

        Args:
            request: The HTTP request object with POST data.
            forum_name_slug (str): The slug of the forum.

        Returns:
            HttpResponse: Redirect to thread list on success or re-render form.
        """

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

    Displays a confirmation page and deletes the forum if confirmed.
    """

    def get_forum(self, forum_name_slug):
        """
        Fetch the forum by its slug.

        Args:
            forum_name_slug (str): The slug of the forum.

        Returns:
            Forum: The forum object or None if not found.
        """
        
        try:
        
            return Forum.objects.get(slug=forum_name_slug)
        
        except Forum.DoesNotExist:
        
            return None

    def get(self, request, forum_name_slug):
        """
        Render the forum deletion confirmation page.

        Args:
            request: The HTTP request object.
            forum_name_slug (str): The slug of the forum.

        Returns:
            HttpResponse: Rendered delete_forum.html or redirect if not staff.
        """

        if not request.user.is_staff:

            return redirect('main:thread_list', forum_name_slug=forum_name_slug)
        
        forum = self.get_forum(forum_name_slug)

        if forum is None:
        
            return render(request, 'main/delete_forum.html', {'forum': None})

        return render(request, 'main/delete_forum.html', {'forum': forum})

    def post(self, request, forum_name_slug):
        """
        Process the forum deletion.

        Args:
            request: The HTTP request object.
            forum_name_slug (str): The slug of the forum.

        Returns:
            HttpResponse: Redirect to forum list on success or re-render if not found.
        """

        if not request.user.is_staff:

            return redirect('main:thread_list', forum_name_slug=forum_name_slug)
        
        forum = self.get_forum(forum_name_slug)

        if forum is None:
        
            return render(request, 'main/delete_forum.html', {'forum': None})
        
        forum.delete()

        return redirect('main:forum_list')

class ThreadListView(View):
    """
    Display a list of threads within a specific forum.
    """

    def create_context_dict(self, forum_name_slug):
        """
        Build the context dictionary for the thread list page.

        Args:
            forum_name_slug (str): The slug of the forum.

        Returns:
            dict: Context with forum and thread data or None if not found.
        """
        
        context_dict = {}

        try:

            forum = Forum.objects.get(slug=forum_name_slug)

            threads = Thread.objects.filter(forum=forum).annotate(post_count=Count('post'))

            context_dict['threads'] = threads

            context_dict['forum'] = forum

        except Forum.DoesNotExist:

            context_dict['threads'] = None

            context_dict['forum'] = None

        return context_dict

    def get(self, request, forum_name_slug):
        """
        Render the thread list page for the specified forum.

        Args:
            request: The HTTP request object.
            forum_name_slug (str): The slug of the forum.

        Returns:
            HttpResponse: Rendered thread_list.html with thread data.
        """

        context_dict = self.create_context_dict(forum_name_slug)

        return render(request, 'main/thread_list.html', context_dict)

@method_decorator(login_required, name='dispatch')
class ThreadDetailView(View):
    """
    Display details of a thread, including its posts and optional poll.

    Provides a form to add new posts and displays poll options if present.
    """

    def create_context_dict(self, forum_name_slug, thread_title_slug):
        """
        Build the context dictionary for the thread detail page.

        Args:
            forum_name_slug (str): The slug of the forum.
            thread_title_slug (str): The slug of the thread.

        Returns:
            dict: Context with forum, thread, posts, and poll data or None if not found.
        """

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
        """
        Render the thread detail page with posts and a post form.

        Args:
            request: The HTTP request object with optional 'query' GET parameter.
            forum_name_slug (str): The slug of the forum.
            thread_title_slug (str): The slug of the thread.

        Returns:
            HttpResponse: Rendered thread_detail.html with thread details.
        """

        context_dict = self.create_context_dict(forum_name_slug, thread_title_slug)

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
        """
        Process a new post submission for the thread.

        Checks for banned words and updates the thread's timestamp on success.

        Args:
            request: The HTTP request object with POST data.
            forum_name_slug (str): The slug of the forum.
            thread_title_slug (str): The slug of the thread.

        Returns:
            HttpResponse: Redirect to thread page on success or re-render form.
        """

        context_dict = self.create_context_dict(forum_name_slug, thread_title_slug)

        form = PostForm(request.POST)

        query = request.POST.get('query', '').strip()

        if query:

            context_dict['query'] = query

            context_dict['result_list'] = run_query(query)

        if form.is_valid():

            content = form.cleaned_data['content']
            
            # Check for banned words in the post's content.
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
    Enable logged-in users to create a new thread within a specified forum.

    This view supports both creating a thread from scratch and assisting users with content generation
    by integrating an external Bing search query. It ensures that only authenticated users can access
    this functionality and validates thread content against a list of banned words before saving.
    """

    def get_forum_name(self, forum_name_slug):
        """
        Retrieve the forum object based on its slug identifier.

        Args:
            forum_name_slug (str): The unique slug of the forum to fetch.

        Returns:
            Forum or None: The Forum object if found, otherwise None if the forum does not exist.
        """

        try:

            forum = Forum.objects.get(slug=forum_name_slug)

        except Forum.DoesNotExist:

            forum = None

        return forum

    @method_decorator(login_required)
    def get(self, request, forum_name_slug):
        """
        Display the thread creation form with optional search results to assist content creation.

        Fetches the forum by its slug, initializes an empty thread form, and optionally includes
        search results if a query parameter is provided. This allows users to reference external
        content while drafting their thread.

        Args:
            request: The HTTP request object containing user session and GET parameters.
            forum_name_slug (str): The slug of the forum where the thread will be created.

        Returns:
            HttpResponse: Rendered create_thread.html template with the form and optional search data.
        """

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
        """
        Process the thread creation form submission and save the new thread.

        Validates the form data, checks the title and topic for banned words, associates the thread
        with the current user and forum, and redirects to the thread detail page on success. If
        validation fails or banned words are detected, it re-renders the form with error messages.

        Args:
            request: The HTTP request object containing POST data and user session.
            forum_name_slug (str): The slug of the forum where the thread will be created.

        Returns:
            HttpResponse: Redirect to thread detail page on success, or re-rendered form on failure.
        """

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

            # Check for banned words in the threads's title and topic
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
    Allow the original author of a thread to edit its details.

    Ensures that only the thread's author can make changes, provides a pre-filled form with existing
    data, and validates updated content against banned words. Redirects unauthorized users to the
    thread detail page.
    """

    def get_forum(self, forum_name_slug):
        """
        Retrieve the forum object using its slug.

        Args:
            forum_name_slug (str): The slug of the forum to fetch.

        Returns:
            Forum or None: The Forum object if found, otherwise None if the forum does not exist.
        """

        try:

            return Forum.objects.get(slug=forum_name_slug)
        
        except Forum.DoesNotExist:

            return None

    def get_thread(self, thread_title_slug):
        """
        Retrieve the thread object using its slug.

        Args:
            thread_title_slug (str): The slug of the thread to fetch.

        Returns:
            Thread or None: The Thread object if found, otherwise None if the thread does not exist.
        """
        
        try:
        
            return Thread.objects.get(slug=thread_title_slug)
        
        except Thread.DoesNotExist:
        
            return None

    def create_context_dict(self, thread):
        """
        Build the context dictionary for the thread edit form.

        Args:
            thread: The Thread object being edited.

        Returns:
            dict: A dictionary containing the thread and a pre-filled form instance.
        """
        
        return {'thread': thread, 'form': ThreadForm(instance=thread)}

    def get(self, request, forum_name_slug, thread_title_slug):
        """
        Display the thread edit form for the thread's author.

        Fetches the forum and thread, checks if the current user is the author, and renders the edit
        form with existing thread data. Redirects non-authors to the thread detail page.

        Args:
            request: The HTTP request object containing user session.
            forum_name_slug (str): The slug of the forum containing the thread.
            thread_title_slug (str): The slug of the thread to edit.

        Returns:
            HttpResponse: Rendered edit_thread.html template or redirect if unauthorized.
        """

        forum = self.get_forum(forum_name_slug)

        thread = self.get_thread(thread_title_slug)

        if thread is None:

            return render(request, 'main/edit_thread.html', {'thread': None})

        if request.user != thread.author:

            return redirect('main:thread_detail', forum_name_slug=forum_name_slug, thread_title_slug=thread_title_slug)

        context_dict = self.create_context_dict(thread)
        
        return render(request, 'main/edit_thread.html', context_dict)

    def post(self, request, forum_name_slug, thread_title_slug):
        """
        Process the thread edit form submission and save changes.

        Validates the updated form data, checks for banned words in the title and topic, and saves
        the changes if valid. Redirects to the thread detail page on success or re-renders the form
        with errors if validation fails.

        Args:
            request: The HTTP request object containing POST data and user session.
            forum_name_slug (str): The slug of the forum containing the thread.
            thread_title_slug (str): The slug of the thread to edit.

        Returns:
            HttpResponse: Redirect to thread detail page on success, or re-rendered form on failure.
        """

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

            # Check for banned words in the thread's title and topic
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
    Allow the author of a thread to delete it entirely.

    Presents a confirmation page to the thread’s author and, upon confirmation, deletes the thread
    along with its associated posts and poll (if any). Only the author can perform this action.
    """

    def get_thread(self, forum_name_slug, thread_title_slug):
        """
        Retrieve the thread object based on its forum slug and thread slug.

        Args:
            forum_name_slug (str): The slug of the forum containing the thread.
            thread_title_slug (str): The slug of the thread to fetch.

        Returns:
            Thread or None: The Thread object if found, otherwise None if the thread does not exist.
        """

        try:
        
            return Thread.objects.get(forum__slug=forum_name_slug, slug=thread_title_slug)
        
        except Thread.DoesNotExist:
        
            return None

    def get(self, request, forum_name_slug, thread_title_slug):
        """
        Display the thread deletion confirmation page.

        Fetches the thread and checks if the current user is the author. If authorized, it renders
        a confirmation page; otherwise, it redirects to the thread detail page.

        Args:
            request: The HTTP request object containing user session.
            forum_name_slug (str): The slug of the forum containing the thread.
            thread_title_slug (str): The slug of the thread to delete.

        Returns:
            HttpResponse: Rendered delete_thread.html template or redirect if unauthorized.
        """
        
        thread = self.get_thread(forum_name_slug, thread_title_slug)
        
        if thread is None:
        
            return render(request, 'main/delete_thread.html', {'thread': None})

        if request.user != thread.author:
        
            return redirect('main:thread_detail', forum_name_slug=forum_name_slug, thread_title_slug=thread_title_slug)

        return render(request, 'main/delete_thread.html', {'thread': thread})

    def post(self, request, forum_name_slug, thread_title_slug):
        """
        Process the thread deletion upon user confirmation.

        Deletes the thread if the current user is the author and redirects to the forum’s thread list.
        If the thread is not found or the user is not authorized, it redirects to the thread detail page.

        Args:
            request: The HTTP request object containing user session.
            forum_name_slug (str): The slug of the forum containing the thread.
            thread_title_slug (str): The slug of the thread to delete.

        Returns:
            HttpResponse: Redirect to thread list on success, or thread detail page if unauthorized.
        """
        
        thread = self.get_thread(forum_name_slug, thread_title_slug)

        if thread is None or request.user != thread.author:
        
            return redirect('main:show_thread', forum_name_slug=forum_name_slug, thread_title_slug=thread_title_slug)

        forum_slug = thread.forum.slug
        
        thread.delete()

        return redirect('main:thread_list', forum_name_slug=forum_slug)

@method_decorator(login_required, name='dispatch')
class EditPostView(View):
    """
    Allow the author of a post to edit its content within 24 hours of creation.

    Ensures that only the post’s author can edit it, enforces a 24-hour edit window, and validates
    the updated content against banned words. Updates the thread’s timestamp upon successful edit.
    """

    def get_thread(self, forum_name_slug, thread_title_slug):
        """
        Retrieve the thread object based on its forum slug and thread slug.

        Args:
            forum_name_slug (str): The slug of the forum containing the thread.
            thread_title_slug (str): The slug of the thread containing the post.

        Returns:
            Thread or None: The Thread object if found, otherwise None if the thread does not exist.
        """
        
        try:
        
            return Thread.objects.get(forum__slug=forum_name_slug, slug=thread_title_slug)
        
        except Thread.DoesNotExist:
        
            return None

    def get_post(self, post_id):
        """
        Retrieve the post object based on its unique identifier.

        Args:
            post_id (int): The primary key of the post to fetch.

        Returns:
            Post or None: The Post object if found, otherwise None if the post does not exist.
        """
        
        try:
        
            return Post.objects.get(id=post_id)
        
        except Post.DoesNotExist:
        
            return None

    def is_editable(self, post):
        """
        Determine if the post is still within the 24-hour editable period.

        Args:
            post: The Post object to check.

        Returns:
            bool: True if the post was created less than 24 hours ago, False otherwise.
        """

        return (timezone.now() - post.written_on) < timedelta(hours=24)

    def create_context_dict(self, thread, post, can_edit):
        """
        Build the context dictionary for the post edit form.

        Args:
            thread: The Thread object containing the post.
            post: The Post object being edited.
            can_edit (bool): Indicates whether the post is within the editable time window.

        Returns:
            dict: A dictionary containing the thread, post, edit status, and pre-filled form.
        """
        
        return {'thread': thread, 'post': post, 'can_edit': can_edit, 'form': PostForm(instance=post)}

    def get(self, request, forum_name_slug, thread_title_slug, post_id):
        """
        Display the post edit form for the post’s author.

        Fetches the thread and post, checks if the user is the author and if the post is editable,
        then renders the edit form. Redirects unauthorized users to the thread detail page.

        Args:
            request: The HTTP request object containing user session.
            forum_name_slug (str): The slug of the forum containing the thread.
            thread_title_slug (str): The slug of the thread containing the post.
            post_id (int): The ID of the post to edit.

        Returns:
            HttpResponse: Rendered edit_post.html template or redirect if unauthorized.
        """

        thread = self.get_thread(forum_name_slug, thread_title_slug)

        post = self.get_post(post_id)

        if thread is None or post is None:
        
            return render(request, 'main/edit_post.html', {'post': None})

        can_edit = self.is_editable(post)

        if request.user != post.author:
        
            return redirect('main:thread_detail', forum_name_slug=forum_name_slug, thread_title_slug=thread_title_slug)

        context_dict = self.create_context_dict(thread, post, can_edit)
        
        return render(request, 'main/edit_post.html', context_dict)

    def post(self, request, forum_name_slug, thread_title_slug, post_id):
        """
        Process the post edit form submission and save changes.

        Validates the updated content, checks for banned words, and updates the post and thread
        timestamp if successful. Redirects to the thread detail page on success or re-renders the
        form with errors if validation fails.

        Args:
            request: The HTTP request object containing POST data and user session.
            forum_name_slug (str): The slug of the forum containing the thread.
            thread_title_slug (str): The slug of the thread containing the post.
            post_id (int): The ID of the post to edit.

        Returns:
            HttpResponse: Redirect to thread detail page on success, or re-rendered form on failure.
        """

        thread = self.get_thread(forum_name_slug, thread_title_slug)
        
        post = self.get_post(post_id)

        if thread is None or post is None:
        
            return render(request, 'main/edit_post.html', {'post': None})

        can_edit = self.is_editable(post)

        if request.user != post.author:
        
            return redirect('main:thread_detail', forum_name_slug=forum_name_slug, thread_title_slug=thread_title_slug)

        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            content = form.cleaned_data['content']

            # Check for banned words in the post's content
            if any(word in content.lower() for word in BANNED_WORDS):

                storage = messages.get_messages(request)
                
                storage.used = True

                messages.error(request, "Your post contains inappropriate content and was not edited.", extra_tags="danger")
        
            else:

                form.save()

                thread.updated_on = timezone.now()

                thread.save()

                messages.success(request, "Your post has been edited successfully.")

                return redirect("main:thread_detail", forum_name_slug=forum_name_slug, thread_title_slug=thread_title_slug)

        context_dict = self.create_context_dict(thread, post, can_edit)

        context_dict['form'] = form

        return render(request, 'main/edit_post.html', context_dict)

@method_decorator(login_required, name='dispatch')
class DeletePostView(View):
    """
    Allow the author of a post to delete it within 24 hours of creation.

    Presents a confirmation page to the post’s author and deletes the post if confirmed, updating
    the thread’s timestamp. Only the author can perform this action within the time limit.
    """

    def get_thread(self, forum_name_slug, thread_title_slug):
        """
        Retrieve the thread object based on its forum slug and thread slug.

        Args:
            forum_name_slug (str): The slug of the forum containing the thread.
            thread_title_slug (str): The slug of the thread containing the post.

        Returns:
            Thread or None: The Thread object if found, otherwise None if the thread does not exist.
        """

        try:
        
            return Thread.objects.get(forum__slug=forum_name_slug, slug=thread_title_slug)
        
        except Thread.DoesNotExist:
        
            return None

    def get_post(self, post_id):
        """
        Retrieve the post object based on its unique identifier.

        Args:
            post_id (int): The primary key of the post to fetch.

        Returns:
            Post or None: The Post object if found, otherwise None if the post does not exist.
        """

        try:
        
            return Post.objects.get(id=post_id)
        
        except Post.DoesNotExist:
        
            return None

    def is_deletable(self, post):
        """
        Determine if the post is still within the 24-hour deletable period.

        Args:
            post: The Post object to check.

        Returns:
            bool: True if the post was created less than 24 hours ago, False otherwise.
        """

        return (timezone.now() - post.written_on) < timedelta(hours=24)

    def create_context_dict(self, thread, post, can_delete):
        """
        Build the context dictionary for the post deletion confirmation page.

        Args:
            thread: The Thread object containing the post.
            post: The Post object to delete.
            can_delete (bool): Indicates whether the post is within the deletable time window.

        Returns:
            dict: A dictionary containing the thread, post, and delete status.
        """

        return {'thread': thread, 'post': post, 'can_delete': can_delete}

    def get(self, request, forum_name_slug, thread_title_slug, post_id):
        """
        Display the post deletion confirmation page.

        Fetches the thread and post, checks if the user is the author and if the post is deletable,
        then renders the confirmation page. Redirects unauthorized users to the thread detail page.

        Args:
            request: The HTTP request object containing user session.
            forum_name_slug (str): The slug of the forum containing the thread.
            thread_title_slug (str): The slug of the thread containing the post.
            post_id (int): The ID of the post to delete.

        Returns:
            HttpResponse: Rendered delete_post.html template or redirect if unauthorized.
        """

        thread = self.get_thread(forum_name_slug, thread_title_slug)

        post = self.get_post(post_id)

        if thread is None or post is None:
        
            return render(request, 'main/delete_post.html', {'post': None})

        can_delete = self.is_deletable(post)

        if request.user != post.author:
        
            return redirect('main:thread_detail', forum_name_slug=forum_name_slug, thread_title_slug=thread_title_slug)

        context_dict = self.create_context_dict(thread, post, can_delete)

        return render(request, 'main/delete_post.html', context_dict)

    def post(self, request, forum_name_slug, thread_title_slug, post_id):
        """
        Process the post deletion upon user confirmation.

        Deletes the post if the user is the author and updates the thread timestamp. Redirects to
        the thread detail page on success or if unauthorized.

        Args:
            request: The HTTP request object containing user session.
            forum_name_slug (str): The slug of the forum containing the thread.
            thread_title_slug (str): The slug of the thread containing the post.
            post_id (int): The ID of the post to delete.

        Returns:
            HttpResponse: Redirect to thread detail page on success or if unauthorized.
        """

        thread = self.get_thread(forum_name_slug, thread_title_slug)

        post = self.get_post(post_id)

        if thread is None or post is None:

            return render(request, 'main/delete_post.html', {'post': None})

        if request.user != post.author:
        
            return redirect('main:thread_detail', forum_name_slug=forum_name_slug, thread_title_slug=thread_title_slug)

        thread_slug = thread.slug
        
        post.delete()

        thread.updated_on = timezone.now()

        thread.save()

        return redirect('main:thread_detail', forum_name_slug=forum_name_slug, thread_title_slug=thread_slug)

@login_required
def save_thread(request, thread_title_slug):
    """
    Toggle the saved status of a thread in the user’s profile.

    Adds the thread to the user’s saved threads if not already saved, or removes it if it is.
    Requires the user to be logged in and redirects back to the thread detail page.

    Args:
        request: The HTTP request object containing user session.
        thread_title_slug (str): The slug of the thread to save or unsave.

    Returns:
        HttpResponse: Redirect to the thread detail page after toggling the saved status.
    """

    thread = get_object_or_404(Thread, slug=thread_title_slug)

    userprofile = request.user.userprofile

    if thread in userprofile.saved_threads.all():

        userprofile.saved_threads.remove(thread)
    
    else:

        userprofile.saved_threads.add(thread)

    return redirect('main:thread_detail', forum_name_slug=thread.forum.slug, thread_title_slug=thread.slug)

@method_decorator(login_required, name='dispatch')
class PollVoteView(View):
    """
    Handle user votes on poll options within a thread.

    Validates the existence of the forum, thread, poll, and poll option, ensures the user hasn’t
    already voted, and increments the vote count. Returns a JSON response with the updated vote
    tally or an error message if validation fails.
    """

    def get_forum(self, forum_name_slug):
        """
        Retrieve the forum object based on its slug.

        Args:
            forum_name_slug (str): The slug of the forum to fetch.

        Returns:
            Forum or None: The Forum object if found, otherwise None if the forum does not exist.
        """

        try:
    
            return Forum.objects.get(slug=forum_name_slug)
    
        except Forum.DoesNotExist:
    
            return None

    def get_thread(self, forum, thread_title_slug):
        """
        Retrieve the thread object within the specified forum.

        Args:
            forum: The Forum object containing the thread.
            thread_title_slug (str): The slug of the thread to fetch.

        Returns:
            Thread or None: The Thread object if found, otherwise None if the thread does not exist.
        """

        try:
    
            return Thread.objects.get(slug=thread_title_slug, forum=forum)
    
        except Thread.DoesNotExist:
    
            return None

    def get_poll(self, thread):
        """
        Retrieve the poll object associated with the thread.

        Args:
            thread: The Thread object containing the poll.

        Returns:
            Poll or None: The Poll object if found, otherwise None if no poll exists.
        """

        try:
    
            return Poll.objects.get(thread=thread)
    
        except Poll.DoesNotExist:
    
            return None

    def get_option(self, poll, option_id):
        """
        Retrieve the specific poll option based on its ID.

        Args:
            poll: The Poll object containing the option.
            option_id (int): The ID of the poll option to fetch.

        Returns:
            PollOption or None: The PollOption object if found, otherwise None if it does not exist.
        """

        try:
    
            return PollOption.objects.get(id=option_id, poll=poll)
    
        except PollOption.DoesNotExist:
    
            return None

    def post(self, request, forum_name_slug, thread_title_slug):
        """
        Process a user’s vote on a poll option and return the result as JSON.

        Validates the chain of forum, thread, poll, and option existence, checks if the user has
        already voted, and updates the vote count if valid. Returns a success response with the
        new vote count or an error response if any validation fails.

        Args:
            request: The HTTP request object containing POST data (option_id) and user session.
            forum_name_slug (str): The slug of the forum containing the thread.
            thread_title_slug (str): The slug of the thread containing the poll.

        Returns:
            JsonResponse: JSON object with status and either vote count or error message.
        """

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

        if request.user in poll.voted_users.all():
    
            return JsonResponse({'status': 'error', 'message': 'You have already voted on this poll!'}, status=400)

        option.votes += 1
    
        poll.voted_users.add(request.user)
    
        option.save()

        return JsonResponse({'status': 'success', 'votes': option.votes})

@method_decorator(login_required, name='dispatch')
class AddPollView(View):
    """
    Allow staff users to add a poll to an existing thread.

    Provides a form for entering a poll question and multiple options (between 2 and 5), validates
    the input, and saves the poll and its options atomically. Only staff members can access this view.
    """

    def get_forum(self, forum_name_slug):
        """
        Retrieve the forum object based on its slug.

        Args:
            forum_name_slug (str): The slug of the forum to fetch.

        Returns:
            Forum or None: The Forum object if found, otherwise None if the forum does not exist.
        """

        try:
    
            return Forum.objects.get(slug=forum_name_slug)
    
        except Forum.DoesNotExist:
    
            return None

    def get_thread(self, forum, thread_title_slug):
        """
        Retrieve the thread object within the specified forum.

        Args:
            forum: The Forum object containing the thread.
            thread_title_slug (str): The slug of the thread to fetch.

        Returns:
            Thread or None: The Thread object if found, otherwise None if the thread does not exist.
        """

        try:
    
            return Thread.objects.get(slug=thread_title_slug, forum=forum)
    
        except Thread.DoesNotExist:
    
            return None

    def get(self, request, forum_name_slug, thread_title_slug):
        """
        Display the poll creation form for staff users.

        Fetches the forum and thread, initializes a poll form and an option formset (with a minimum
        of 2 and maximum of 5 options), and renders the form page. Redirects non-staff users to the homepage.

        Args:
            request: The HTTP request object containing user session.
            forum_name_slug (str): The slug of the forum containing the thread.
            thread_title_slug (str): The slug of the thread to add the poll to.

        Returns:
            HttpResponse: Rendered add_poll.html template or redirect if not staff.
        """

        if not request.user.is_staff:
    
            return redirect(reverse('main:index'))

        forum = self.get_forum(forum_name_slug)

        thread = self.get_thread(forum, thread_title_slug)

        if not thread:
            
            return render(request, 'main/add_poll.html', {'thread': None})

        poll_form = PollForm()

        PollOptionFormSet = formset_factory(PollOptionForm, extra=0, min_num=2, max_num=5)

        option_formset = PollOptionFormSet(initial=[{}, {}])

        context_dict = {
            'forum': forum,
            'thread': thread,
            'poll_form': poll_form,
            'option_formset': option_formset,
        }

        return render(request, 'main/add_poll.html', context_dict)

    def post(self, request, forum_name_slug, thread_title_slug):
        """
        Process the poll creation form submission and save the poll with its options.

        Validates the poll question and options, ensures the number of options is between 2 and 5,
        and saves everything in a transaction. Redirects to the thread detail page on success or
        re-renders the form with errors if validation fails.

        Args:
            request: The HTTP request object containing POST data and user session.
            forum_name_slug (str): The slug of the forum containing the thread.
            thread_title_slug (str): The slug of the thread to add the poll to.

        Returns:
            HttpResponse: Redirect to thread detail page on success, or re-rendered form on failure.
        """

        if not request.user.is_staff:
        
            return redirect(reverse('main:index'))

        forum = self.get_forum(forum_name_slug)

        thread = self.get_thread(forum, thread_title_slug)

        if not thread:

            return render(request, 'main/add_poll.html', {'thread': None})

        poll_form = PollForm(request.POST)

        PollOptionFormSet = formset_factory(PollOptionForm, extra=0, min_num=2, max_num=5)
        
        option_formset = PollOptionFormSet(request.POST)

        if poll_form.is_valid() and option_formset.is_valid():
                
            try:

                with transaction.atomic():
        
                    poll = Poll(thread=thread, question=poll_form.cleaned_data['question'])
                
                    poll.save(skip_validation=True)

                    options = []

                    for option_form in option_formset:
                
                        if option_form.cleaned_data.get("option_text"):

                            option = PollOption(
                                poll=poll,
                                option_text=option_form.cleaned_data['option_text']
                            )

                            option.save()
                
                            options.append(option)
                                    
                    poll.full_clean()

                    if len(options) < Poll.MIN_OPTIONS:

                        raise ValidationError(f'A poll must have at least {Poll.MIN_OPTIONS} options.')
                        
                    if len(options) > Poll.MAX_OPTIONS:

                        raise ValidationError(f'A poll cannot have more than {Poll.MAX_OPTIONS} options.')

                return redirect('main:thread_detail', forum_name_slug=forum.slug, thread_title_slug=thread.slug)

            except ValidationError as e:

                if poll.pk:
                    
                    poll.delete()

                poll_form.add_error(None, e)

        context_dict = {
            'forum': forum,
            'thread': thread,
            'poll_form': poll_form,
            'option_formset': option_formset,
        }

        return render(request, 'main/add_poll.html', context_dict)

class SearchView(View):
    """
    Handle search queries to find matching articles and threads across the platform.

    Processes a search term provided via GET request, searches article titles, summaries, and content,
    as well as thread titles and topics, and displays the results on a dedicated search page.
    """

    def get(self, request, *args, **kwargs):
        """
        Process the search query and render the results page.

        Extracts the search term from the query string, performs case-insensitive searches on articles
        and threads, and returns a page with the matching results. If no query is provided, it returns
        empty result sets.

        Args:
            request: The HTTP request object containing GET parameters.
            *args: Variable length argument list (unused).
            **kwargs: Arbitrary keyword arguments (unused).

        Returns:
            HttpResponse: Rendered search_results.html template with search results.
        """
        
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

        context_dict = {
            'query': query,
            'articles': articles,
            'threads': threads,
        }

        return render(request, 'main/search_results.html', context_dict)

def get_category_list(max_results=0, contains=''):
    """
    Retrieve a list of categories, optionally filtered by a search term.

    Fetches all categories ordered by name, or filters them based on a provided term if specified.
    Limits the result set if a maximum number of results is provided.

    Args:
        max_results (int): Maximum number of categories to return (0 for unlimited).
        contains (str): Term to filter category names by (case-insensitive).

    Returns:
        QuerySet: A list of Category objects matching the criteria.
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
    Retrieve a list of forums, optionally filtered by a search term.

    Fetches all forums ordered by name, or filters them based on a provided term if specified.
    Limits the result set if a maximum number of results is provided.

    Args:
        max_results (int): Maximum number of forums to return (0 for unlimited).
        contains (str): Term to filter forum names by (case-insensitive).

    Returns:
        QuerySet: A list of Forum objects matching the criteria.
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
    Provide dynamic suggestions for categories and forums based on a partial search term.

    Handles AJAX requests to supply a list of up to 5 matching categories and forums as the user types.
    Returns rendered HTML snippets that can be used in an autocomplete or suggestion dropdown on the frontend.
    """

    def get(self, request):
        """
        Generate and return category and forum suggestions as HTML snippets via AJAX.

        Extracts the partial search term from the query string, fetches matching categories and forums
        (up to 5 each), renders them into HTML templates, and returns the results as a JSON response.

        Args:
            request: The HTTP request object containing the 'suggestion' GET parameter.

        Returns:
            JsonResponse: JSON object containing rendered HTML for categories and forums.
        """
    
        suggestion = request.GET.get('suggestion', '')

        category_list = get_category_list(max_results=5, contains=suggestion)

        forum_list = get_forum_list(max_results=5, contains=suggestion)

        categories_html = render_to_string('main/categories.html', {'categories': category_list, 'current_category': None})

        forums_html = render_to_string('main/forums.html', {'forums': forum_list, 'current_forum': None})

        return JsonResponse({'categories': categories_html, 'forums': forums_html})