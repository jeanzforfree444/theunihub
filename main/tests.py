import os
import importlib
from django.test import TestCase, Client
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.test.client import encode_multipart
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import mail
from django.db.models import Count
from unittest.mock import patch
import json
from django.contrib.auth.models import User
from main.models import UserProfile, Category, Forum, Article, Thread, Comment, Post, Poll, PollOption
from main.forms import UserProfileForm

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}THEUNIHUB TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class StructureTests(TestCase):

    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.main_app_dir = os.path.join(self.project_base_dir, 'main')

    def test_project_root_files(self):
        expected_files = [
            '.gitignore', 'bing.key', 'db.sqlite3', 'manage.py', 
            'population_script.py', 'README.md', 'secret.key', 'translator.key'
        ]
        for file_name in expected_files:
            file_exists = os.path.isfile(os.path.join(self.project_base_dir, file_name))
            self.assertTrue(file_exists, f"{FAILURE_HEADER}The {file_name} file is missing at the project root.{FAILURE_FOOTER}")

    def test_theunihub_directory(self):
        directory_exists = os.path.isdir(os.path.join(self.project_base_dir, 'theunihub'))
        expected_files = ['settings.py', 'urls.py', 'wsgi.py', '__init__.py']
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}Your theunihub directory does not seem to exist.{FAILURE_FOOTER}")
        for file_name in expected_files:
            file_exists = os.path.isfile(os.path.join(self.project_base_dir, 'theunihub', file_name))
            self.assertTrue(file_exists, f"{FAILURE_HEADER}The {file_name} file is missing in theunihub/.{FAILURE_FOOTER}")

    def test_main_app_directory(self):
        directory_exists = os.path.isdir(self.main_app_dir)
        expected_files = [
            'admin.py', 'apps.py', 'bing_search.py', 'context_processors.py', 'forms.py', 
            'models.py', 'tests.py', 'urls.py', 'views.py', '__init__.py'
        ]
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The main app directory does not exist.{FAILURE_FOOTER}")
        for file_name in expected_files:
            file_exists = os.path.isfile(os.path.join(self.main_app_dir, file_name))
            self.assertTrue(file_exists, f"{FAILURE_HEADER}The {file_name} file is missing in main/.{FAILURE_FOOTER}")

    def test_main_migrations_directory(self):
        migrations_dir = os.path.join(self.main_app_dir, 'migrations')
        directory_exists = os.path.isdir(migrations_dir)
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The migrations/ directory does not exist in main/.{FAILURE_FOOTER}")

    def test_main_templatetags_directory(self):
        templatetags_dir = os.path.join(self.main_app_dir, 'templatetags')
        directory_exists = os.path.isdir(templatetags_dir)
        expected_files = ['main_template_tags.py', '__init__.py']
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The templatetags/ directory does not exist in main/.{FAILURE_FOOTER}")
        for file_name in expected_files:
            file_exists = os.path.isfile(os.path.join(templatetags_dir, file_name))
            self.assertTrue(file_exists, f"{FAILURE_HEADER}The {file_name} file is missing in main/templatetags/.{FAILURE_FOOTER}")

    def test_is_main_app_configured(self):
        is_app_configured = 'main' in settings.INSTALLED_APPS
        self.assertTrue(is_app_configured, f"{FAILURE_HEADER}The main app is missing from your settings' INSTALLED_APPS list.{FAILURE_FOOTER}")

    def test_main_templates_directory(self):
        main_templates_dir = os.path.join(self.project_base_dir, 'templates', 'main')
        directory_exists = os.path.isdir(main_templates_dir)
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The templates/main directory does not exist at the project root.{FAILURE_FOOTER}")

    def test_main_template_files(self):
        main_templates_dir = os.path.join(self.project_base_dir, 'templates', 'main')
        directory_exists = os.path.isdir(main_templates_dir)
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The templates/main directory does not exist at the project root.{FAILURE_FOOTER}")
        expected_files = [
            'about.html', 'add_article.html', 'add_category.html', 'add_forum.html', 'add_poll.html', 'article.html', 'base.html',
            'categories.html', 'category.html', 'category_list.html', 'confirm_delete_account.html', 'contact.html', 'create_thread.html',
            'delete_article.html', 'delete_category.html', 'delete_comment.html', 'delete_forum.html', 'delete_post.html', 'delete_thread.html',
            'edit_article.html', 'edit_category.html', 'edit_comment.html', 'edit_forum.html', 'edit_post.html', 'edit_profile.html', 'edit_thread.html',
            'faqs.html', 'favourite_articles.html', 'forums.html', 'forum_list.html', 'index.html', 'list_users.html', 'mission_vision.html',
            'privacy.html', 'profile.html', 'profiles.html', 'profile_registration.html', 'saved_threads.html', 'search_results.html',
            'stats.html', 'terms.html', 'thread_detail.html', 'thread_list.html', 'values.html'
        ]
        for template_file in expected_files:
            file_exists = os.path.isfile(os.path.join(main_templates_dir, template_file))
            self.assertTrue(file_exists, f"{FAILURE_HEADER}The {template_file} template is missing in templates/main/.{FAILURE_FOOTER}")

    def test_registration_templates_directory(self):
        reg_templates_dir = os.path.join(self.project_base_dir, 'templates', 'registration')
        directory_exists = os.path.isdir(reg_templates_dir)
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The templates/registration directory does not exist at the project root.{FAILURE_FOOTER}")

    def test_reg_template_files(self):
        reg_templates_dir = os.path.join(self.project_base_dir, 'templates', 'registration')
        directory_exists = os.path.isdir(reg_templates_dir)
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The templates/registration directory does not exist at the project root.{FAILURE_FOOTER}")
        expected_files = [
            'login.html', 'logout.html', 'password_change_done.html', 'password_change_form.html',
            'registration_closed.html', 'registration_form.html'
        ]
        for template_file in expected_files:
            file_exists = os.path.isfile(os.path.join(reg_templates_dir, template_file))
            self.assertTrue(file_exists, f"{FAILURE_HEADER}The {template_file} template is missing in templates/registration/.{FAILURE_FOOTER}")

    def test_static_directory(self):
        static_dir = os.path.join(self.project_base_dir, 'static')
        directory_exists = os.path.isdir(static_dir)
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The static/ directory does not exist at the project root.{FAILURE_FOOTER}")
        subdirs_files = {
            'css': ['core.css', 'extra.css'],
            'fonts': ['Commissioner.ttf'],
            'images': ['logo.ico'],
            'js': [
                'add_poll.js', 'bing_translate.js', 'chart.js', 'jquery.js', 'like_dislike.js',
                'poll_vote.js', 'profile_registration.js', 'search_filter.js', 'user_posts.js'
            ]
        }
        for subdir, files in subdirs_files.items():
            subdir_exists = os.path.isdir(os.path.join(static_dir, subdir))
            self.assertTrue(subdir_exists, f"{FAILURE_HEADER}The static/{subdir}/ directory is missing.{FAILURE_FOOTER}")
            for file_name in files:
                file_exists = os.path.isfile(os.path.join(static_dir, subdir, file_name))
                self.assertTrue(file_exists, f"{FAILURE_HEADER}The static/{subdir}/{file_name} file is missing.{FAILURE_FOOTER}")

    def test_media_directory(self):
        media_dir = os.path.join(self.project_base_dir, 'media')
        directory_exists = os.path.isdir(media_dir)
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The media/ directory does not exist at the project root.{FAILURE_FOOTER}")
        subdirs = ['article_images', 'profile_pictures']
        for subdir in subdirs:
            subdir_exists = os.path.isdir(os.path.join(media_dir, subdir))
            self.assertTrue(subdir_exists, f"{FAILURE_HEADER}The media/{subdir}/ directory is missing.{FAILURE_FOOTER}")
        self.assertTrue(hasattr(settings, 'MEDIA_ROOT'), f"{FAILURE_HEADER}MEDIA_ROOT is not defined in settings.py.{FAILURE_FOOTER}")
        self.assertTrue(hasattr(settings, 'MEDIA_URL'), f"{FAILURE_HEADER}MEDIA_URL is not defined in settings.py.{FAILURE_FOOTER}")
        self.assertEqual(settings.MEDIA_ROOT, media_dir, f"{FAILURE_HEADER}MEDIA_ROOT does not point to the media/ directory.{FAILURE_FOOTER}")

    def test_settings_templates_config(self):
        templates_config = settings.TEMPLATES
        self.assertTrue(len(templates_config) > 0, f"{FAILURE_HEADER}TEMPLATES setting is not defined in settings.py.{FAILURE_FOOTER}")
        dirs = templates_config[0].get('DIRS', [])
        app_dirs_enabled = templates_config[0].get('APP_DIRS', False)
        self.assertTrue(app_dirs_enabled, f"{FAILURE_HEADER}APP_DIRS should be True in TEMPLATES settings to load app templates.{FAILURE_FOOTER}")

    def test_settings_static_config(self):
        self.assertTrue(hasattr(settings, 'STATIC_URL'), f"{FAILURE_HEADER}STATIC_URL is not defined in settings.py.{FAILURE_FOOTER}")
        self.assertEqual(settings.STATIC_URL, '/static/', f"{FAILURE_HEADER}STATIC_URL should be '/static/' in settings.py.{FAILURE_FOOTER}")
        self.assertTrue(hasattr(settings, 'STATICFILES_DIRS'), f"{FAILURE_HEADER}STATICFILES_DIRS is not defined in settings.py.{FAILURE_FOOTER}")
        expected_static_dir = os.path.join(self.project_base_dir, 'static')
        self.assertIn(expected_static_dir, settings.STATICFILES_DIRS, f"{FAILURE_HEADER}The static/ directory is not in STATICFILES_DIRS.{FAILURE_FOOTER}")

    def test_database_config(self):
        self.assertTrue(hasattr(settings, 'DATABASES'), f"{FAILURE_HEADER}DATABASES setting is not defined in settings.py.{FAILURE_FOOTER}")
        self.assertTrue('default' in settings.DATABASES, f"{FAILURE_HEADER}The 'default' database is not configured in DATABASES.{FAILURE_FOOTER}")

    def test_urls_inclusion(self):
        from theunihub.urls import urlpatterns
        main_urls_included = any(
            hasattr(pattern, 'app_name') and pattern.app_name == 'main'
            for pattern in urlpatterns
        )
        self.assertTrue(main_urls_included, f"{FAILURE_HEADER}The main app's URLs are not included in theunihub/urls.py.{FAILURE_FOOTER}")

class BaseTemplateTests(TestCase):

    def setUp(self):
        
        self.VALID_IMAGE = SimpleUploadedFile(
            name='default.jpg',
            content=open(os.path.join(settings.BASE_DIR, 'default.jpg'), 'rb').read(),
            content_type='image/jpg'
        )

        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            bio='Test bio',
            university='edinburgh',
            school='Test School',
            department='Test Department',
            degree='Test Degree',
            start_year=2025,
            profile_picture=self.VALID_IMAGE
        )

        self.category = Category.objects.create(name='Test Category', description='A test category')
        
        self.forum = Forum.objects.create(name='Test Forum', description='A test forum')
        
        self.article = Article.objects.create(
            category=self.category,
            title='Test Article',
            summary='Test summary',
            content='Test content',
            article_image=self.VALID_IMAGE,
            author=self.user
        )
        
        self.thread = Thread.objects.create(
            forum=self.forum,
            title='Test Thread',
            topic='Test topic',
            author=self.user
        )
        
        self.user_profile.favourite_articles.add(self.article)
        
        self.user_profile.saved_threads.add(self.thread)

    def tearDown(self):
        profile_pics_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pictures')
        article_images_dir = os.path.join(settings.MEDIA_ROOT, 'article_images')
        for directory in (profile_pics_dir, article_images_dir):
            if os.path.exists(directory):
                for filename in os.listdir(directory):
                    if filename.startswith('default'):
                        file_path = os.path.join(directory, filename)
                        if os.path.isfile(file_path):
                            os.remove(file_path)

    def test_for_home_hyperlink(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            '<a class="nav-link" href="/main/">Home</a>' in content or
            '<a class="nav-link" href="/main">Home</a>' in content,
            f"{FAILURE_HEADER}We couldn't find the hyperlink to /main/ in your index page response. It should be in the navigation bar.{FAILURE_FOOTER}"
        )
        response = self.client.get('/main/')
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Clicking the Home link did not return a 200 status.{FAILURE_FOOTER}")

    def test_for_about_hyperlink(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            '<a class="nav-link" href="/main/about/">About</a>' in content or
            '<a class="nav-link" href="/main/about">About</a>' in content,
            f"{FAILURE_HEADER}We couldn't find the hyperlink to /main/about/ in your index page response. It should be in the navigation bar.{FAILURE_FOOTER}"
        )
        response = self.client.get('/main/about/')
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Clicking the About link did not return a 200 status.{FAILURE_FOOTER}")

    def test_for_categories_hyperlink(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            '<a class="nav-link" href="/main/category/">Categories</a>' in content or
            '<a class="nav-link" href="/main/category">Categories</a>' in content,
            f"{FAILURE_HEADER}We couldn't find the hyperlink to /main/category/ in your index page response. It should be in the navigation bar.{FAILURE_FOOTER}"
        )
        response = self.client.get('/main/category/')
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Clicking the Categories link did not return a 200 status.{FAILURE_FOOTER}")

    def test_for_forums_hyperlink(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            '<a class="nav-link" href="/main/forum/">Forums</a>' in content or
            '<a class="nav-link" href="/main/forum">Forums</a>' in content,
            f"{FAILURE_HEADER}We couldn't find the hyperlink to /main/forum/ in your index page response. It should be in the navigation bar.{FAILURE_FOOTER}"
        )
        response = self.client.get('/main/forum/')
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Clicking the Forums link did not return a 200 status.{FAILURE_FOOTER}")

    def test_users_link_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            '<a class="nav-link" href="/main/users/">Users</a>' in content or
            '<a class="nav-link" href="/main/users">Users</a>' in content,
            f"{FAILURE_HEADER}We couldn't find the Users hyperlink when authenticated. It should be in the navigation bar.{FAILURE_FOOTER}"
        )
        response = self.client.get('/main/users/')
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Clicking the Users link did not return a 200 status for an authenticated user.{FAILURE_FOOTER}")
        self.client.logout()

    def test_users_link_not_authenticated(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertFalse(
            '<a class="nav-link" href="/main/users/">Users</a>' in content or
            '<a class="nav-link" href="/main/users">Users</a>' in content,
            f"{FAILURE_HEADER}The Users hyperlink should not be visible when not authenticated.{FAILURE_FOOTER}"
        )
        response = self.client.get('/main/users/')
        self.assertEqual(
            response.status_code, 302,
            f"{FAILURE_HEADER}Unauthenticated access to /main/users/ should redirect (302), not return a 200 status.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            response.url.startswith('/accounts/login/'),
            f"{FAILURE_HEADER}Unauthenticated access to /main/users/ should redirect to the login page.{FAILURE_FOOTER}"
        )
        
    def test_register_and_signin_links_not_authenticated(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            '<a class="nav-link" href="/accounts/register/">Register</a>' in content or
            '<a class="nav-link" href="/accounts/register">Register</a>' in content,
            f"{FAILURE_HEADER}We couldn't find the Register hyperlink when not authenticated. It should be in the navigation bar.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            '<a class="nav-link" href="/accounts/login/">Sign In</a>' in content or
            '<a class="nav-link" href="/accounts/login">Sign In</a>' in content,
            f"{FAILURE_HEADER}We couldn't find the Sign In hyperlink when not authenticated. It should be in the navigation bar.{FAILURE_FOOTER}"
        )
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Clicking the Register link did not return a 200 status.{FAILURE_FOOTER}")
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Clicking the Sign In link did not return a 200 status.{FAILURE_FOOTER}")

    def test_my_account_link_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            'href="/main/profile/testuser/"' in content or 'href="/main/profile/testuser"' in content,
            f"{FAILURE_HEADER}The profile URL (/main/profile/testuser/) is missing or incorrect in the navigation bar.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'My Account' in content,
            f"{FAILURE_HEADER}The 'My Account' text is missing from the navigation bar when authenticated.{FAILURE_FOOTER}"
        )
        response = self.client.get('/main/profile/testuser/')
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Clicking the My Account link did not return a 200 status.{FAILURE_FOOTER}")
        self.client.logout()

    def test_navbar_search_bar_functionality(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            '<form class="flex-grow-1 mx-1" action="/main/search/" method="get">' in content,
            f"{FAILURE_HEADER}The navbar search form is missing or incorrectly configured in the base template.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            '<input type="search" id="search-bar" class="form-control w-100" placeholder="Search by keyword..." name="q"' in content,
            f"{FAILURE_HEADER}The navbar search input field is missing or incorrect in the base template.{FAILURE_FOOTER}"
        )
        response = self.client.get('/main/search/', {'q': 'test'})
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Submitting a navbar search query did not return a 200 status.{FAILURE_FOOTER}")

    def test_sidebar_search_bar(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            '<input type="search" id="search-input" class="form-control ds-input" placeholder="Search by names..." />' in content,
            f"{FAILURE_HEADER}The sidebar search input field is missing or incorrect in the base template.{FAILURE_FOOTER}"
        )

    def test_sidebar_headings(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            '<p class="sidebar-heading">' in content and 'Categories' in content,
            f"{FAILURE_HEADER}The Categories heading is missing from the sidebar in the base template.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            '<p class="sidebar-heading">' in content and 'Forums' in content,
            f"{FAILURE_HEADER}The Forums heading is missing from the sidebar in the base template.{FAILURE_FOOTER}"
        )

    def test_sidebar_dynamic_content(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            'Test Category' in content,
            f"{FAILURE_HEADER}The category list in the sidebar is not rendering correctly (missing 'Test Category'). Check the get_category_list template tag.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'Test Forum' in content,
            f"{FAILURE_HEADER}The forum list in the sidebar is not rendering correctly (missing 'Test Forum'). Check the get_forum_list template tag.{FAILURE_FOOTER}"
        )

    def test_sidebar_authenticated_content(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            '<p class="sidebar-heading">Favourites Articles</p>' in content,
            f"{FAILURE_HEADER}The Favourites Articles heading is missing from the sidebar when authenticated.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            '<p class="sidebar-heading">Saved Threads</p>' in content,
            f"{FAILURE_HEADER}The Saved Threads heading is missing from the sidebar when authenticated.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'Test Article' in content,
            f"{FAILURE_HEADER}The favourite articles list in the sidebar is not rendering correctly (missing 'Test Article'). Check the get_favourites_list template tag.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'Test Thread' in content,
            f"{FAILURE_HEADER}The saved threads list in the sidebar is not rendering correctly (missing 'Test Thread'). Check the get_saved_list template tag.{FAILURE_FOOTER}"
        )
        self.client.logout()

    def test_sidebar_staff_links(self):
        self.user.is_staff = True
        self.user.save()
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            '<a href="/main/add_category/"><span data-feather="plus-circle"></span></a>' in content,
            f"{FAILURE_HEADER}The Add Category link is missing for staff users in the sidebar.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            '<a href="/main/add_forum/"><span data-feather="plus-circle"></span></a>' in content,
            f"{FAILURE_HEADER}The Add Forum link is missing for staff users in the sidebar.{FAILURE_FOOTER}"
        )
        response = self.client.get('/main/add_category/')
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Clicking the Add Category link did not return a 200 status for a staff user.{FAILURE_FOOTER}")
        response = self.client.get('/main/add_forum/')
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Clicking the Add Forum link did not return a 200 status for a staff user.{FAILURE_FOOTER}")
        self.client.logout()
        self.user.is_staff = False
        self.user.save()

    def test_navbar_brand(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            '<a class="navbar-brand p-2" href="/main/"><span class="company-logo"><i>TheUniHub</i></span></a>' in content,
            f"{FAILURE_HEADER}The navbar brand link to /main/ with 'TheUniHub' is missing or incorrect.{FAILURE_FOOTER}"
        )
        response = self.client.get('/main/')
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Clicking the navbar brand link did not return a 200 status.{FAILURE_FOOTER}")

    def test_footer_links(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            '<a href="/main/privacy/">Privacy</a>' in content or
            '<a href="/main/privacy">Privacy</a>' in content,
            f"{FAILURE_HEADER}The Privacy link is missing from the footer.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            '<a href="/main/terms/">Terms</a>' in content or
            '<a href="/main/terms">Terms</a>' in content,
            f"{FAILURE_HEADER}The Terms link is missing from the footer.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            '<a href="/main/faqs/">FAQs</a>' in content or
            '<a href="/main/faqs">FAQs</a>' in content,
            f"{FAILURE_HEADER}The FAQs link is missing from the footer.{FAILURE_FOOTER}"
        )
        response = self.client.get('/main/privacy/')
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Clicking the Privacy link did not return a 200 status.{FAILURE_FOOTER}")
        response = self.client.get('/main/terms/')
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Clicking the Terms link did not return a 200 status.{FAILURE_FOOTER}")
        response = self.client.get('/main/faqs/')
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Clicking the FAQs link did not return a 200 status.{FAILURE_FOOTER}")

    def test_footer_stats_link_staff(self):
        self.user.is_staff = True
        self.user.save()
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            '<a href="/main/stats/">Statistics</a>' in content or
            '<a href="/main/stats">Statistics</a>' in content,
            f"{FAILURE_HEADER}The Statistics link is missing for staff users in the footer.{FAILURE_FOOTER}"
        )
        response = self.client.get('/main/stats/')
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Clicking the Statistics link did not return a 200 status for a staff user.{FAILURE_FOOTER}")
        self.client.logout()
        self.user.is_staff = False
        self.user.save()

    def test_footer_back_to_top(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            '<a href="#"><span data-feather="arrow-up"></span> Back to top</a>' in content,
            f"{FAILURE_HEADER}The Back to top link is missing from the footer.{FAILURE_FOOTER}"
        )

    def test_static_file_loading(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            '<link rel="icon" href="/static/images/logo.ico">' in content,
            f"{FAILURE_HEADER}Static file loading seems broken; the favicon link is missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_language_selector(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            '<select id="language-select" class="form-control form-control-sm">' in content,
            f"{FAILURE_HEADER}The language selector dropdown is missing from the base template.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            '<option value="en">English</option>' in content,
            f"{FAILURE_HEADER}The English option is missing from the language selector.{FAILURE_FOOTER}"
        )

class IndexTemplateTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user_profile = UserProfile.objects.create(user=self.user, university='edinburgh')

        Category.objects.all().delete()
        for i in range(6):
            views = 100 - i * 10
            Category.objects.create(name=f'Category {i}', slug=f'category-{i}', views=views)
        self.category = Category.objects.get(slug='category-0')

        Article.objects.all().delete()
        for i in range(6):
            points = 50 - i * 5
            Article.objects.create(
                category=self.category, title=f'Article {i}', slug=f'article-{i}',
                author=self.user, content=f'Content {i}', points=points, views=200 - i * 10,
                related_university='edinburgh' if i < 3 else None
            )
        self.article = Article.objects.get(slug='article-0')

        Comment.objects.all().delete()
        self.comment = Comment.objects.create(
            article=self.article, author=self.user, content='Test comment',
            written_on=timezone.now(),
            edited_on=timezone.now() + timezone.timedelta(days=1)
        )

        Forum.objects.all().delete()
        Thread.objects.all().delete()
        Post.objects.all().delete()
        self.forum = Forum.objects.create(name='Test Forum', slug='test-forum')
        self.thread = Thread.objects.create(
            forum=self.forum, title='Test Thread', slug='test-thread',
            author=self.user, topic='Test topic',
            started_on=timezone.now(),
            updated_on=timezone.now() + timezone.timedelta(days=1),
            related_university='edinburgh'
        )
        Post.objects.create(thread=self.thread, author=self.user, content='Test post', written_on=timezone.now())
        self.thread = Thread.objects.filter(id=self.thread.id).annotate(post_count=Count('post')).first()

    def tearDown(self):
        profile_pics_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pictures')
        article_images_dir = os.path.join(settings.MEDIA_ROOT, 'article_images')
        for directory in (profile_pics_dir, article_images_dir):
            if os.path.exists(directory):
                for filename in os.listdir(directory):
                    if filename.startswith('default'):
                        file_path = os.path.join(directory, filename)
                        if os.path.isfile(file_path):
                            os.remove(file_path)

    def test_index_page_loads(self):
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Index page did not load successfully.{FAILURE_FOOTER}")
        content = response.content.decode()
        self.assertTrue(
            'main/index.html' in [t.name for t in response.templates],
            f"{FAILURE_HEADER}Index page is not using main/index.html template.{FAILURE_FOOTER}"
        )

    def test_title_block(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    Home' in content,
            f"{FAILURE_HEADER}Title block does not contain 'TheUniHub - Home'.{FAILURE_FOOTER}"
        )

    def test_jumbotron_heading(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            '<h1 class="jumbotron-heading">Home</h1>' in content,
            f"{FAILURE_HEADER}Jumbotron heading 'Home' is missing.{FAILURE_FOOTER}"
        )

    def test_jumbotron_subheading(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            'Welcome back to <span class="company-name"><i>TheUniHub</i></span>' in content,
            f"{FAILURE_HEADER}Welcome text is missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_unauthenticated_user_greeting(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            'Hello! If you haven\'t already, please <a href="/accounts/register/">register</a> or <a href="/accounts/login/">login</a>' in content,
            f"{FAILURE_HEADER}Unauthenticated user greeting is incorrect or missing.{FAILURE_FOOTER}"
        )

    def test_authenticated_user_greeting(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            'Hello, testuser!' in content,
            f"{FAILURE_HEADER}Authenticated user greeting does not include username.{FAILURE_FOOTER}"
        )
        self.assertFalse(
            'please <a href="{% url \'registration_register\' %}">register</a>' in content,
            f"{FAILURE_HEADER}Authenticated user should not see register link.{FAILURE_FOOTER}"
        )
        self.client.logout()

    def test_categories_section(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            '<h2>Most Visited Categories</h2>' in content,
            f"{FAILURE_HEADER}'Most Visited Categories' header is missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            f'<a href="/main/category/{self.category.slug}/">{self.category.name}</a> ({self.category.views} views)' in content,
            f"{FAILURE_HEADER}Category list does not display correctly.{FAILURE_FOOTER}"
        )

    def test_articles_section(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            '<h2>Most Helpful Articles</h2>' in content,
            f"{FAILURE_HEADER}'Most Helpful Articles' header is missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            f'<a href="/main/category/{self.article.category.slug}/article/{self.article.slug}/">{self.article.title}</a>  ({self.article.points} points)' in content,
            f"{FAILURE_HEADER}Article list does not display correctly.{FAILURE_FOOTER}"
        )

    def test_comments_section(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            '<h2>Latest Comments</h2>' in content,
            f"{FAILURE_HEADER}'Latest Comments' header is missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            '<strong>testuser:</strong>' in content,
            f"{FAILURE_HEADER}Comment author is missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'Test comment' in content,
            f"{FAILURE_HEADER}Comment content is missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            '<a href="/main/category/category-0/article/article-0/">Article 0</a>' in content,
            f"{FAILURE_HEADER}Comment article link is missing.{FAILURE_FOOTER}"
        )

    def test_threads_section(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            '<h2>Trending Discussions</h2>' in content,
            f"{FAILURE_HEADER}'Trending Discussions' header is missing.{FAILURE_FOOTER}"
        )
        expected_thread = f'<strong>{self.thread.forum.name}:</strong> <a href="/main/forum/{self.thread.forum.slug}/thread/{self.thread.slug}/">{self.thread.title}</a> - {self.thread.post_count} posts'
        self.assertTrue(
            expected_thread in content,
            f"{FAILURE_HEADER}Thread list does not display correctly.{FAILURE_FOOTER}"
        )

    def test_university_feed_unauthenticated(self):
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertFalse(
            'University of Edinburgh Feed' in content,
            f"{FAILURE_HEADER}University feed should not appear for unauthenticated users.{FAILURE_FOOTER}"
        )

    def test_university_feed_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            'University of Edinburgh Feed' in content,
            f"{FAILURE_HEADER}University feed header is missing for authenticated user.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            '<a href="https://www.ed.ac.uk/" target="_blank" class="btn btn-primary btn-sm">\n                                        <span data-feather="external-link"></span> Visit Official Website\n                                    </a>' in content,
            f"{FAILURE_HEADER}University website link is missing or incorrect.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            f'<a href="/main/category/{self.article.category.slug}/article/{self.article.slug}/">{self.article.title}</a>' in content,
            f"{FAILURE_HEADER}University article is missing from feed.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            f'<a href="/main/forum/{self.thread.forum.slug}/thread/{self.thread.slug}/">{self.thread.title}</a> - {self.thread.post_count} posts' in content,
            f"{FAILURE_HEADER}University thread is missing from feed.{FAILURE_FOOTER}"
        )
        self.client.logout()

    def test_empty_data_handling(self):
        Category.objects.all().delete()
        Article.objects.all().delete()
        Comment.objects.all().delete()
        Thread.objects.all().delete()
        Forum.objects.all().delete()
        Post.objects.all().delete()
        UserProfile.objects.all().delete()
        
        response = self.client.get(reverse('main:index'))
        content = response.content.decode()
        self.assertTrue(
            'There are no categories yet.' in content,
            f"{FAILURE_HEADER}Empty categories message is missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'There are no articles in any categories yet. You can start the first by finding a category and clicking the "<span data-feather="edit"></span> Add Article" button.' in content,
            f"{FAILURE_HEADER}Empty articles message is missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'There are no comments on any articles yet. You can start the first by finding an article, typing your comment and clicking the "<span data-feather="edit"></span> Comment" button.' in content,
            f"{FAILURE_HEADER}Empty comments message is missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'There are no threads in any forums yet. You can start the first by finding a forum and clicking the "<span data-feather="edit"></span> Start Thread" button.' in content,
            f"{FAILURE_HEADER}Empty threads message is missing.{FAILURE_FOOTER}"
        )

class AboutTemplateTests(TestCase):
    
    def setUp(self):
        
        self.VALID_IMAGE = SimpleUploadedFile(
            name='default.jpg',
            content=open(os.path.join(settings.BASE_DIR, 'default.jpg'), 'rb').read(),
            content_type='image/jpg'
        )
        
        self.client = Client()
        
        self.team_data = [
            ('aaronhxx_1', 'Aaron', 'Hughes', 'Founder - Built TheUniHub from scratch.'),
            ('phoebe6504', 'Phoebe', 'Smith', 'Developer - Code wizard.'),
            ('euan_galloway', 'Euan', 'Galloway', 'Marketer - Spreads the word.'),
            ('urangoo123', 'Urangoo', 'Bat', 'SysAdmin - Keeps servers humming.'),
        ]
        
        for username, first_name, last_name, bio in self.team_data:
            
            user = User.objects.create(username=username)
            
            UserProfile.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                bio=bio,
                profile_picture=self.VALID_IMAGE
            )

    def tearDown(self):
        profile_pics_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pictures')
        if os.path.exists(profile_pics_dir):
            for filename in os.listdir(profile_pics_dir):
                if filename.startswith('default'):
                    file_path = os.path.join(profile_pics_dir, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)

    def test_about_page_loads(self):
        response = self.client.get(reverse('main:about'))
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}About page did not load successfully.{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'main/about.html', f"{FAILURE_HEADER}About page is not using main/about.html template.{FAILURE_FOOTER}")

    def test_title_block(self):
        response = self.client.get(reverse('main:about'))
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    About Us' in content,
            f"{FAILURE_HEADER}Title block does not contain 'TheUniHub - About Us'.{FAILURE_FOOTER}"
        )

    def test_jumbotron_heading(self):
        response = self.client.get(reverse('main:about'))
        content = response.content.decode()
        self.assertTrue(
            '<h1 class="jumbotron-heading">About Us</h1>' in content,
            f"{FAILURE_HEADER}Jumbotron heading 'About Us' is missing.{FAILURE_FOOTER}"
        )

    def test_jumbotron_subheading(self):
        response = self.client.get(reverse('main:about'))
        content = response.content.decode()
        self.assertTrue(
            'All about the people behind <span class="company-name"><i>TheUniHub</i></span>' in content,
            f"{FAILURE_HEADER}Jumbotron subheading is missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_visit_counter(self):
        response = self.client.get(reverse('main:about'))
        content = response.content.decode()
        self.assertTrue(
            'You have visited our website 1 time.' in content,
            f"{FAILURE_HEADER}First visit counter incorrect.{FAILURE_FOOTER}"
        )

    def test_team_section(self):
        response = self.client.get(reverse('main:about'))
        content = response.content.decode()
        self.assertTrue(
            '<h5>Our Team</h5>' in content,
            f"{FAILURE_HEADER}Team heading missing.{FAILURE_FOOTER}"
        )
        for username, first_name, last_name, bio in self.team_data:
            full_name = f"{first_name} {last_name}"
            self.assertTrue(
                f'<a href="/main/profile/{username}/">{full_name}</a>' in content,
                f"{FAILURE_HEADER}Team member {full_name} link missing.{FAILURE_FOOTER}"
            )
            self.assertTrue(
                bio in content,
                f"{FAILURE_HEADER}Bio for {full_name} missing.{FAILURE_FOOTER}"
            )
            self.assertTrue(
                f'<img src="{settings.MEDIA_URL}profile_pictures/default.jpg' in content,
                f"{FAILURE_HEADER}Profile picture for {full_name} missing.{FAILURE_FOOTER}"
            )

    def test_empty_team_section(self):
        UserProfile.objects.all().delete()
        response = self.client.get(reverse('main:about'))
        content = response.content.decode()
        self.assertTrue(
            '<h5>Our Team</h5>' in content,
            f"{FAILURE_HEADER}Team heading missing with no members.{FAILURE_FOOTER}"
        )
        self.assertFalse(
            '<div class="col-md-6 mb-3">' in content,
            f"{FAILURE_HEADER}Team member divs present when empty.{FAILURE_FOOTER}"
        )

    def test_mission_section(self):
        response = self.client.get(reverse('main:about'))
        content = response.content.decode()
        self.assertTrue(
            '<h5>Our Mission</h5>' in content,
            f"{FAILURE_HEADER}Mission heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'To provide a platform for university students' in content,
            f"{FAILURE_HEADER}Mission text missing.{FAILURE_FOOTER}"
        )

    def test_vision_section(self):
        response = self.client.get(reverse('main:about'))
        content = response.content.decode()
        self.assertTrue(
            '<h5>The Vision</h5>' in content,
            f"{FAILURE_HEADER}Vision heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'To become the go-to resource' in content,
            f"{FAILURE_HEADER}Vision text missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            '<a href="/main/mission_vision/">Our Mission, The Vision</a>' in content,
            f"{FAILURE_HEADER}Vision link missing.{FAILURE_FOOTER}"
        )

    def test_values_section(self):
        response = self.client.get(reverse('main:about'))
        content = response.content.decode()
        self.assertTrue(
            '<h5>Our Values</h5>' in content,
            f"{FAILURE_HEADER}Values heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            '<a href="/main/values/">Values</a>' in content,
            f"{FAILURE_HEADER}Values link missing.{FAILURE_FOOTER}"
        )
        for value in ['Support', 'Integrity', 'Accessibility', 'Growth', 'Transparency']:
            self.assertTrue(
                f'<strong>{value}</strong>' in content,
                f"{FAILURE_HEADER}Value {value} missing.{FAILURE_FOOTER}"
            )

    def test_partners_section(self):
        response = self.client.get(reverse('main:about'))
        content = response.content.decode()
        self.assertTrue(
            '<h5>Our Partners</h5>' in content,
            f"{FAILURE_HEADER}Partners heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'We are proud to be partnered' in content,
            f"{FAILURE_HEADER}Partners text missing.{FAILURE_FOOTER}"
        )
        partners = [
            ('UCAS', 'https://www.ucas.com/'),
            ('National Union of Students (NUS)', 'https://www.nus.org.uk/'),
            ('British Council', 'https://www.britishcouncil.org/'),
            ('Universities UK', 'https://www.universitiesuk.ac.uk/'),
            ('Quality Assurance Agency for Higher Education (QAA)', 'https://www.qaa.ac.uk/'),
            ('Scholarship Portal', 'https://www.scholarshipportal.com/')
        ]
        for partner, url in partners:
            self.assertTrue(
                f'<a href="{url}" target="_blank">{partner}</a>' in content,
                f"{FAILURE_HEADER}Partner {partner} link missing.{FAILURE_FOOTER}"
            )

    def test_sponsors_section(self):
        response = self.client.get(reverse('main:about'))
        content = response.content.decode()
        self.assertTrue(
            '<h5>Our Sponsors</h5>' in content,
            f"{FAILURE_HEADER}Sponsors heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'We are grateful to be sponsored' in content,
            f"{FAILURE_HEADER}Sponsors text missing.{FAILURE_FOOTER}"
        )
        sponsors = [
            ('Student Finance England', 'https://studentfinance.campaign.gov.uk/'),
            ('Student Finance Scotland', 'https://www.saas.gov.uk/'),
            ('UNiDAYS', 'https://www.myunidays.com/'),
            ('Student Beans', 'https://www.studentbeans.com/uk/'),
            ('Chegg', 'https://www.chegg.com/'),
            ('Coursera', 'https://www.coursera.org/')
        ]
        for sponsor, url in sponsors:
            self.assertTrue(
                f'<a href="{url}" target="_blank">{sponsor}</a>' in content,
                f"{FAILURE_HEADER}Sponsor {sponsor} link missing.{FAILURE_FOOTER}"
            )

class PrivacyTemplateTests(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_privacy_page_loads(self):
        response = self.client.get(reverse('main:privacy'))
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Privacy page did not load successfully.{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'main/privacy.html', f"{FAILURE_HEADER}Privacy page is not using main/privacy.html template.{FAILURE_FOOTER}")

    def test_title_block(self):
        response = self.client.get(reverse('main:privacy'))
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    Privacy Policy' in content,
            f"{FAILURE_HEADER}Title block does not contain 'TheUniHub - Privacy Policy'.{FAILURE_FOOTER}"
        )

    def test_jumbotron_heading(self):
        response = self.client.get(reverse('main:privacy'))
        content = response.content.decode()
        self.assertTrue(
            '<h1 class="jumbotron-heading">Privacy Policy</h1>' in content,
            f"{FAILURE_HEADER}Jumbotron heading 'Privacy Policy' is missing.{FAILURE_FOOTER}"
        )

    def test_jumbotron_subheading(self):
        response = self.client.get(reverse('main:privacy'))
        content = response.content.decode()
        self.assertTrue(
            'This is the privacy policy for <span class="company-name"><i>TheUniHub</i></span>.' in content,
            f"{FAILURE_HEADER}Jumbotron subheading is missing or incorrect.{FAILURE_FOOTER}"
        )
    
    def test_jumbotron_info(self):
        response = self.client.get(reverse('main:privacy'))
        content = response.content.decode()
        self.assertTrue(
            'This page has been put together by our legal team.' in content,
            f"{FAILURE_HEADER}Jumbotron info text is missing.{FAILURE_FOOTER}"
        )

    def test_privacy_policy_section(self):
        response = self.client.get(reverse('main:privacy'))
        content = response.content.decode()
        self.assertTrue(
            '<h5>Privacy Policy</h5>' in content,
            f"{FAILURE_HEADER}Privacy Policy heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'This privacy policy sets out how <span class="company-name"><i>TheUniHub</i></span> uses and protects any information' in content,
            f"{FAILURE_HEADER}Privacy policy intro text missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            '<span class="company-name"><i>TheUniHub</i></span> is committed to ensuring that your privacy is protected.' in content,
            f"{FAILURE_HEADER}Privacy commitment text missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'This policy is effective from 1st January 2020.' in content,
            f"{FAILURE_HEADER}Policy effective date missing.{FAILURE_FOOTER}"
        )

    def test_what_we_collect_section(self):
        response = self.client.get(reverse('main:privacy'))
        content = response.content.decode()
        self.assertTrue(
            '<h6>What we collect</h6>' in content,
            f"{FAILURE_HEADER}'What we collect' heading missing.{FAILURE_FOOTER}"
        )
        items = [
            'Name and profile picture',
            'Contact information including email address',
            'Demographic information such as university details, preferences and interests',
            'Other information relevant to customer surveys and/or offers'
        ]
        for item in items:
            self.assertTrue(
                f'<li class="list-group-item">{item}</li>' in content,
                f"{FAILURE_HEADER}Collected item '{item}' missing.{FAILURE_FOOTER}"
            )

    def test_what_we_do_with_info_section(self):
        response = self.client.get(reverse('main:privacy'))
        content = response.content.decode()
        self.assertTrue(
            '<h6>What we do with the information we gather</h6>' in content,
            f"{FAILURE_HEADER}'What we do with info' heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'We require this information to understand your needs and provide you with a better service' in content,
            f"{FAILURE_HEADER}Info purpose text missing.{FAILURE_FOOTER}"
        )
        items = [
            'Internal record keeping.',
            'We may use the information to improve our products and services.',
            'We may periodically send promotional emails about new products, special offers or other information which we think you may find interesting using the email address which you have provided.',
            'From time to time, we may also use your information to contact you for market research purposes. We may contact you by email, phone, fax or mail. We may use the information to customise the website according to your interests.'
        ]
        for item in items:
            self.assertTrue(
                f'<li class="list-group-item">{item}</li>' in content,
                f"{FAILURE_HEADER}Info usage item '{item}' missing.{FAILURE_FOOTER}"
            )

    def test_security_section(self):
        response = self.client.get(reverse('main:privacy'))
        content = response.content.decode()
        self.assertTrue(
            '<h6>Security</h6>' in content,
            f"{FAILURE_HEADER}Security heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'We are committed to ensuring that your information is secure.' in content,
            f"{FAILURE_HEADER}Security commitment text missing.{FAILURE_FOOTER}"
        )

    def test_cookies_section(self):
        response = self.client.get(reverse('main:privacy'))
        content = response.content.decode()
        self.assertTrue(
            '<h6>How we use cookies</h6>' in content,
            f"{FAILURE_HEADER}Cookies heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'A cookie is a small file which asks permission to be placed on your computer\'s hard drive.' in content,
            f"{FAILURE_HEADER}Cookie definition text missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'We use traffic log cookies to identify which pages are being used.' in content,
            f"{FAILURE_HEADER}Traffic log cookies text missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'Overall, cookies help us provide you with a better website' in content,
            f"{FAILURE_HEADER}Cookies benefit text missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'You can choose to accept or decline cookies.' in content,
            f"{FAILURE_HEADER}Cookie control text missing.{FAILURE_FOOTER}"
        )

    def test_links_to_other_websites_section(self):
        response = self.client.get(reverse('main:privacy'))
        content = response.content.decode()
        self.assertTrue(
            '<h6>Links to other websites</h6>' in content,
            f"{FAILURE_HEADER}'Links to other websites' heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'Our website may contain links to other websites of interest.' in content,
            f"{FAILURE_HEADER}External links disclaimer text missing.{FAILURE_FOOTER}"
        )

    def test_controlling_personal_info_section(self):
        response = self.client.get(reverse('main:privacy'))
        content = response.content.decode()
        self.assertTrue(
            '<h6>Controlling your personal information</h6>' in content,
            f"{FAILURE_HEADER}'Controlling personal info' heading missing.{FAILURE_FOOTER}"
        )
        items = [
            'Whenever you are asked to fill in a form on the website, look for the box that you can click to indicate that you do not want the information to be used by anybody for direct marketing purposes',
            'If you have previously agreed to us using your personal information for direct marketing purposes, you may change your mind at any time by checking our <a href="/main/contact/">contact</a> information.'
        ]
        for item in items:
            self.assertTrue(
                f'<li class="list-group-item">{item}</li>' in content if 'contact' not in item else item in content,
                f"{FAILURE_HEADER}Control option '{item}' missing or incorrect.{FAILURE_FOOTER}"
            )
        self.assertTrue(
            '<a href="/main/contact/">contact</a>' in content,
            f"{FAILURE_HEADER}Contact link in control section missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'We will not sell, distribute or lease your personal information to third parties unless we have your permission or are required by law to do so.' in content,
            f"{FAILURE_HEADER}Personal info distribution policy missing.{FAILURE_FOOTER}"
        )

class TermsTemplateTests(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_terms_page_loads(self):
        response = self.client.get(reverse('main:terms'))
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Terms page did not load successfully.{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'main/terms.html', f"{FAILURE_HEADER}Terms page is not using main/terms.html template.{FAILURE_FOOTER}")

    def test_title_block(self):
        response = self.client.get(reverse('main:terms'))
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    Terms and Conditions' in content,
            f"{FAILURE_HEADER}Title block does not contain 'TheUniHub - Terms and Conditions'.{FAILURE_FOOTER}"
        )

    def test_jumbotron_heading(self):
        response = self.client.get(reverse('main:terms'))
        content = response.content.decode()
        self.assertTrue(
            '<h1 class="jumbotron-heading">Terms and Conditions</h1>' in content,
            f"{FAILURE_HEADER}Jumbotron heading 'Terms and Conditions' is missing.{FAILURE_FOOTER}"
        )

    def test_jumbotron_subheading(self):
        response = self.client.get(reverse('main:terms'))
        content = response.content.decode()
        self.assertTrue(
            'These are the terms and conditions for <span class="company-name"><i>TheUniHub</i></span>.' in content,
            f"{FAILURE_HEADER}Jumbotron subheading is missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_jumbotron_info(self):
        response = self.client.get(reverse('main:terms'))
        content = response.content.decode()
        self.assertTrue(
            'This page has been put together by our legal team.' in content,
            f"{FAILURE_HEADER}Jumbotron info text is missing.{FAILURE_FOOTER}"
        )

    def test_terms_and_conditions_section(self):
        response = self.client.get(reverse('main:terms'))
        content = response.content.decode()
        self.assertTrue(
            '<h5>Terms and Conditions</h5>' in content,
            f"{FAILURE_HEADER}Terms and Conditions heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'These terms and conditions govern your use of <span class="company-name"><i>TheUniHub</i></span>.' in content,
            f"{FAILURE_HEADER}Terms agreement text missing.{FAILURE_FOOTER}"
        )

    def test_use_of_website_section(self):
        response = self.client.get(reverse('main:terms'))
        content = response.content.decode()
        self.assertTrue(
            '<h6>Use of the Website</h6>' in content,
            f"{FAILURE_HEADER}'Use of the Website' heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'By using <span class="company-name"><i>TheUniHub</i></span>, you agree to:' in content,
            f"{FAILURE_HEADER}Website use intro text missing.{FAILURE_FOOTER}"
        )
        items = [
            'Use the website only for lawful purposes.',
            'Not post or share any harmful, abusive, or illegal content.',
            'Respect other users and engage in constructive discussions.',
            'Not attempt to gain unauthorised access to any part of the website.'
        ]
        for item in items:
            self.assertTrue(
                f'<li class="list-group-item">{item}</li>' in content,
                f"{FAILURE_HEADER}Website use item '{item}' missing.{FAILURE_FOOTER}"
            )

    def test_account_registration_section(self):
        response = self.client.get(reverse('main:terms'))
        content = response.content.decode()
        self.assertTrue(
            '<h6>Account Registration</h6>' in content,
            f"{FAILURE_HEADER}'Account Registration' heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'Some features of <span class="company-name"><i>TheUniHub</i></span> may require you to create an account.' in content,
            f"{FAILURE_HEADER}Account registration intro text missing.{FAILURE_FOOTER}"
        )
        items = [
            'Provide accurate and up-to-date information.',
            'Keep your account credentials secure and confidential.',
            'Be responsible for all activities under your account.'
        ]
        for item in items:
            self.assertTrue(
                f'<li class="list-group-item">{item}</li>' in content,
                f"{FAILURE_HEADER}Account registration item '{item}' missing.{FAILURE_FOOTER}"
            )

    def test_intellectual_property_section(self):
        response = self.client.get(reverse('main:terms'))
        content = response.content.decode()
        self.assertTrue(
            '<h6>Intellectual Property</h6>' in content,
            f"{FAILURE_HEADER}'Intellectual Property' heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'All content on <span class="company-name"><i>TheUniHub</i></span>, including text, graphics, logos, and software' in content,
            f"{FAILURE_HEADER}Intellectual property text missing.{FAILURE_FOOTER}"
        )

    def test_termination_section(self):
        response = self.client.get(reverse('main:terms'))
        content = response.content.decode()
        self.assertTrue(
            '<h6>Termination</h6>' in content,
            f"{FAILURE_HEADER}'Termination' heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'We reserve the right to suspend or terminate your access to <span class="company-name"><i>TheUniHub</i></span>' in content,
            f"{FAILURE_HEADER}Termination text missing.{FAILURE_FOOTER}"
        )

    def test_limitation_of_liability_section(self):
        response = self.client.get(reverse('main:terms'))
        content = response.content.decode()
        self.assertTrue(
            '<h6>Limitation of Liability</h6>' in content,
            f"{FAILURE_HEADER}'Limitation of Liability' heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            '<span class="company-name"><i>TheUniHub</i></span> is not responsible for any direct, indirect, or consequential damages' in content,
            f"{FAILURE_HEADER}Liability disclaimer text missing.{FAILURE_FOOTER}"
        )

    def test_third_party_links_section(self):
        response = self.client.get(reverse('main:terms'))
        content = response.content.decode()
        self.assertTrue(
            '<h6>Third-Party Links</h6>' in content,
            f"{FAILURE_HEADER}'Third-Party Links' heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'Our website may contain links to external websites.' in content,
            f"{FAILURE_HEADER}Third-party links disclaimer text missing.{FAILURE_FOOTER}"
        )

    def test_changes_to_terms_section(self):
        response = self.client.get(reverse('main:terms'))
        content = response.content.decode()
        self.assertTrue(
            '<h6>Changes to These Terms</h6>' in content,
            f"{FAILURE_HEADER}'Changes to These Terms' heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'We may update these terms from time to time.' in content,
            f"{FAILURE_HEADER}Terms update notice text missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            '<a href="/main/contact/">contact</a>' in content,
            f"{FAILURE_HEADER}Contact link in changes section missing.{FAILURE_FOOTER}"
        )

    def test_governing_law_section(self):
        response = self.client.get(reverse('main:terms'))
        content = response.content.decode()
        self.assertTrue(
            '<h6>Governing Law</h6>' in content,
            f"{FAILURE_HEADER}'Governing Law' heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'These terms and conditions are governed by and construed in accordance with the laws of the United Kingdom.' in content,
            f"{FAILURE_HEADER}Governing law text missing.{FAILURE_FOOTER}"
        )

class MissionVisionTemplateTests(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_mission_vision_page_loads(self):
        response = self.client.get(reverse('main:mission_vision'))
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Mission Vision page did not load successfully.{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'main/mission_vision.html', f"{FAILURE_HEADER}Mission Vision page is not using main/mission_vision.html template.{FAILURE_FOOTER}")

    def test_title_block(self):
        response = self.client.get(reverse('main:mission_vision'))
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    Our Mission, The Vision' in content,
            f"{FAILURE_HEADER}Title block does not contain 'TheUniHub - Our Mission, The Vision'.{FAILURE_FOOTER}"
        )

    def test_jumbotron_heading(self):
        response = self.client.get(reverse('main:mission_vision'))
        content = response.content.decode()
        self.assertTrue(
            '<h1 class="jumbotron-heading">Our Mission, The Vision</h1>' in content,
            f"{FAILURE_HEADER}Jumbotron heading 'Our Mission, The Vision' is missing.{FAILURE_FOOTER}"
        )

    def test_jumbtron_subheading(self):
        response = self.client.get(reverse('main:mission_vision'))
        content = response.content.decode()
        self.assertTrue(
            'The missions and visions at the core of <span class="company-name"><i>TheUniHub</i></span>.' in content,
            f"{FAILURE_HEADER}Jumbotron subheading is missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_jumbtron_info(self):
        response = self.client.get(reverse('main:mission_vision'))
        content = response.content.decode()
        self.assertTrue(
            'This page outlines the mission and vision that drive us to support university students and the community.' in content,
            f"{FAILURE_HEADER}Jumbotron info text is missing.{FAILURE_FOOTER}"
        )

    def test_mission_section(self):
        response = self.client.get(reverse('main:mission_vision'))
        content = response.content.decode()
        self.assertTrue(
            '<h5>Our Mission</h5>' in content,
            f"{FAILURE_HEADER}'Our Mission' heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'At <i>TheUniHub</i>, our mission is to create a thriving community for university students' in content,
            f"{FAILURE_HEADER}Mission purpose text missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'We are committed to improving the student experience by offering a wide range of services' in content,
            f"{FAILURE_HEADER}Mission commitment text missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'Our mission is to empower students to take control of their futures' in content,
            f"{FAILURE_HEADER}Mission empowerment text missing.{FAILURE_FOOTER}"
        )
        items = [
            'Comprehensive academic support, including tutoring, workshops, and study resources to enhance learning.',
            'A supportive mental health environment with resources for counselling, stress management, and peer support groups.',
            'Career services to help students transition smoothly into the workforce, offering CV reviews, interview preparation, and internship opportunities.',
            'Financial advice, scholarships, and budgeting resources to ensure students can manage their finances throughout their studies.',
            'Building strong social networks by connecting students with similar interests, creating an inclusive and welcoming community.'
        ]
        for item in items:
            self.assertTrue(
                f'<li class="list-group-item">{item}</li>' in content,
                f"{FAILURE_HEADER}Mission item '{item}' missing.{FAILURE_FOOTER}"
            )

    def test_vision_section(self):
        response = self.client.get(reverse('main:mission_vision'))
        content = response.content.decode()
        self.assertTrue(
            '<h5>The Vision</h5>' in content,
            f"{FAILURE_HEADER}'The Vision' heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'We envision a future where all university students, regardless of background, have access to the tools and resources' in content,
            f"{FAILURE_HEADER}Vision access text missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'We see <i>TheUniHub</i> becoming an essential part of the university experience' in content,
            f"{FAILURE_HEADER}Vision essential text missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'The vision is to ensure that every student, from the moment they step foot on campus, has the support they need' in content,
            f"{FAILURE_HEADER}Vision thrive text missing.{FAILURE_FOOTER}"
        )
        items = [
            'A supportive platform for students to access all the resources they need in one place, from academic materials to personal growth resources.',
            'A thriving community that fosters collaboration, innovation, and mutual support among students from all disciplines.',
            'Educational and career opportunities through partnerships with employers, alumni, and professional networks to give students a head start after graduation.',
            'A mental health initiative that ensures every student has the support they need, reducing stress and promoting overall well-being.',
            'An inclusive, accessible space where every student feels heard and valued, regardless of their personal circumstances.'
        ]
        for item in items:
            self.assertTrue(
                f'<li class="list-group-item">{item}</li>' in content,
                f"{FAILURE_HEADER}Vision item '{item}' missing.{FAILURE_FOOTER}"
            )

    def test_student_life_section(self):
        response = self.client.get(reverse('main:mission_vision'))
        content = response.content.decode()
        self.assertTrue(
            '<h5>What We Will Do to Make Student Life Better</h5>' in content,
            f"{FAILURE_HEADER}'What We Will Do to Make Student Life Better' heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'At <i>TheUniHub</i>, we are dedicated to enhancing student life by offering a comprehensive range of services' in content,
            f"{FAILURE_HEADER}Student life dedication text missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'Our commitment is to create a nurturing environment where students feel supported, inspired, and motivated' in content,
            f"{FAILURE_HEADER}Student life commitment text missing.{FAILURE_FOOTER}"
        )
        items = [
            'Provide academic resources such as study guides, peer tutoring, and exam prep workshops to help students achieve their academic goals.',
            'Create mental health support services, including online counselling sessions, stress-relieving activities, and well-being workshops.',
            'Offer tailored career advice, helping students craft professional CVs, prepare for interviews, and connect with potential employers through job fairs and internship programmes.',
            'Launch social initiatives that bring students together, such as virtual clubs, interest-based groups, and mentorship programmes for students to form meaningful connections.',
            'Provide easy access to financial aid and budgeting advice to help students manage their finances and reduce the financial stress of university life.',
            'Establish partnerships with local businesses and service providers to offer students exclusive discounts, further enhancing their university experience.'
        ]
        for item in items:
            self.assertTrue(
                f'<li class="list-group-item">{item}</li>' in content,
                f"{FAILURE_HEADER}Student life item '{item}' missing.{FAILURE_FOOTER}"
            )

    def test_empowering_collaboration_subsection(self):
        response = self.client.get(reverse('main:mission_vision'))
        content = response.content.decode()
        self.assertTrue(
            '<h6>Empowering Students Through Collaboration</h6>' in content,
            f"{FAILURE_HEADER}'Empowering Students Through Collaboration' heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'Collaboration is key to our mission. We will work closely with student unions, university staff, and faculty members' in content,
            f"{FAILURE_HEADER}Collaboration text missing.{FAILURE_FOOTER}"
        )

    def test_long_term_support_subsection(self):
        response = self.client.get(reverse('main:mission_vision'))
        content = response.content.decode()
        self.assertTrue(
            '<h6>Building a Long-Term Student Support Network</h6>' in content,
            f"{FAILURE_HEADER}'Building a Long-Term Student Support Network' heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'Our vision extends beyond the duration of a student\'s degree.' in content,
            f"{FAILURE_HEADER}Long-term support text missing.{FAILURE_FOOTER}"
        )

    def test_promise_to_community_subsection(self):
        response = self.client.get(reverse('main:mission_vision'))
        content = response.content.decode()
        self.assertTrue(
            '<h6>Our Promise to the Community</h6>' in content,
            f"{FAILURE_HEADER}'Our Promise to the Community' heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'At <i>TheUniHub</i>, we promise to always put the well-being and success of students first.' in content,
            f"{FAILURE_HEADER}Promise to community text missing.{FAILURE_FOOTER}"
        )

class ValuesTemplateTests(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_values_page_loads(self):
        response = self.client.get(reverse('main:values'))
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Values page did not load successfully.{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'main/values.html', f"{FAILURE_HEADER}Values page is not using main/values.html template.{FAILURE_FOOTER}")

    def test_title_block(self):
        response = self.client.get(reverse('main:values'))
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    Our Values' in content,
            f"{FAILURE_HEADER}Title block does not contain 'TheUniHub - Our Values'.{FAILURE_FOOTER}"
        )

    def test_jumbotron_heading(self):
        response = self.client.get(reverse('main:values'))
        content = response.content.decode()
        self.assertTrue(
            '<h1 class="jumbotron-heading">Our Values</h1>' in content,
            f"{FAILURE_HEADER}Jumbotron heading 'Our Values' is missing.{FAILURE_FOOTER}"
        )

    def test_jumbotron_subheading(self):
        response = self.client.get(reverse('main:values'))
        content = response.content.decode()
        self.assertTrue(
            'These values are the foundations of <span class="company-name"><i>TheUniHub</i></span>.' in content,
            f"{FAILURE_HEADER}Jumbotron subheading is missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_jumbotron_info(self):
        response = self.client.get(reverse('main:values'))
        content = response.content.decode()
        self.assertTrue(
            'This page has been put together by our management team.' in content,
            f"{FAILURE_HEADER}Jumbotron info text is missing.{FAILURE_FOOTER}"
        )

    def test_values_section(self):
        response = self.client.get(reverse('main:values'))
        content = response.content.decode()
        self.assertTrue(
            '<h5>Our Values</h5>' in content,
            f"{FAILURE_HEADER}'Our Values' heading missing.{FAILURE_FOOTER}"
        )
        values = [
            ('Respect', 'We believe that respect is the cornerstone of a strong academic and social community.'),
            ('Integrity', 'Honesty and ethical behaviour are central to everything we do.'),
            ('Support', 'University life can be challenging, and no student should have to navigate it alone.'),
            ('Quality', 'Excellence is our benchmark.'),
            ('Transparency', 'We believe in openness and honesty in all our decisions, policies, and communications.')
        ]
        for value, text in values:
            self.assertTrue(
                f'<h6>{value}</h6>' in content,
                f"{FAILURE_HEADER}'{value}' subheading missing.{FAILURE_FOOTER}"
            )
            self.assertTrue(
                text in content,
                f"{FAILURE_HEADER}'{value}' description text missing.{FAILURE_FOOTER}"
            )

    def test_your_rights_section(self):
        response = self.client.get(reverse('main:values'))
        content = response.content.decode()
        self.assertTrue(
            '<h5>Your Rights</h5>' in content,
            f"{FAILURE_HEADER}'Your Rights' heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'At <span class="company-name"><i>TheUniHub</i></span>, we are committed to protecting your rights as a student' in content,
            f"{FAILURE_HEADER}Your Rights intro text missing.{FAILURE_FOOTER}"
        )

    def test_rights_subsections(self):
        response = self.client.get(reverse('main:values'))
        content = response.content.decode()
        rights = [
            ('Right to Access', 'You have the right to access and benefit from the resources available on'),
            ('Right to Privacy', 'Your privacy matters to us.'),
            ('Right to Expression', 'We believe in freedom of expression within a respectful and constructive framework.'),
            ('Right to Security', 'A safe and secure platform is our priority.'),
            ('Right to Support', 'University life can be overwhelming, and we are here to help.'),
            ('Right to Control Your Content', 'You maintain ownership of the content you contribute to'),
            ('Right to Transparency', 'We are committed to keeping our policies, updates, and decisions clear and understandable.')
        ]
        for right, text in rights:
            self.assertTrue(
                f'<h6>{right}</h6>' in content,
                f"{FAILURE_HEADER}'{right}' subheading missing.{FAILURE_FOOTER}"
            )
            self.assertTrue(
                text in content,
                f"{FAILURE_HEADER}'{right}' description text missing.{FAILURE_FOOTER}"
            )
        self.assertTrue(
            '<a href="/main/contact/">contact</a>' in content,
            f"{FAILURE_HEADER}Contact link in 'Right to Transparency' missing.{FAILURE_FOOTER}"
        )

class FAQsTemplateTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_faqs_page_loads(self):
        response = self.client.get(reverse('main:faqs'))
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}FAQs page did not load successfully.{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'main/faqs.html', f"{FAILURE_HEADER}FAQs page is not using main/faqs.html template.{FAILURE_FOOTER}")

    def test_title_block(self):
        response = self.client.get(reverse('main:faqs'))
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    Frequently Asked Questions (FAQs)' in content,
            f"{FAILURE_HEADER}Title block does not contain 'TheUniHub - Frequently Asked Questions (FAQs)'.{FAILURE_FOOTER}"
        )

    def test_jumbotron_heading(self):
        response = self.client.get(reverse('main:faqs'))
        content = response.content.decode()
        self.assertTrue(
            '<h1 class="jumbotron-heading">Frequently Asked Questions (FAQs)</h1>' in content,
            f"{FAILURE_HEADER}Jumbotron heading 'Frequently Asked Questions (FAQs)' is missing.{FAILURE_FOOTER}"
        )

    def test_jumbotron_subheading(self):
        response = self.client.get(reverse('main:faqs'))
        content = response.content.decode()
        self.assertTrue(
            'Answers to common questions about <span class="company-name"><i>TheUniHub</i></span>.' in content,
            f"{FAILURE_HEADER}Jumbotron subheading is missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_jumbotron_info(self):
        response = self.client.get(reverse('main:faqs'))
        content = response.content.decode()
        self.assertTrue(
            'You should be able to find everything you need to make best use of the website.' in content,
            f"{FAILURE_HEADER}Jumbotron info text is missing.{FAILURE_FOOTER}"
        )

    def test_general_questions_section(self):
        response = self.client.get(reverse('main:faqs'))
        content = response.content.decode()
        self.assertTrue(
            '<h5>General Questions</h5>' in content,
            f"{FAILURE_HEADER}'General Questions' heading missing.{FAILURE_FOOTER}"
        )
        qa_pairs = [
            ('What is TheUniHub?', '<span class="company-name"><i>TheUniHub</i></span> is an online platform designed to provide students'),
            ('Is TheUniHub affiliated with any universities?', 'No, we are an independent platform that aims to provide unbiased information'),
            ('What are the benefits of becoming a member?', 'Non-members have access to a large portion of <span class="company-name"><i>TheUniHub</i></span>')
        ]
        for question, answer in qa_pairs:
            self.assertTrue(
                f'<h6>{question}</h6>' in content,
                f"{FAILURE_HEADER}'{question}' subheading missing.{FAILURE_FOOTER}"
            )
            self.assertTrue(
                answer in content,
                f"{FAILURE_HEADER}'{question}' answer text missing.{FAILURE_FOOTER}"
            )

    def test_registration_accounts_section(self):
        response = self.client.get(reverse('main:faqs'))
        content = response.content.decode()
        self.assertTrue(
            '<h5>Registration and Accounts</h5>' in content,
            f"{FAILURE_HEADER}'Registration and Accounts' heading missing.{FAILURE_FOOTER}"
        )
        qa_pairs = [
            ('How do I create an account?', 'You can sign up by clicking the “Register” button'),
            ('Is there a cost to using TheUniHub?', 'No, our platform is completely free to use.'),
            ('I forgot my password. What should I do?', 'Click on “Forgot Password?” on the login page'),
            ('Can I delete my account?', 'Yes, you can delete your account from your profile settings.'),
            ('Can I edit my profile?', 'Yes, click on the "Edit profile" button on your profile page')
        ]
        for question, answer in qa_pairs:
            self.assertTrue(
                f'<h6>{question}</h6>' in content,
                f"{FAILURE_HEADER}'{question}' subheading missing.{FAILURE_FOOTER}"
            )
            self.assertTrue(
                answer in content,
                f"{FAILURE_HEADER}'{question}' answer text missing.{FAILURE_FOOTER}"
            )
        self.assertTrue(
            '<a href="/main/contact/">contact</a>' in content,
            f"{FAILURE_HEADER}Contact link in 'Can I delete my account?' missing.{FAILURE_FOOTER}"
        )

    def test_website_functionality_section(self):
        response = self.client.get(reverse('main:faqs'))
        content = response.content.decode()
        self.assertTrue(
            '<h5>Website Functionality</h5>' in content,
            f"{FAILURE_HEADER}'Website Functionality' heading missing.{FAILURE_FOOTER}"
        )
        qa_pairs = [
            ('What are categories, and how do they work?', 'Categories help group articles based on specific topics.'),
            ('Can I create or edit categories?', 'No, only staff members can create or modify categories.'),
            ('How do articles work on this website?', 'Articles provide informative content on various topics.'),
            ('Can I write my own articles?', 'Currently, only approved contributors and staff can write articles.'),
            ('How do comments work on articles?', 'You can comment on articles by typing your response in the comment section'),
            ('Can I edit or delete my comments?', 'Yes, you can edit or delete your comments within 24 hours of posting.'),
            ('What are forums, and how do they work?', 'Forums help organise threads based on specific topics.'),
            ('Can I create/edit forums?', 'No, only users registered as staff are able to create forums.'),
            ('How do threads work on this website?', 'Threads provide a discussion space across a wide range of topics.'),
            ('How do I start threads?', 'Make your way to the forums section, choose a forum'),
            ('Can I edit/delete my threads?', 'Yes, you can edit your threads within 24 hours of starting.'),
            ('How do posts work on threads?', 'You can post on threads by typing your response in the post section'),
            ('Can I edit/delete my posts?', 'Yes, you can edit your posts within 24 hours of posting.'),
            ('How do I report inappropriate content?', 'Every post has a “Report” button.'),
            ('How does the search functionality work?', 'There are two search bars on the website:'),
            ('How do I favourite articles?', 'You can favourite an article by clicking the "<span data-feather="plus-circle"></span> Favourite" button'),
            ('How do I save threads?', 'To save a thread for later, click the "<span data-feather="plus-circle"></span> Save" button')
        ]
        for question, answer in qa_pairs:
            self.assertTrue(
                f'<h6>{question}</h6>' in content,
                f"{FAILURE_HEADER}'{question}' subheading missing.{FAILURE_FOOTER}"
            )
            self.assertTrue(
                answer in content,
                f"{FAILURE_HEADER}'{question}' answer text missing.{FAILURE_FOOTER}"
            )
        for q in ['Can I create or edit categories?', 'Can I write my own articles?', 'Can I create/edit forums?']:
            self.assertTrue(
                '<a href="/main/contact/">contact</a>' in content or '<a href="/main/contact/">reach out</a>' in content,
                f"{FAILURE_HEADER}Contact link in '{q}' missing.{FAILURE_FOOTER}"
            )
        search_items = [
            '<strong>Navigation bar search:</strong> This search bar is designed for finding articles and threads based on keywords.',
            '<strong>Sidebar search:</strong> This search bar helps users find forum and category names.'
        ]
        for item in search_items:
            self.assertTrue(
                f'<li>{item}</li>' in content,
                f"{FAILURE_HEADER}Search functionality item '{item}' missing.{FAILURE_FOOTER}"
            )

    def test_support_contact_section(self):
        response = self.client.get(reverse('main:faqs'))
        content = response.content.decode()
        self.assertTrue(
            '<h5>Support and Contact</h5>' in content,
            f"{FAILURE_HEADER}'Support and Contact' heading missing.{FAILURE_FOOTER}"
        )
        qa_pairs = [
            ('How can I contact TheUniHub support?', 'You can reach our support team through the <a href="/main/contact/">contact</a> page'),
            ('Do you have a form feature?', 'Yes, our form is available during business hours.')
        ]
        for question, answer in qa_pairs:
            self.assertTrue(
                f'<h6>{question}</h6>' in content,
                f"{FAILURE_HEADER}'{question}' subheading missing.{FAILURE_FOOTER}"
            )
            self.assertTrue(
                answer in content,
                f"{FAILURE_HEADER}'{question}' answer text missing.{FAILURE_FOOTER}"
            )

class ContactTemplateTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.client.get(reverse('main:contact'))
        mail.outbox = []

    def test_contact_page_loads(self):
        response = self.client.get(reverse('main:contact'))
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Contact page did not load successfully.{FAILURE_FOOTER}")
        self.assertTemplateUsed(response, 'main/contact.html', f"{FAILURE_HEADER}Contact page is not using main/contact.html template.{FAILURE_FOOTER}")

    def test_title_block(self):
        response = self.client.get(reverse('main:contact'))
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    Contact Us' in content,
            f"{FAILURE_HEADER}Title block does not contain 'TheUniHub - Contact Us'.{FAILURE_FOOTER}"
        )

    def test_jumbotron_heading(self):
        response = self.client.get(reverse('main:contact'))
        content = response.content.decode()
        self.assertTrue(
            '<h1 class="jumbotron-heading">Contact Us</h1>' in content,
            f"{FAILURE_HEADER}Jumbotron heading 'Contact Us' is missing.{FAILURE_FOOTER}"
        )
    
    def test_jumbotron_subheading(self):
        response = self.client.get(reverse('main:contact'))
        content = response.content.decode()
        self.assertTrue(
            'The contact information for <span class="company-name"><i>TheUniHub</i></span>.' in content,
            f"{FAILURE_HEADER}Jumbotron subheading is missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_jumbotron_info(self):
        response = self.client.get(reverse('main:contact'))
        content = response.content.decode()
        self.assertTrue(
            'Please be aware that during times of high demand, contact timings may be delayed by up to an additional 10 working days' in content,
            f"{FAILURE_HEADER}Jumbotron info text is missing.{FAILURE_FOOTER}"
        )

    def test_our_information_section(self):
        response = self.client.get(reverse('main:contact'))
        content = response.content.decode()
        self.assertTrue(
            '<h5>Our Information</h5>' in content,
            f"{FAILURE_HEADER}'Our Information' heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'If you have any questions, concerns, or suggestions, feel free to get in touch with us.' in content,
            f"{FAILURE_HEADER}Intro text missing.{FAILURE_FOOTER}"
        )
        items = [
            ('Email:', f'<strong>Email:</strong> <a href="mailto:info@theunihub.co.uk">info@theunihub.co.uk</a>'),
            ('Phone:', '<strong>Phone:</strong> <a href="tel:+441632960961">+44 1632 960961</a>'),
            ('Address:', '<strong>Address:</strong> TheUniHub Ltd., 3rd Floor, 52 High Street, London, EC2A 2BS, United Kingdom.'),
            ('Opening Hours:', '<strong>Opening Hours:</strong><br>\n                                Monday to Friday: 9:00 AM - 6:00 PM (GMT)<br>\n                                Saturday: 10:00 AM - 4:00 PM (GMT)<br>\n                                Sunday: Closed')
        ]
        for label, html in items:
            self.assertTrue(
                html in content,
                f"{FAILURE_HEADER}Contact info item '{label}' missing or incorrect.{FAILURE_FOOTER}"
            )

    def test_contact_form_section(self):
        response = self.client.get(reverse('main:contact'))
        content = response.content.decode()
        self.assertTrue(
            '<h5>Contact Form</h5>' in content,
            f"{FAILURE_HEADER}'Contact Form' heading missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'You can also fill out the contact form below, and our team will get back to you as soon as possible' in content,
            f"{FAILURE_HEADER}Form intro text missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            '<form action="#" method="post">' in content,
            f"{FAILURE_HEADER}Form tag missing.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'name="csrfmiddlewaretoken"' in content,
            f"{FAILURE_HEADER}CSRF token missing in form.{FAILURE_FOOTER}"
        )
        fields = [
            ('name', '<input type="text" class="form-control" id="name" name="name" value="" required>'),
            ('email', '<input type="email" class="form-control" id="email" name="email" value="" required>'),
            ('message', '<textarea class="form-control" id="message" name="message" rows="5" required></textarea>')
        ]
        for field_name, html in fields:
            self.assertTrue(
                html in content,
                f"{FAILURE_HEADER}Form field '{field_name}' missing or incorrect.{FAILURE_FOOTER}"
            )
        self.assertTrue(
            '<button type="submit" class="btn btn-primary btn-sm">' in content,
            f"{FAILURE_HEADER}Submit button missing.{FAILURE_FOOTER}"
        )

    def test_form_submission_success(self):
        form_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'message': 'This is a test message.'
        }
        response = self.client.post(reverse('main:contact'), data=form_data, follow=True)
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Form submission did not return 200.{FAILURE_FOOTER}")

        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertTrue(
            any(msg.message == 'Your message has been sent successfully!' and msg.tags == 'success' for msg in messages_list),
            f"{FAILURE_HEADER}Success message not displayed after form submission.{FAILURE_FOOTER}"
        )
        content = response.content.decode()
        self.assertTrue(
            '<div class="alert alert-success">' in content,
            f"{FAILURE_HEADER}Success alert not rendered.{FAILURE_FOOTER}"
        )

        self.assertEqual(len(mail.outbox), 1, f"{FAILURE_HEADER}Email was not logged to outbox.{FAILURE_FOOTER}")
        email = mail.outbox[0]
        self.assertEqual(email.subject, 'New message from John Doe', f"{FAILURE_HEADER}Email subject incorrect.{FAILURE_FOOTER}")
        self.assertEqual(email.to, [settings.CONTACT_EMAIL], f"{FAILURE_HEADER}Email not sent to CONTACT_EMAIL.{FAILURE_FOOTER}")
        self.assertIn('Message from: John Doe', email.body, f"{FAILURE_HEADER}Email body missing name.{FAILURE_FOOTER}")
        self.assertIn('Email: john.doe@example.com', email.body, f"{FAILURE_HEADER}Email body missing sender email.{FAILURE_FOOTER}")
        self.assertIn('This is a test message.', email.body, f"{FAILURE_HEADER}Email body missing message.{FAILURE_FOOTER}")

        self.assertTrue('value="John Doe"' in content, f"{FAILURE_HEADER}Name field not repopulated.{FAILURE_FOOTER}")
        self.assertTrue('value="john.doe@example.com"' in content, f"{FAILURE_HEADER}Email field not repopulated.{FAILURE_FOOTER}")
        self.assertTrue('This is a test message.' in content, f"{FAILURE_HEADER}Message field not repopulated.{FAILURE_FOOTER}")

    def test_form_submission_email_failure(self):
        with patch('main.views.send_mail') as mock_send_mail:
            mock_send_mail.side_effect = Exception("SMTP error")
            form_data = {
                'name': 'John Doe',
                'email': 'john.doe@example.com',
                'message': 'This is a test message.'
            }
            response = self.client.post(reverse('main:contact'), data=form_data, follow=True)
            content = response.content.decode()
            self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Form submission with email failure did not return 200.{FAILURE_FOOTER}")
            self.assertTrue(
                'Something went wrong. Please try again later.' in content,
                f"{FAILURE_HEADER}Error message not displayed when email fails.{FAILURE_FOOTER}"
            )
            self.assertEqual(len(mail.outbox), 0, f"{FAILURE_HEADER}Email outbox should be empty on failure.{FAILURE_FOOTER}")

    def test_form_submission_whitespace_only(self):
        form_data = {
            'name': '   ',
            'email': 'john.doe@example.com',
            'message': 'This is a test message.'
        }
        response = self.client.post(reverse('main:contact'), data=form_data, follow=True)
        content = response.content.decode()
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Form submission with missing fields did not return 200.{FAILURE_FOOTER}")
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertFalse(
            any(msg.message == 'Your message has been sent successfully!' for msg in messages_list),
            f"{FAILURE_HEADER}Success message appeared despite whitespace-only fields.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'All fields are required.' in content,
            f"{FAILURE_HEADER}Error message not displayed for whitespace-only name.{FAILURE_FOOTER}"
        )
        self.assertEqual(len(mail.outbox), 0, f"{FAILURE_HEADER}Email was sent despite whitespace-only name.{FAILURE_FOOTER}")

    def test_form_submission_missing_fields(self):
        form_data = {
            'name': '',
            'email': 'john.doe@example.com',
            'message': 'This is a test message.'
        }
        response = self.client.post(reverse('main:contact'), data=form_data, follow=True)
        content = response.content.decode()
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Form submission with missing fields did not return 200.{FAILURE_FOOTER}")
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertFalse(
            any(msg.message == 'Your message has been sent successfully!' for msg in messages_list),
            f"{FAILURE_HEADER}Success message appeared despite missing fields.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'All fields are required.' in content,
            f"{FAILURE_HEADER}Error message not displayed for whitespace-only name.{FAILURE_FOOTER}"
        )
        self.assertEqual(len(mail.outbox), 0, f"{FAILURE_HEADER}Email was sent despite missing fields.{FAILURE_FOOTER}")

class StatisticsTemplateTests(TestCase):
    
    def setUp(self):

        self.VALID_IMAGE = SimpleUploadedFile(
            name='default.jpg',
            content=open(os.path.join(settings.BASE_DIR, 'default.jpg'), 'rb').read(),
            content_type='image/jpg'
        )

        self.client = Client()

        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            bio='Test bio',
            university='edinburgh',
            school='Test School',
            department='Test Department',
            degree='Test Degree',
            start_year=2025,
            profile_picture=self.VALID_IMAGE
        )
        
        self.staff_user = User.objects.create_user(username='staffuser', password='staffpass123', is_staff=True)
        self.user_profile = UserProfile.objects.create(
            user=self.staff_user,
            first_name='Test',
            last_name='User',
            bio='Test bio',
            university='edinburgh',
            school='Test School',
            department='Test Department',
            degree='Test Degree',
            start_year=2025,
            profile_picture=self.VALID_IMAGE
        )
        
        self.category1 = Category.objects.create(name='Tech', description='Tech category', views=150, points=120, slug='tech')
        self.category2 = Category.objects.create(name='Science', description='Science category', slug='science')
        
        self.article1 = Article.objects.create(
            title='Test Article 1',
            summary='Test article',
            slug='test-article-1',
            category=self.category1,
            author=self.user,
            views=100,
            points=50,
            created_on=timezone.now(),
            updated_on=timezone.now()
        )
        
        self.article2 = Article.objects.create(
            title='Test Article 2',
            summary='Test article',
            slug='test-article-2',
            category=self.category2,
            author=self.user,
            views=200,
            points=75,
            created_on=timezone.now(),
            updated_on=timezone.now()
        )
        
        self.comment = Comment.objects.create(
            article=self.article1,
            author=self.user,
            content='Test comment',
            written_on=timezone.now()
        )
        
        self.forum = Forum.objects.create(name='General', slug='general')
        self.thread = Thread.objects.create(
            forum=self.forum,
            title='Test Thread',
            topic='Test thread',
            slug='test-thread',
            author=self.user,
            started_on=timezone.now(),
            updated_on=timezone.now()
        )
        
        self.post = Post.objects.create(
            thread=self.thread,
            author=self.user,
            content='Test post',
            written_on=timezone.now()
        )

    def test_stats_view_access_denied_for_non_staff(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:show_stats'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:index'))

    def test_stats_view_access_for_staff(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:show_stats'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/stats.html')

    def test_title_block(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:show_stats'))
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    Statistics' in content,
            f"{FAILURE_HEADER}Title block does not contain 'TheUniHub - Statistics'.{FAILURE_FOOTER}"
        )

    def test_jumbotron_heading(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:show_stats'))
        content = response.content.decode()
        self.assertTrue(
            '<h1 class="jumbotron-heading">Statistics</h1>' in content,
            f"{FAILURE_HEADER}Jumbotron heading 'Statistics' is missing.{FAILURE_FOOTER}"
        )
    
    def test_jumbotron_subheading(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:show_stats'))
        content = response.content.decode()
        self.assertTrue(
            'The statistics behind <span class="company-name"><i>TheUniHub</i></span>.' in content,
            f"{FAILURE_HEADER}Jumbotron subheading is missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_jumbotron_info(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:show_stats'))
        content = response.content.decode()
        self.assertTrue(
            'Here is information about views and points for categories, articles, forums, and threads as well as a breakdown of our users.' in content,
            f"{FAILURE_HEADER}Jumbotron info text is missing.{FAILURE_FOOTER}"
        )

    def test_stats_context_data(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:show_stats'))
        
        self.assertEqual(response.context['total_categories'], 2)
        self.assertEqual(response.context['total_articles'], 2)
        self.assertEqual(response.context['total_comments'], 1)
        self.assertEqual(response.context['total_users'], 2)
        self.assertEqual(response.context['total_forums'], 1)
        self.assertEqual(response.context['total_threads'], 1)
        self.assertEqual(response.context['total_posts'], 1)
        self.assertEqual(response.context['total_points'], 125)
        self.assertEqual(response.context['total_views'], 300)

        category_stats = response.context['category_stats']
        self.assertEqual(category_stats['Tech']['articles'], 1)
        self.assertEqual(category_stats['Tech']['points'], 50)
        self.assertEqual(category_stats['Tech']['views'], 100)
        self.assertEqual(category_stats['Science']['articles'], 1)
        self.assertEqual(category_stats['Science']['points'], 75)
        self.assertEqual(category_stats['Science']['views'], 200)

        forum_stats = response.context['forum_stats']
        self.assertEqual(forum_stats['General']['threads'], 1)
        self.assertEqual(forum_stats['General']['posts'], 1)

        self.assertEqual(json.loads(response.context['category_names']), ['Science', 'Tech'])
        self.assertEqual(json.loads(response.context['category_points']), [75, 50])
        self.assertEqual(json.loads(response.context['category_views']), [200, 100])

    def test_stats_template_renders_chart(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:show_stats'))
        
        self.assertContains(response, '<canvas id="categoryChart"')
        
        self.assertContains(response, '<div id="categoryPointsData"')
        self.assertContains(response, '<div id="categoryViewsData"')
        self.assertContains(response, '<div id="categoryNamesData"')
        
        self.assertContains(response, json.dumps([75, 50]))
        self.assertContains(response, json.dumps([200, 100]))
        self.assertContains(response, json.dumps(['Science', 'Tech']))

    def test_stats_view_no_data(self):
        Category.objects.all().delete()
        Article.objects.all().delete()
        Comment.objects.all().delete()
        Forum.objects.all().delete()
        Thread.objects.all().delete()
        Post.objects.all().delete()
        
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:show_stats'))
        
        self.assertEqual(response.context['total_categories'], 0)
        self.assertEqual(response.context['total_articles'], 0)
        self.assertEqual(response.context['total_comments'], 0)
        self.assertEqual(response.context['total_forums'], 0)
        self.assertEqual(response.context['total_threads'], 0)
        self.assertEqual(response.context['total_posts'], 0)
        self.assertEqual(response.context['total_points'], 0)
        self.assertEqual(response.context['total_views'], 0)
        
        self.assertEqual(response.context['category_stats'], {})
        self.assertEqual(response.context['forum_stats'], {})
        self.assertEqual(json.loads(response.context['category_names']), [])
        self.assertEqual(json.loads(response.context['category_points']), [])
        self.assertEqual(json.loads(response.context['category_views']), [])

    def test_javascript_chart_loading(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:show_stats'))
        content = response.content.decode()
        self.assertTrue('<script src="/static/js/chart.js" defer></script>' in content, "")

class RegistrationTemplateTests(TestCase):
    
    def setUp(self):

        self.VALID_IMAGE = SimpleUploadedFile(
            name='default.jpg',
            content=open(os.path.join(settings.BASE_DIR, 'default.jpg'), 'rb').read(),
            content_type='image/jpg'
        )

        self.client = Client()
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='testuser@example.com'
        )

    def tearDown(self):
        profile_pics_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pictures')
        if os.path.exists(profile_pics_dir):
            for filename in os.listdir(profile_pics_dir):
                if filename.startswith('default'):
                    file_path = os.path.join(profile_pics_dir, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)

    def test_registration_access_unauthenticated(self):
        response = self.client.get(reverse('registration_register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/registration_form.html')

    def test_registration_redirect_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('registration_register'))
        self.assertEqual(response.status_code, 302)

    def test_registration_title_block(self):
        response = self.client.get(reverse('registration_register'))
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    Register' in content,
            f"{FAILURE_HEADER}Title block does not contain 'TheUniHub - Register'.{FAILURE_FOOTER}"
        )

    def test_registration_jumbotron_heading(self):
        response = self.client.get(reverse('registration_register'))
        content = response.content.decode()
        self.assertTrue(
            '<h1 class="jumbotron-heading">Register Here</h1>' in content,
            f"{FAILURE_HEADER}Jumbotron heading 'Register Here' is missing.{FAILURE_FOOTER}"
        )

    def test_registration_jumbotron_subheading(self):
        response = self.client.get(reverse('registration_register'))
        content = response.content.decode()
        self.assertTrue(
            'This page takes basic details to start your <span class="company-name"><i>TheUniHub</i></span> profile.' in content,
            f"{FAILURE_HEADER}Jumbotron subheading is missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_registration_jumbotron_info(self):
        response = self.client.get(reverse('registration_register'))
        content = response.content.decode()
        self.assertTrue(
            'These fields are all required otherwise you will not be able to make an account with us.' in content,
            f"{FAILURE_HEADER}Jumbotron info text is missing.{FAILURE_FOOTER}"
        )

    def test_registration_form_submission(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass12345',
            'password2': 'newpass12345',
        }
        response = self.client.post(reverse('registration_register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:register_profile'))
        
        user = User.objects.get(username='newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertTrue(user.check_password('newpass12345'))

    def test_registration_form_errors(self):
        data = {
            'username': '',
            'email': 'invalidemail',
            'password1': 'test',
            'password2': 'test',
        }
        response = self.client.post(reverse('registration_register'), data)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertTrue('<strong>Error:</strong> Please correct the following issues.' in content)
        self.assertTrue('Username: This field is required.' in content)
        self.assertTrue('E-mail: Enter a valid email address.' in content)
        self.assertTrue('Password confirmation: This password is too short. It must contain at least 10 characters.' in content)
        self.assertTrue('Password confirmation: This password is too common.' in content)

    def test_profile_registration_access_denied_unauthenticated(self):
        response = self.client.get(reverse('main:register_profile'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('auth_login')))

    def test_profile_registration_access_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:register_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/profile_registration.html')

    def test_profile_registration_title_block(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:register_profile'))
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    Register' in content,
            f"{FAILURE_HEADER}Title block does not contain 'TheUniHub - Register'.{FAILURE_FOOTER}"
        )

    def test_profile_registration_jumbotron_heading(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:register_profile'))
        content = response.content.decode()
        self.assertTrue(
            '<h1 class="jumbotron-heading">Register Here</h1>' in content,
            f"{FAILURE_HEADER}Jumbotron heading 'Register Here' is missing.{FAILURE_FOOTER}"
        )

    def test_profile_registration_jumbotron_subheading(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:register_profile'))
        content = response.content.decode()
        self.assertTrue(
            'This page takes additional details to personalise your <span class="company-name"><i>TheUniHub</i></span> profile.' in content,
            f"{FAILURE_HEADER}Jumbotron subheading is missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_profile_registration_jumbotron_info(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:register_profile'))
        content = response.content.decode()
        self.assertTrue(
            'If you are not currently student then we ask that you leave the university related fields blank.' in content,
            f"{FAILURE_HEADER}Jumbotron info text is missing.{FAILURE_FOOTER}"
        )

    def test_profile_registration_form_submission(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'bio': 'Test biography',
            'university': 'edinburgh',
            'school': 'Science',
            'department': 'Computer Science',
            'degree': 'Computer Science',
            'start_year': 2023,
            'profile_picture': self.VALID_IMAGE
        }
        response = self.client.post(reverse('main:register_profile'), data, format='multipart')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:index'))
        
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.first_name, 'John')
        self.assertEqual(profile.last_name, 'Doe')
        self.assertEqual(profile.bio, 'Test biography')
        self.assertEqual(profile.university, 'edinburgh')
        self.assertEqual(profile.school, 'Science')
        self.assertEqual(profile.department, 'Computer Science')
        self.assertEqual(profile.degree, 'Computer Science')
        self.assertEqual(profile.start_year, 2023)
        self.assertTrue(profile.profile_picture.name.endswith('default.jpg'))

    def test_profile_registration_form_errors(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'first_name': '',
            'last_name': '',
            'bio': '',
        }
        response = self.client.post(reverse('main:register_profile'), data, format='multipart')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertTrue('<strong>Error:</strong> Please correct the issues below.' in content)
        self.assertTrue('First name: This field is required.' in content)
        self.assertTrue('Last name: This field is required.' in content)
        self.assertTrue('Bio: This field is required.' in content)

    def test_profile_registration_form_context(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:register_profile'))
        self.assertIsInstance(response.context['form'], UserProfileForm)

class ProfileManagementTests(TestCase):
    
    def setUp(self):
        
        self.VALID_IMAGE = SimpleUploadedFile(
            name='default.jpg',
            content=open(os.path.join(settings.BASE_DIR, 'default.jpg'), 'rb').read(),
            content_type='image/jpg'
        )

        self.client = Client()
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='testuser@example.com'
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            bio='Test bio',
            university='edinburgh',
            school='Science',
            department='Computer Science',
            degree='Software Engineering',
            start_year=2023,
            profile_picture='default.jpg'
        )
    
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123',
            email='otheruser@example.com'
        )
        self.other_profile = UserProfile.objects.create(
            user=self.other_user,
            first_name='Other',
            last_name='User',
            bio='Other bio',
            profile_picture='default.jpg'
        )

        self.category = Category.objects.create(name='Test Category', description='Test category', slug='test-category')
        self.forum = Forum.objects.create(name='Test Forum', slug='test-forum')

        self.article1 = Article.objects.create(
            author=self.user,
            title='Test Article 1',
            summary='Summary 1',
            slug='test-article-1',
            category=self.category
        )
        self.article2 = Article.objects.create(
            author=self.other_user,
            title='Test Article 2',
            summary='Summary 2',
            slug='test-article-2',
            category=self.category
        )

        self.thread1 = Thread.objects.create(
            author=self.user,
            title='Test Thread 1',
            topic='Topic 1',
            slug='test-thread-1',
            forum=self.forum
        )
        self.thread2 = Thread.objects.create(
            author=self.other_user,
            title='Test Thread 2',
            topic='Topic 2',
            slug='test-thread-2',
            forum=self.forum
        )

    def tearDown(self):
        profile_pics_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pictures')
        if os.path.exists(profile_pics_dir):
            for filename in os.listdir(profile_pics_dir):
                if filename.startswith('default'):
                    file_path = os.path.join(profile_pics_dir, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)

    def test_profile_access_unauthenticated(self):
        response = self.client.get(reverse('main:profile', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('auth_login')))

    def test_profile_access_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:profile', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/profile.html')

    def test_profile_title_block(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:profile', kwargs={'username': 'testuser'}))
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    \n        Profile for testuser' in content,
            f"{FAILURE_HEADER}Title block does not contain 'TheUniHub - Profile for testuser'.{FAILURE_FOOTER}"
        )

    def test_profile_jumbotron_heading(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:profile', kwargs={'username': 'testuser'}))
        content = response.content.decode()
        self.assertTrue(
            '<h1 class="jumbotron-heading">Your Profile</h1>' in content,
            f"{FAILURE_HEADER}Jumbotron heading 'Your Profile' is missing.{FAILURE_FOOTER}"
        )

    def test_profile_jumbotron_subheading(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:profile', kwargs={'username': 'testuser'}))
        content = response.content.decode()
        self.assertTrue(
            'You can edit and view your <span class="company-name"><i>TheUniHub</i></span> profile here.' in content,
            f"{FAILURE_HEADER}Jumbotron subheading is missing or incorrect.{FAILURE_FOOTER}"
        )
    
    def test_profile_jumbotron_info(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:profile', kwargs={'username': 'testuser'}))
        content = response.content.decode()
        self.assertTrue(
            'Test bio' in content,
            f"{FAILURE_HEADER}Jumbotron info is missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_profile_context_data(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:profile', kwargs={'username': 'testuser'}))
        self.assertEqual(response.context['selected_user'], self.user)
        self.assertEqual(response.context['userprofile'], self.user_profile)
        self.assertTrue(response.context['user_has_university'])
        self.assertEqual(response.context['university_website'], 'https://www.ed.ac.uk/')

    def test_profile_unknown_user(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:profile', kwargs={'username': 'nonexistent'}))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    \n        Unknown User' in content,
            f"{FAILURE_HEADER}Title block does not contain 'TheUniHub - Unknown User'.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            '<h1 class="jumbotron-heading">User Not Found</h1>' in content,
            f"{FAILURE_HEADER}Jumbotron heading is missing or incorrect.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'Sorry, please search for the user again.' in content,
            f"{FAILURE_HEADER}Jumbotron subheading is missing or incorrect.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'Make sure you have entered the URL correctly.' in content,
            f"{FAILURE_HEADER}Jumbotron info is missing or incorrect.{FAILURE_FOOTER}"
        )
    
    def test_profile_buttons_self(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:profile', kwargs={'username': 'testuser'}))
        content = response.content.decode()
        
        self.assertInHTML(
            '<a href="{}" class="btn btn-primary btn-sm"><span data-feather="lock"></span> Change your password</a>'.format(reverse('auth_password_change')),
            content,
            msg_prefix=f"{FAILURE_HEADER}'Change your password' button missing.{FAILURE_FOOTER}"
        )
        self.assertInHTML(
            '<a href="{}" class="btn btn-primary btn-sm"><span data-feather="user"></span> Edit your profile</a>'.format(reverse('main:edit_profile')),
            content,
            msg_prefix=f"{FAILURE_HEADER}'Edit your profile' button missing.{FAILURE_FOOTER}"
        )
        self.assertInHTML(
            '<a href="{}" class="btn btn-primary btn-sm"><span data-feather="log-out"></span> Logout</a>'.format(reverse('auth_logout') + '?next=/main/'),
            content,
            msg_prefix=f"{FAILURE_HEADER}'Logout' button missing.{FAILURE_FOOTER}"
        )
        self.assertInHTML(
            '<a href="{}" class="btn btn-danger btn-sm"><span data-feather="trash-2"></span> Delete your account</a>'.format(reverse('main:delete_account_confirmation')),
            content,
            msg_prefix=f"{FAILURE_HEADER}'Delete your account' button missing.{FAILURE_FOOTER}"
        )

    def test_profile_buttons_other_user(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:profile', kwargs={'username': 'otheruser'}))
        content = response.content.decode()
        
        self.assertNotIn('Change your password', content)
        self.assertNotIn('Edit your profile', content)
        self.assertNotIn('Logout', content)
        self.assertNotIn('Delete your account', content)
        self.assertInHTML(
            '<a href="{}"><span data-feather="arrow-left"></span> Back to Users</a>'.format(reverse('main:list_users')),
            content,
            msg_prefix=f"{FAILURE_HEADER}'Back to Users' link missing.{FAILURE_FOOTER}"
        )
    
    def test_profile_articles_self(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:profile', kwargs={'username': 'testuser'}))
        content = response.content.decode()
        
        self.assertIn('<h2 class="h2">Articles by you</h2>', content)
        self.assertInHTML(
            '<a href="{}">Test Article 1</a>'.format(reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article-1'})),
            content
        )
        self.assertIn('Summary 1', content)
        self.assertNotIn('Test Article 2', content)

    def test_profile_articles_other_user(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:profile', kwargs={'username': 'otheruser'}))
        content = response.content.decode()
        
        self.assertIn('<h2 class="h2">Articles by otheruser</h2>', content)
        self.assertInHTML(
            '<a href="{}">Test Article 2</a>'.format(reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article-2'})),
            content
        )
        self.assertIn('Summary 2', content)
        self.assertNotIn('Test Article 1', content)

    def test_profile_no_articles(self):
        UserProfile.objects.all().delete()
        user_no_articles = User.objects.create_user(username='noarticles', password='pass123')
        UserProfile.objects.create(user=user_no_articles, first_name='no', last_name='articles', bio='No articles')
        self.client.login(username='noarticles', password='pass123')
        response = self.client.get(reverse('main:profile', kwargs={'username': 'noarticles'}))
        content = response.content.decode()
        
        self.assertIn('<h2 class="h2">Articles by you</h2>', content)
        self.assertIn("This user hasn't written any articles yet.", content)

    def test_profile_threads_self(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:profile', kwargs={'username': 'testuser'}))
        content = response.content.decode()
        
        self.assertIn('<h2 class="h2">Threads by you</h2>', content)
        self.assertInHTML(
            '<a href="{}">Test Thread 1</a>'.format(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread-1'})),
            content
        )
        self.assertIn('Topic 1', content)
        self.assertNotIn('Test Thread 2', content)

    def test_profile_threads_other_user(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:profile', kwargs={'username': 'otheruser'}))
        content = response.content.decode()
        
        self.assertIn('<h2 class="h2">Threads by otheruser</h2>', content)
        self.assertInHTML(
            '<a href="{}">Test Thread 2</a>'.format(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread-2'})),
            content
        )
        self.assertIn('Topic 2', content)
        self.assertNotIn('Test Thread 1', content)

    def test_profile_no_threads(self):
        UserProfile.objects.all().delete()
        user_no_threads = User.objects.create_user(username='nothreads', password='pass123')
        UserProfile.objects.create(user=user_no_threads, bio='No threads')
        self.client.login(username='nothreads', password='pass123')
        response = self.client.get(reverse('main:profile', kwargs={'username': 'nothreads'}))
        content = response.content.decode()
        
        self.assertIn('<h2 class="h2">Threads by you</h2>', content)
        self.assertIn("This user hasn't started any threads yet.", content)

    def test_edit_profile_access_denied_unauthenticated(self):
        response = self.client.get(reverse('main:edit_profile'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('auth_login')))

    def test_edit_profile_access_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/edit_profile.html')

    def test_edit_profile_title_block(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:edit_profile'))
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    Edit Profile' in content,
            f"{FAILURE_HEADER}Title block does not contain 'TheUniHub - Edit Profile'.{FAILURE_FOOTER}"
        )

    def test_edit_profile_jumbotron_heading(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:edit_profile'))
        content = response.content.decode()
        self.assertTrue(
            '<h1 class="jumbotron-heading">Edit Your Profile</h1>' in content,
            f"{FAILURE_HEADER}Jumbotron heading is missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_edit_profile_jumbotron_subheading(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:edit_profile'))
        content = response.content.decode()
        self.assertTrue(
            'This page allows you to edit your <span class="company-name"><i>TheUniHub</i></span> profile.' in content,
            f"{FAILURE_HEADER}Jumbotron subheading is missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_edit_profile_jumbotron_info(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:edit_profile'))
        content = response.content.decode()
        self.assertTrue(
            'Edit the details for your account.' in content,
            f"{FAILURE_HEADER}Jumbotron info is missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_edit_profile_form_submission(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'bio': 'Updated bio',
            'university': 'glasgow',
            'school': 'Arts',
            'department': 'History',
            'degree': 'Art History',
            'start_year': 2022,
            'profile_picture': self.VALID_IMAGE
        }

        boundary = 'testboundary'
        content = encode_multipart(boundary, data)
        content_type = f'multipart/form-data; boundary={boundary}'

        response = self.client.post(
            reverse('main:edit_profile'),
            data=content,
            content_type=content_type
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:profile', kwargs={'username': 'testuser'}))

        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.first_name, 'Jane')
        self.assertEqual(profile.last_name, 'Doe')
        self.assertEqual(profile.bio, 'Updated bio')
        self.assertEqual(profile.university, 'glasgow')
        self.assertEqual(profile.school, 'Arts')
        self.assertEqual(profile.department, 'History')
        self.assertEqual(profile.degree, 'Art History')
        self.assertEqual(profile.start_year, 2022)
        self.assertTrue('default.jpg' in profile.profile_picture.name, f"Expected 'default.jpg' in {profile.profile_picture.name}")

    def test_edit_profile_form_errors(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'first_name': '',
            'last_name': '',
            'bio': '',
        }

        boundary = 'testboundary'
        content = encode_multipart(boundary, data)
        content_type = f'multipart/form-data; boundary={boundary}'

        response = self.client.post(
            reverse('main:edit_profile'),
            data=content,
            content_type=content_type
        )

        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertTrue('<strong>Error:</strong> Please correct the issues below.' in content)
        self.assertTrue('First name: This field is required.' in content)
        self.assertTrue('Last name: This field is required.' in content)
        self.assertTrue('Bio: This field is required.' in content)

    def test_password_change_access_denied_unauthenticated(self):
        response = self.client.get(reverse('auth_password_change'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('auth_login')))

    def test_password_change_access_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('auth_password_change'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_change_form.html')

    def test_password_change_title_block(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('auth_password_change'))
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    Change your password' in content,
            f"{FAILURE_HEADER}Title block is missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_password_change_jumbotron_heading(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('auth_password_change'))
        content = response.content.decode()
        self.assertTrue(
            '<h1 class="jumbotron-heading">Change your password</h1>' in content,
            f"{FAILURE_HEADER}Jumbotron heading 'Change your password' is missing.{FAILURE_FOOTER}"
        )

    def test_password_change_jumbotron_subheading(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('auth_password_change'))
        content = response.content.decode()
        self.assertTrue(
            'You can now change your <span class="company-name"><i>TheUniHub</i></span> account password.' in content,
            f"{FAILURE_HEADER}Jumbotron subheading is missing or incorrect.{FAILURE_FOOTER}"
        )
    
    def test_password_change_jumbotron_info(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('auth_password_change'))
        content = response.content.decode()
        self.assertTrue(
            'You will need to use this new password when you next sign in.' in content,
            f"{FAILURE_HEADER}Jumbotron subheading is missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_password_change_form_submission(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'old_password': 'testpass123',
            'new_password1': 'newpass12345',
            'new_password2': 'newpass12345',
        }
        response = self.client.post(reverse('auth_password_change'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('auth_password_change_done'))
        
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpass12345'))

    def test_password_change_form_errors(self):
        """Test form errors on invalid password change"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'old_password': 'wrongpass',
            'new_password1': 'short',
            'new_password2': 'different',
        }
        response = self.client.post(reverse('auth_password_change'), data)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertTrue('<strong>Error:</strong> Please correct the following issues.' in content)
        self.assertTrue('Old password: Your old password was entered incorrectly. Please enter it again.' in content)
        self.assertTrue('New password confirmation: The two password fields didn&#39;t match.' in content)

    def test_password_change_done(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('auth_password_change_done'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_change_done.html')
        
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    Password Changed' in content,
            f"{FAILURE_HEADER}Title block does not contain 'TheUniHub - Password Changed'.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            '<h1 class="jumbotron-heading">Change your password</h1>' in content,
            f"{FAILURE_HEADER}Jumbotron heading is missing or incorrect.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'You have changed your <span class="company-name"><i>TheUniHub</i></span> account password.' in content,
            f"{FAILURE_HEADER}Jumbotron subheading is missing or incorrect.{FAILURE_FOOTER}"
        )
        self.assertTrue(
            'You will need to use this new password when you next sign in.' in content,
            f"{FAILURE_HEADER}Jumbotron info is missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_delete_account_confirmation_access_denied_unauthenticated(self):
        response = self.client.get(reverse('main:delete_account_confirmation'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('auth_login')))

    def test_delete_account_confirmation_access_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:delete_account_confirmation'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/confirm_delete_account.html')

    def test_delete_account_confirmation_title_block(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:delete_account_confirmation'))
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    Delete your account' in content,
            f"{FAILURE_HEADER}Title block does not contain 'TheUniHub - Delete your account'.{FAILURE_FOOTER}"
        )

    def test_delete_account_confirmation_jumbotron_heading(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:delete_account_confirmation'))
        content = response.content.decode()
        self.assertTrue(
            '<h1 class="jumbotron-heading">Delete Your Account</h1>' in content,
            f"{FAILURE_HEADER}Jumbotron heading 'Delete Your Account' is missing.{FAILURE_FOOTER}"
        )

    def test_delete_account_confirmation_jumbotron_subheading(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:delete_account_confirmation'))
        content = response.content.decode()
        self.assertTrue(
            'You are trying to delete your <span class="company-name"><i>TheUniHub</i></span> account.' in content,
            f"{FAILURE_HEADER}Jumbotron subheading is missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_delete_account_confirmation_jumbotron_info(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:delete_account_confirmation'))
        content = response.content.decode()
        self.assertTrue(
            'Please make sure this is what you are trying to do because you will not be able to recover your account.' in content,
            f"{FAILURE_HEADER}Jumbotron info is missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_delete_account_submission(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('main:delete_account'), {})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:index'))
        
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username='testuser')
        with self.assertRaises(UserProfile.DoesNotExist):
            UserProfile.objects.get(user=self.user)

class UsersTemplateTests(TestCase):
    
    def setUp(self):
        
        self.VALID_IMAGE = SimpleUploadedFile(
            name='default.jpg',
            content=open(os.path.join(settings.BASE_DIR, 'default.jpg'), 'rb').read(),
            content_type='image/jpg'
        )

        self.client = Client()
        
        self.user1 = User.objects.create_user(
            username='user1',
            password='pass123',
            email='user1@example.com'
        )
        self.profile1 = UserProfile.objects.create(
            user=self.user1,
            first_name='User',
            last_name='One',
            bio='Bio 1',
            university='edinburgh',
            profile_picture=self.VALID_IMAGE
        )

        self.user2 = User.objects.create_user(
            username='user2',
            password='pass123',
            email='user2@example.com'
        )
        self.profile2 = UserProfile.objects.create(
            user=self.user2,
            first_name='User',
            last_name='Two',
            bio='Bio 2',
            university='glasgow',
            profile_picture=self.VALID_IMAGE
        )

    def tearDown(self):
        profile_pics_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pictures')
        if os.path.exists(profile_pics_dir):
            for filename in os.listdir(profile_pics_dir):
                if filename.startswith('default'):
                    file_path = os.path.join(profile_pics_dir, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)

    def test_list_users_access_authenticated(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('main:list_users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/list_users.html')
        self.assertTemplateUsed(response, 'main/profiles.html')

    def test_list_users_access_denied_unauthenticated(self):
        response = self.client.get(reverse('main:list_users'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/main/users/')

    def test_list_users_title_block(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('main:list_users'))
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    User Profiles' in content,
            f"{FAILURE_HEADER}Title block does not contain 'TheUniHub - User Profiles'.{FAILURE_FOOTER}"
        )

    def test_list_users_jumbotron_heading(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('main:list_users'))
        content = response.content.decode()
        self.assertIn('<h1 class="jumbotron-heading">User Profiles</h1>', content)
        
    def test_list_users_jumbotron_subheading(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('main:list_users'))
        content = response.content.decode()
        self.assertIn(
            'Here you can search and filter the profiles of all <span class="company-name"><i>TheUniHub</i></span> users.',
            content,
            msg=f"{FAILURE_HEADER}Jumbotron subheading missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_list_users_jumbotron_info(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('main:list_users'))
        content = response.content.decode()
        self.assertIn(
            'Your can edit and view your own profile <a href="/main/profile/user1/">here</a>',
            content,
            msg=f"{FAILURE_HEADER}Jumbotron info missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_list_users_profile_link(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('main:list_users'))
        content = response.content.decode()
        self.assertInHTML(
            '<a href="{}">here</a>'.format(reverse('main:profile', kwargs={'username': 'user1'})),
            content,
            msg_prefix=f"{FAILURE_HEADER}Profile link for logged-in user missing.{FAILURE_FOOTER}"
        )

    def test_list_users_search_filter_elements(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('main:list_users'))
        content = response.content.decode()
        self.assertIn(
            '<input type="text" id="profile-search-input" class="form-control" placeholder="Search by username...">',
            content,
            msg=f"{FAILURE_HEADER}Search input missing.{FAILURE_FOOTER}"
        )
        self.assertIn(
            '<select id="university-filter" class="form-control">',
            content,
            msg=f"{FAILURE_HEADER}University filter missing.{FAILURE_FOOTER}"
        )
        self.assertIn('<option value="edinburgh">', content)
        self.assertIn('<option value="glasgow">', content)

class CategoryManagementTests(TestCase):
    
    def setUp(self):
        
        self.VALID_IMAGE = SimpleUploadedFile(
            name='default.jpg',
            content=open(os.path.join(settings.BASE_DIR, 'default.jpg'), 'rb').read(),
            content_type='image/jpg'
        )

        self.client = Client()

        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            bio='Test bio',
            university='edinburgh',
            school='Test School',
            department='Test Department',
            degree='Test Degree',
            start_year=2025,
            profile_picture=self.VALID_IMAGE
        )
        
        self.staff_user = User.objects.create_user(username='staffuser', password='staffpass123', is_staff=True)
        self.user_profile = UserProfile.objects.create(
            user=self.staff_user,
            first_name='Test',
            last_name='User',
            bio='Test bio',
            university='edinburgh',
            school='Test School',
            department='Test Department',
            degree='Test Degree',
            start_year=2025,
            profile_picture=self.VALID_IMAGE
        )
        
        self.category1 = Category.objects.create(
            name='Test Category 1',
            description='First test category',
            slug='test-category-1',
            views=5,
            points=3
        )
        self.category2 = Category.objects.create(
            name='Test Category 2',
            description='Second test category',
            slug='test-category-2',
            views=10,
            points=7
        )

        self.article = Article.objects.create(
            title='Test Article',
            summary='Test summary',
            content='Test content',
            category=self.category1,
            author=self.user,
            slug='test-article',
            views=0,
            points=0
        )

    def tearDown(self):
        profile_pics_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pictures')
        if os.path.exists(profile_pics_dir):
            for filename in os.listdir(profile_pics_dir):
                if filename.startswith('default'):
                    file_path = os.path.join(profile_pics_dir, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)

    def _create_long_string(self, length):
        return 'a' * length

    def test_category_list_loads(self):
        response = self.client.get(reverse('main:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/category_list.html')

    def test_category_list_title_block(self):
        response = self.client.get(reverse('main:category_list'))
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    Categories' in content,
            f"{FAILURE_HEADER}Title block does not contain 'TheUniHub - Categories'.{FAILURE_FOOTER}"
        )

    def test_category_list_jumbotron_heading(self):
        response = self.client.get(reverse('main:category_list'))
        content = response.content.decode()
        self.assertTrue(
            '<h1 class="jumbotron-heading">Categories</h1>' in content,
            f"{FAILURE_HEADER}Jumbotron heading 'Categories' is missing.{FAILURE_FOOTER}"
        )

    def test_category_list_jumbotron_subheading(self):
        response = self.client.get(reverse('main:category_list'))
        content = response.content.decode()
        self.assertTrue(
            'Read and write about university and student-life related on <span class="company-name"><i>TheUniHub</i></span>.' in content,
            f"{FAILURE_HEADER}Jumbotron subheading is missing or incorrect.{FAILURE_FOOTER}"
        )
    
    def test_category_list_jumbotron_info(self):
        response = self.client.get(reverse('main:category_list'))
        content = response.content.decode()
        self.assertTrue(
            'You can create articles and comments on any of the categories.' in content,
            f"{FAILURE_HEADER}Jumbotron info text is missing.{FAILURE_FOOTER}"
        )

    def test_category_lists(self):
        response = self.client.get(reverse('main:category_list'))
        self.assertContains(response, 'Test Category 1')
        self.assertContains(response, 'First test category')
        self.assertContains(response, '5 views')
        self.assertContains(response, '3 points')
        self.assertContains(response, 'Test Category 2')
        self.assertContains(response, 'Second test category')
        self.assertContains(response, '10 views')
        self.assertContains(response, '7 points')

    def test_category_lists_empty(self):
        Category.objects.all().delete()
        response = self.client.get(reverse('main:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Categories on <span class="company-name"><i>TheUniHub</i></span>')
        self.assertNotContains(response, 'list-group-item')

    def test_category_list_staff_add_button(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:category_list'))
        self.assertContains(response, 'Add Category')

    def test_category_loads(self):
        response = self.client.get(reverse('main:show_category', kwargs={'category_name_slug': 'test-category-1'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/category.html')
    
    def test_category_title_block(self):
        response = self.client.get(reverse('main:show_category', kwargs={'category_name_slug': 'test-category-1'}))
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    \n        Articles in Test Category 1' in content,
            f"{FAILURE_HEADER}Title block does not contain 'TheUniHub - Test Category 1'.{FAILURE_FOOTER}"
        )

    def test_category_jumbotron_heading(self):
        response = self.client.get(reverse('main:show_category', kwargs={'category_name_slug': 'test-category-1'}))
        content = response.content.decode()
        self.assertTrue(
            '<h1 class="jumbotron-heading">Test Category 1</h1>' in content,
            f"{FAILURE_HEADER}Jumbotron heading 'Test Category 1' is missing.{FAILURE_FOOTER}"
        )

    def test_category_jumbotron_subheading(self):
        response = self.client.get(reverse('main:show_category', kwargs={'category_name_slug': 'test-category-1'}))
        content = response.content.decode()
        self.assertTrue(
            'Search, view, and post on this category.' in content,
            f"{FAILURE_HEADER}Jumbotron subheading is missing or incorrect.{FAILURE_FOOTER}"
        )
    
    def test_category_jumbotron_info(self):
        response = self.client.get(reverse('main:show_category', kwargs={'category_name_slug': 'test-category-1'}))
        content = response.content.decode()
        self.assertTrue(
            'First test category' in content,
            f"{FAILURE_HEADER}Jumbotron info text is missing.{FAILURE_FOOTER}"
        )

    def test_category_staff_edit_button(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:show_category', kwargs={'category_name_slug': 'test-category-1'}))
        self.assertContains(response, 'Edit Category')

    def test_category_unknown(self):
        response = self.client.get(reverse('main:show_category', kwargs={'category_name_slug': 'nonexistent'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Category not found')
        self.assertNotContains(response, 'Articles in')

    def test_category_increments_views(self):
        initial_views = self.category1.views
        self.client.get(reverse('main:show_category', kwargs={'category_name_slug': 'test-category-1'}))
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.views, initial_views + 1)
        response = self.client.get(reverse('main:show_category', kwargs={'category_name_slug': 'test-category-1'}))
        self.category1.refresh_from_db()
        self.assertContains(response, f'<strong id="view_count">{initial_views + 2}</strong> views')

    def test_category_no_articles(self):
        Article.objects.all().delete()
        response = self.client.get(reverse('main:show_category', kwargs={'category_name_slug': 'test-category-1'}))
        self.assertContains(response, 'No articles in this category yet')

    def test_add_category_access_denied_unauthenticated(self):
        response = self.client.get(reverse('main:add_category'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={reverse("main:add_category")}')

    def test_add_category_access_denied_non_staff(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:add_category'))
        self.assertRedirects(response, reverse('main:index'))

    def test_add_category_access_staff(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:add_category'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/add_category.html')
        self.assertContains(response, 'Add a Category')
        self.assertContains(response, 'Add Category')

    def test_add_category_form_submission(self):
        self.client.login(username='staffuser', password='staffpass123')
        data = {
            'name': 'New Category',
            'description': 'New category description'
        }
        response = self.client.post(reverse('main:add_category'), data)
        self.assertRedirects(response, reverse('main:index'))
        new_category = Category.objects.get(name='New Category')
        self.assertEqual(new_category.description, 'New category description')
        self.assertEqual(new_category.slug, 'new-category')
        self.assertEqual(new_category.views, 0)
        self.assertEqual(new_category.points, 0)

    def test_add_category_form_missing_field(self):
        self.client.login(username='staffuser', password='staffpass123')
        data = {
            'name': '',
            'description': 'Description only'
        }
        response = self.client.post(reverse('main:add_category'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<strong>Error:</strong> Please correct the issues below')
        self.assertContains(response, 'This field is required')
        self.assertFalse(Category.objects.filter(description='Description only').exists())

    def test_add_category_form_invalid_name(self):
        self.client.login(username='staffuser', password='staffpass123')
        data = {
            'name': self._create_long_string(500),
            'description': 'Valid description'
        }
        response = self.client.post(reverse('main:add_category'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ensure this value has at most 150 characters')
        self.assertFalse(Category.objects.filter(description='Valid description').exists())

    def test_add_category_form_invalid_description(self):
        self.client.login(username='staffuser', password='staffpass123')
        data = {
            'name': 'Valid Name',
            'description': self._create_long_string(5000)
        }
        response = self.client.post(reverse('main:add_category'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ensure this value has at most 1000 characters')
        self.assertFalse(Category.objects.filter(name='Valid Name').exists())

    def test_add_category_form_duplicate_name(self):
        self.client.login(username='staffuser', password='staffpass123')
        data = {
            'name': 'Test Category 1',
            'description': 'Different description'
        }
        response = self.client.post(reverse('main:add_category'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Category with this Name already exists')
        self.assertEqual(Category.objects.filter(name='Test Category 1').count(), 1)

    def test_edit_category_access_denied_unauthenticated(self):
        response = self.client.get(reverse('main:edit_category', kwargs={'category_name_slug': 'test-category-1'}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={reverse("main:edit_category", kwargs={"category_name_slug": "test-category-1"})}')

    def test_edit_category_access_denied_non_staff(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:edit_category', kwargs={'category_name_slug': 'test-category-1'}))
        self.assertRedirects(response, reverse('main:show_category', kwargs={'category_name_slug': 'test-category-1'}))

    def test_edit_category_access_staff(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:edit_category', kwargs={'category_name_slug': 'test-category-1'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/edit_category.html')
        self.assertContains(response, 'Edit Category: Test Category 1')
        self.assertContains(response, 'value="Test Category 1"')
        self.assertContains(response, 'First test category')

    def test_edit_category_unknown(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:edit_category', kwargs={'category_name_slug': 'nonexistent'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Category Not Found')

    def test_edit_category_form_submission(self):
        self.client.login(username='staffuser', password='staffpass123')
        data = {
            'name': 'Updated Category',
            'description': 'Updated description'
        }
        response = self.client.post(reverse('main:edit_category', kwargs={'category_name_slug': 'test-category-1'}), data)
        self.assertRedirects(response, reverse('main:show_category', kwargs={'category_name_slug': 'updated-category'}))
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.name, 'Updated Category')
        self.assertEqual(self.category1.description, 'Updated description')
        self.assertEqual(self.category1.slug, 'updated-category')

    def test_edit_category_form_invalid_name(self):
        self.client.login(username='staffuser', password='staffpass123')
        data = {
            'name': '',
            'description': 'New description'
        }
        response = self.client.post(reverse('main:edit_category', kwargs={'category_name_slug': 'test-category-1'}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.name, 'Test Category 1')

    def test_edit_category_form_duplicate_name(self):
        self.client.login(username='staffuser', password='staffpass123')
        data = {
            'name': 'Test Category 2',
            'description': 'Trying to duplicate'
        }
        response = self.client.post(reverse('main:edit_category', kwargs={'category_name_slug': 'test-category-1'}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Category with this Name already exists')
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.name, 'Test Category 1')

    def test_delete_category_access_denied_unauthenticated(self):
        response = self.client.get(reverse('main:delete_category', kwargs={'category_name_slug': 'test-category-1'}))
        self.assertEqual(response.status_code, 302)

    def test_delete_category_access_denied_non_staff(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:delete_category', kwargs={'category_name_slug': 'test-category-1'}))
        self.assertRedirects(response, reverse('main:show_category', kwargs={'category_name_slug': 'test-category-1'}))

    def test_delete_category_access_staff(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:delete_category', kwargs={'category_name_slug': 'test-category-1'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/delete_category.html')
        self.assertContains(response, 'Test Category 1')

    def test_delete_category_unknown(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:delete_category', kwargs={'category_name_slug': 'nonexistent'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Category Not Found')

    def test_delete_category_submission(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.post(reverse('main:delete_category', kwargs={'category_name_slug': 'test-category-1'}))
        self.assertRedirects(response, reverse('main:category_list'))
        self.assertFalse(Category.objects.filter(slug='test-category-1').exists())
        self.assertFalse(Article.objects.filter(slug='test-article').exists())

    def test_like_category_unauthenticated(self):
        response = self.client.get(reverse('main:like_category'), {'category_id': self.category1.id})
        self.assertEqual(response.status_code, 302)

    def test_like_category_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        initial_points = self.category1.points
        response = self.client.get(reverse('main:like_category'), {'category_id': self.category1.id})
        self.assertEqual(response.status_code, 200)
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.points, initial_points + 1)
        self.assertEqual(int(response.content), initial_points + 1)

    def test_like_category_invalid_id(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:like_category'), {'category_id': '999'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), '-1')

    def test_like_category_non_numeric_id(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:like_category'), {'category_id': 'abc'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), '-1')

    def test_like_category_multiple_likes(self):
        self.client.login(username='testuser', password='testpass123')
        initial_points = self.category1.points
        self.client.get(reverse('main:like_category'), {'category_id': self.category1.id})
        self.client.get(reverse('main:like_category'), {'category_id': self.category1.id})
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.points, initial_points + 2)

    def test_dislike_category_unauthenticated(self):
        response = self.client.get(reverse('main:dislike_category'), {'category_id': self.category1.id})
        self.assertEqual(response.status_code, 302)

    def test_dislike_category_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        initial_points = self.category1.points
        response = self.client.get(reverse('main:dislike_category'), {'category_id': self.category1.id})
        self.assertEqual(response.status_code, 200)
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.points, initial_points - 1)
        self.assertEqual(int(response.content), initial_points - 1)

    def test_dislike_category_invalid_id(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:dislike_category'), {'category_id': '999'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), '-1')

    def test_dislike_category_non_numeric_id(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:dislike_category'), {'category_id': 'abc'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), '-1')

    def test_dislike_category_view_below_zero(self):
        self.client.login(username='testuser', password='testpass123')
        self.category1.points = 0
        self.category1.save()
        response = self.client.get(reverse('main:dislike_category'), {'category_id': self.category1.id})
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.points, -1)
        self.assertEqual(int(response.content), -1)

class ArticleManagementTests(TestCase):
    
    def setUp(self):
        
        self.VALID_IMAGE = SimpleUploadedFile(
            name='default.jpg',
            content=open(os.path.join(settings.BASE_DIR, 'default.jpg'), 'rb').read(),
            content_type='image/jpg'
        )

        self.client = Client()

        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            bio='Test bio',
            university='edinburgh',
            school='Test School',
            department='Test Department',
            degree='Test Degree',
            start_year=2025,
            profile_picture=self.VALID_IMAGE
        )

        self.staff_user = User.objects.create_user(username='staffuser', password='staffpass123', is_staff=True)
        self.staff_profile = UserProfile.objects.create(
            user=self.staff_user,
            first_name='Staff',
            last_name='User',
            bio='Staff bio',
            university='edinburgh',
            school='Test School',
            department='Test Department',
            degree='Test Degree',
            start_year=2025,
            profile_picture=self.VALID_IMAGE
        )

        self.category = Category.objects.create(
            name='Test Category',
            description='Test category description',
            slug='test-category',
            views=5,
            points=3
        )

        self.article = Article.objects.create(
            title='Test Article',
            summary='Test summary',
            content='Test content',
            category=self.category,
            author=self.user,
            slug='test-article',
            views=0,
            points=0,
            article_image=self.VALID_IMAGE
        )

    def tearDown(self):
        profile_pics_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pictures')
        article_imgs_dir = os.path.join(settings.MEDIA_URL, 'article_images')
        for directory in (profile_pics_dir, article_imgs_dir):
            if os.path.exists(directory):
                for filename in os.listdir(directory):
                    if filename.startswith('default'):
                        file_path = os.path.join(directory, filename)
                        if os.path.isfile(file_path):
                            os.remove(file_path)

    def _create_long_string(self, length):
        return 'a' * length

    def test_article_loads(self):
        response = self.client.get(reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/article.html')

    def test_article_title_block(self):
        response = self.client.get(reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    \n        Test Article' in content,
            f"{FAILURE_HEADER}Title block does not contain 'TheUniHub - Test Article'.{FAILURE_FOOTER}"
        )

    def test_article_jumbotron_heading(self):
        response = self.client.get(reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        content = response.content.decode()
        self.assertTrue(
            '<h1 class="jumbotron-heading">Test Article</h1>' in content,
            f"{FAILURE_HEADER}Jumbotron heading 'Test Article' is missing.{FAILURE_FOOTER}"
        )

    def test_article_jumbotron_info(self):
        response = self.client.get(reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        content = response.content.decode()
        self.assertTrue(
            'Test summary' in content,
            f"{FAILURE_HEADER}Jumbotron info is missing or incorrect.{FAILURE_FOOTER}"
        )
    
    def test_article_jumbotron_detail(self):
        response = self.client.get(reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        content = response.content.decode()
        self.assertTrue(
            'Written by' in content,
            f"{FAILURE_HEADER}Jumbotron detail is missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_article_content(self):
        response = self.client.get(reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.assertContains(response, 'Test summary')
        self.assertContains(response, 'Test content')
        self.assertContains(response, '<strong id="view_count">1</strong> views')
        self.assertContains(response, '<strong id="point_count">0</strong> points')

    def test_article_unknown(self):
        response = self.client.get(reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'nonexistent'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Article Not Found')
        self.assertNotContains(response, 'Test Article')

    def test_article_increments_views(self):
        initial_views = self.article.views
        self.client.get(reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.article.refresh_from_db()
        self.assertEqual(self.article.views, initial_views + 1)
        response = self.client.get(reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.article.refresh_from_db()
        self.assertContains(response, f'<strong id="view_count">{initial_views + 2}</strong> views')

    def test_article_favourite_button_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.assertContains(response, 'Favourite')

    def test_article_edit_button_author(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.assertContains(response, 'Edit Article')

    def test_article_edit_button_non_author(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.assertNotContains(response, 'Edit Article')

    def test_add_article_access_denied_unauthenticated(self):
        response = self.client.get(reverse('main:add_article', kwargs={'category_name_slug': 'test-category'}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={reverse("main:add_article", kwargs={"category_name_slug": "test-category"})}')

    def test_add_article_access_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:add_article', kwargs={'category_name_slug': 'test-category'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/add_article.html')
        self.assertContains(response, 'Add an Article')
        self.assertContains(response, 'Publish Article')

    def test_add_article_form_submission(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'New Article',
            'summary': 'New summary',
            'content': 'New content',
            'related_university': 'edinburgh'
        }
        response = self.client.post(reverse('main:add_article', kwargs={'category_name_slug': 'test-category'}), data)
        self.assertRedirects(response, reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'new-article'}))
        new_article = Article.objects.get(title='New Article')
        self.assertEqual(new_article.summary, 'New summary')
        self.assertEqual(new_article.content, 'New content')
        self.assertEqual(new_article.related_university, 'edinburgh')
        self.assertEqual(new_article.views, 1)
        self.assertEqual(new_article.points, 0)

    def test_add_article_form_missing_field(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': '',
            'summary': 'Summary only',
            'content': 'Content only'
        }
        response = self.client.post(reverse('main:add_article', kwargs={'category_name_slug': 'test-category'}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<strong>Error:</strong> Please correct the issues below')
        self.assertContains(response, 'This field is required')
        self.assertFalse(Article.objects.filter(summary='Summary only').exists())

    def test_add_article_form_invalid_title(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': self._create_long_string(750),
            'summary': 'Valid summary',
            'content': 'Valid content'
        }
        response = self.client.post(reverse('main:add_article', kwargs={'category_name_slug': 'test-category'}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ensure this value has at most 500 characters')
        self.assertFalse(Article.objects.filter(summary='Valid summary').exists())

    def test_add_article_form_banned_words(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'Fuck This',
            'summary': 'Test summary',
            'content': 'Test content'
        }
        response = self.client.post(reverse('main:add_article', kwargs={'category_name_slug': 'test-category'}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The title of your article contains innappropriate content')
        self.assertFalse(Article.objects.filter(title='Fuck This').exists())

    def test_add_article_form_search(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'query': 'test search',
            'search': 'Search online'
        }
        response = self.client.post(reverse('main:add_article', kwargs={'category_name_slug': 'test-category'}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Search for related articles')
        self.assertContains(response, 'test search')

    def test_edit_article_access_denied_unauthenticated(self):
        response = self.client.get(reverse('main:edit_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={reverse("main:edit_article", kwargs={"category_name_slug": "test-category", "article_title_slug": "test-article"})}')

    def test_edit_article_access_denied_non_author(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:edit_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.assertRedirects(response, reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))

    def test_edit_article_access_author(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:edit_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/edit_article.html')
        self.assertContains(response, 'Edit Article: Test Article')
        self.assertContains(response, 'Save Changes')

    def test_edit_article_unknown(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:edit_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'nonexistent'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Article Not Found')

    def test_edit_article_form_submission(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'Updated Article',
            'summary': 'Updated summary',
            'content': 'Updated content',
            'related_university': 'glasgow'
        }
        response = self.client.post(reverse('main:edit_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}), data)
        self.assertRedirects(response, reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Updated Article')
        self.assertEqual(self.article.summary, 'Updated summary')
        self.assertEqual(self.article.content, 'Updated content')
        self.assertEqual(self.article.related_university, 'glasgow')

    def test_edit_article_form_missing_field(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': '',
            'summary': 'Test summary',
            'content': 'Test content'
        }
        response = self.client.post(reverse('main:edit_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Test Article')

    def test_edit_article_form_banned_words(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'Shit Article',
            'summary': 'Test summary',
            'content': 'Test content'
        }
        response = self.client.post(reverse('main:edit_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The title of your article contains innappropriate content')
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Test Article')

    def test_delete_article_access_denied_unauthenticated(self):
        response = self.client.get(reverse('main:delete_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.assertEqual(response.status_code, 302)

    def test_delete_article_access_denied_non_author(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:delete_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.assertRedirects(response, reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))

    def test_delete_article_access_author(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:delete_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/delete_article.html')
        self.assertContains(response, 'Delete Article: Test Article')
        self.assertContains(response, 'Yes, delete my article')

    def test_delete_article_unknown(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:delete_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'nonexistent'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Article Not Found')

    def test_delete_article_submission(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('main:delete_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.assertRedirects(response, reverse('main:show_category', kwargs={'category_name_slug': 'test-category'}))
        self.assertFalse(Article.objects.filter(slug='test-article').exists())

    def test_like_article_unauthenticated(self):
        response = self.client.get(reverse('main:like_article'), {'article_id': self.article.id})
        self.assertEqual(response.status_code, 302)

    def test_like_article_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        initial_points = self.article.points
        response = self.client.get(reverse('main:like_article'), {'article_id': self.article.id})
        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertEqual(self.article.points, initial_points + 1)
        self.assertEqual(int(response.content), initial_points + 1)

    def test_like_article_invalid_id(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:like_article'), {'article_id': '999'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), '-1')

    def test_like_article_multiple_likes(self):
        self.client.login(username='testuser', password='testpass123')
        initial_points = self.article.points
        self.client.get(reverse('main:like_article'), {'article_id': self.article.id})
        self.client.get(reverse('main:like_article'), {'article_id': self.article.id})
        self.article.refresh_from_db()
        self.assertEqual(self.article.points, initial_points + 2)

    def test_dislike_article_unauthenticated(self):
        response = self.client.get(reverse('main:dislike_article'), {'article_id': self.article.id})
        self.assertEqual(response.status_code, 302)

    def test_dislike_article_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        initial_points = self.article.points
        response = self.client.get(reverse('main:dislike_article'), {'article_id': self.article.id})
        self.assertEqual(response.status_code, 200)
        self.article.refresh_from_db()
        self.assertEqual(self.article.points, initial_points - 1)
        self.assertEqual(int(response.content), initial_points - 1)

    def test_dislike_article_below_zero(self):
        self.client.login(username='testuser', password='testpass123')
        self.article.points = 0
        self.article.save()
        response = self.client.get(reverse('main:dislike_article'), {'article_id': self.article.id})
        self.article.refresh_from_db()
        self.assertEqual(self.article.points, -1)
        self.assertEqual(int(response.content), -1)

    def test_favourite_article_unauthenticated(self):
        response = self.client.post(reverse('main:favourite_article', kwargs={'article_title_slug': 'test-article'}))
        self.assertEqual(response.status_code, 302)

    def test_favourite_article_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('main:favourite_article', kwargs={'article_title_slug': 'test-article'}))
        self.assertRedirects(response, reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.user_profile.refresh_from_db()
        self.assertIn(self.article, self.user_profile.favourite_articles.all())

    def test_unfavourite_article_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        self.user_profile.favourite_articles.add(self.article)
        response = self.client.post(reverse('main:favourite_article', kwargs={'article_title_slug': 'test-article'}))
        self.assertRedirects(response, reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.user_profile.refresh_from_db()
        self.assertNotIn(self.article, self.user_profile.favourite_articles.all())

class CommentManagementTests(TestCase):
    
    def setUp(self):
        
        self.VALID_IMAGE = SimpleUploadedFile(
            name='default.jpg',
            content=open(os.path.join(settings.BASE_DIR, 'default.jpg'), 'rb').read(),
            content_type='image/jpg'
        )

        self.client = Client()

        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            bio='Test bio',
            university='edinburgh',
            school='Test School',
            department='Test Department',
            degree='Test Degree',
            start_year=2025,
            profile_picture=self.VALID_IMAGE
        )

        self.other_user = User.objects.create_user(username='otheruser', password='otherpass123')
        self.other_profile = UserProfile.objects.create(
            user=self.other_user,
            first_name='Other',
            last_name='User',
            bio='Other bio',
            university='edinburgh',
            school='Other School',
            department='Other Department',
            degree='Other Degree',
            start_year=2025,
            profile_picture=self.VALID_IMAGE
        )

        self.category = Category.objects.create(
            name='Test Category',
            description='Test category description',
            slug='test-category',
            views=5,
            points=3
        )

        self.article = Article.objects.create(
            title='Test Article',
            summary='Test summary',
            content='Test content',
            category=self.category,
            author=self.user,
            slug='test-article',
            views=0,
            points=0,
            article_image=self.VALID_IMAGE
        )

        self.comment = Comment.objects.create(
            article=self.article,
            author=self.user,
            content='Test comment',
            written_on=timezone.now()
        )

    def tearDown(self):
        profile_pics_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pictures')
        article_imgs_dir = os.path.join(settings.MEDIA_ROOT, 'article_images')
        for directory in (profile_pics_dir, article_imgs_dir):
            if os.path.exists(directory):
                for filename in os.listdir(directory):
                    if filename.startswith('default'):
                        file_path = os.path.join(directory, filename)
                        if os.path.isfile(file_path):
                            os.remove(file_path)

    def _create_long_string(self, length):
        return 'a' * length

    def test_comments_load_on_article(self):
        response = self.client.get(reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/article.html')
        self.assertContains(response, 'Comments')
        self.assertContains(response, 'Test comment')
        self.assertContains(response, 'testuser')

    def test_comments_empty_on_article(self):
        Comment.objects.all().delete()
        response = self.client.get(reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No comments yet. Be the first to comment!')

    def test_comment_edit_button_author(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.assertContains(response, '<a href="/main/category/test-category/article/test-article/1/edit_comment/"')

    def test_comment_edit_button_non_author(self):
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.get(reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.assertNotContains(response, '<a href="/main/category/test-category/article/test-article/1/edit_comment/"')

    def test_add_comment_unauthenticated(self):
        response = self.client.get(reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.assertContains(response, '<a href="/accounts/login/">Login</a> to add a comment.')

    def test_add_comment_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.assertContains(response, 'Add a Comment')
        self.assertContains(response, 'Comment')

    def test_add_comment_form_submission(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'content': 'New comment'}
        response = self.client.post(reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}), data)
        self.assertRedirects(response, reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        new_comment = Comment.objects.get(content='New comment')
        self.assertEqual(new_comment.author, self.user)
        self.assertEqual(new_comment.article, self.article)

    def test_add_comment_form_missing_field(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'content': ''}
        response = self.client.post(reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        self.assertFalse(Comment.objects.filter(content='').exists())

    def test_add_comment_form_banned_words(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'content': 'Fuck you'}
        response = self.client.post(
            reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}),
            data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Comment.objects.filter(content='Fuck you').exists())

    def test_edit_comment_access_denied_unauthenticated(self):
        response = self.client.get(reverse('main:edit_comment', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article', 'comment_id': self.comment.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={reverse("main:edit_comment", kwargs={"category_name_slug": "test-category", "article_title_slug": "test-article", "comment_id": self.comment.id})}')

    def test_edit_comment_access_denied_non_author(self):
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.get(reverse('main:edit_comment', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article', 'comment_id': self.comment.id}))
        self.assertRedirects(response, reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))

    def test_edit_comment_access_author(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:edit_comment', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article', 'comment_id': self.comment.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/edit_comment.html')
        self.assertContains(response, 'Edit Comment: Test Article')
        self.assertContains(response, 'Save Changes')

    def test_edit_comment_time_limit_exceeded(self):
        self.client.login(username='testuser', password='testpass123')
        self.comment.written_on = timezone.now() - timedelta(days=1)
        self.comment.save()
        response = self.client.get(reverse('main:edit_comment', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article', 'comment_id': self.comment.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You\'re not within the time limit to edit this comment')

    def test_edit_comment_unknown(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:edit_comment', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article', 'comment_id': 999}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Article/Comment Not Found')

    def test_edit_comment_form_submission(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'content': 'Updated comment'}
        response = self.client.post(reverse('main:edit_comment', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article', 'comment_id': self.comment.id}), data)
        self.assertRedirects(response, reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Updated comment')
        self.assertIsNotNone(self.comment.edited_on)

    def test_edit_comment_form_missing_field(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'content': ''}
        response = self.client.post(reverse('main:edit_comment', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article', 'comment_id': self.comment.id}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Test comment')

    def test_edit_comment_form_banned_words(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'content': 'Fuck you'}
        response = self.client.post(reverse('main:edit_comment', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article', 'comment_id': self.comment.id}), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Comment.objects.filter(content='Fuck you').exists())

    def test_delete_comment_access_denied_unauthenticated(self):
        response = self.client.get(reverse('main:delete_comment', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article', 'comment_id': self.comment.id}))
        self.assertEqual(response.status_code, 302)

    def test_delete_comment_access_denied_non_author(self):
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.get(reverse('main:delete_comment', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article', 'comment_id': self.comment.id}))
        self.assertRedirects(response, reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))

    def test_delete_comment_access_author(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:delete_comment', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article', 'comment_id': self.comment.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/delete_comment.html')
        self.assertContains(response, 'Delete Comment: Test Article')
        self.assertContains(response, 'Yes, delete my comment')

    def test_delete_comment_time_limit_exceeded(self):
        self.client.login(username='testuser', password='testpass123')
        self.comment.written_on = timezone.now() - timedelta(days=1)
        self.comment.save()
        response = self.client.get(reverse('main:delete_comment', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article', 'comment_id': self.comment.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You\'re not within the time limit to delete this comment')

    def test_delete_comment_unknown(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:delete_comment', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article', 'comment_id': 999}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Article/Comment Not Found')

    def test_delete_comment_submission(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('main:delete_comment', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article', 'comment_id': self.comment.id}))
        self.assertRedirects(response, reverse('main:show_article', kwargs={'category_name_slug': 'test-category', 'article_title_slug': 'test-article'}))
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())

class ForumManagementTests(TestCase):
    
    def setUp(self):
        
        self.VALID_IMAGE = SimpleUploadedFile(
            name='default.jpg',
            content=open(os.path.join(settings.BASE_DIR, 'default.jpg'), 'rb').read(),
            content_type='image/jpg'
        )

        self.client = Client()

        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            bio='Test bio',
            university='edinburgh',
            school='Test School',
            department='Test Department',
            degree='Test Degree',
            start_year=2025,
            profile_picture=self.VALID_IMAGE
        )
        
        self.staff_user = User.objects.create_user(username='staffuser', password='staffpass123', is_staff=True)
        self.staff_profile = UserProfile.objects.create(
            user=self.staff_user,
            first_name='Staff',
            last_name='User',
            bio='Staff bio',
            university='edinburgh',
            school='Staff School',
            department='Staff Department',
            degree='Staff Degree',
            start_year=2025,
            profile_picture=self.VALID_IMAGE
        )
        
        self.forum1 = Forum.objects.create(
            name='Test Forum 1',
            description='First test forum',
            slug='test-forum-1'
        )
        self.forum2 = Forum.objects.create(
            name='Test Forum 2',
            description='Second test forum',
            slug='test-forum-2'
        )

        self.thread = Thread.objects.create(
            title='Test Thread',
            topic='Test topic',
            forum=self.forum1,
            author=self.user,
            slug='test-thread'
        )

    def tearDown(self):
        profile_pics_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pictures')
        if os.path.exists(profile_pics_dir):
            for filename in os.listdir(profile_pics_dir):
                if filename.startswith('default'):
                    file_path = os.path.join(profile_pics_dir, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)

    def _create_long_string(self, length):
        return 'a' * length

    def test_forum_list_loads(self):
        response = self.client.get(reverse('main:forum_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/forum_list.html')

    def test_forum_list_title_block(self):
        response = self.client.get(reverse('main:forum_list'))
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    Forums' in content,
            f"{FAILURE_HEADER}Title block does not contain 'TheUniHub - Forums'.{FAILURE_FOOTER}"
        )

    def test_forum_list_jumbotron_heading(self):
        response = self.client.get(reverse('main:forum_list'))
        content = response.content.decode()
        self.assertTrue(
            '<h1 class="jumbotron-heading">Forums</h1>' in content,
            f"{FAILURE_HEADER}Jumbotron heading 'Forums' is missing.{FAILURE_FOOTER}"
        )

    def test_forum_list_jumbotron_subheading(self):
        response = self.client.get(reverse('main:forum_list'))
        content = response.content.decode()
        self.assertTrue(
            'Discuss everything university and student-life related on <span class="company-name"><i>TheUniHub</i></span>.' in content,
            f"{FAILURE_HEADER}Jumbotron subheading is missing or incorrect.{FAILURE_FOOTER}"
        )
    
    def test_forum_list_jumbotron_info(self):
        response = self.client.get(reverse('main:forum_list'))
        content = response.content.decode()
        self.assertTrue(
            'You can start threads and posts on any of the forums.' in content,
            f"{FAILURE_HEADER}Jumbotron info text is missing.{FAILURE_FOOTER}"
        )

    def test_forum_lists(self):
        response = self.client.get(reverse('main:forum_list'))
        self.assertContains(response, 'Test Forum 1')
        self.assertContains(response, 'First test forum')
        self.assertContains(response, 'Test Forum 2')
        self.assertContains(response, 'Second test forum')

    def test_forum_lists_empty(self):
        Forum.objects.all().delete()
        response = self.client.get(reverse('main:forum_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Forums on <span class="company-name"><i>TheUniHub</i></span>')
        self.assertNotContains(response, 'list-group-item')

    def test_forum_list_staff_create_button(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:forum_list'))
        self.assertContains(response, 'Create Forum')

    def test_forum_loads(self):
        response = self.client.get(reverse('main:thread_list', kwargs={'forum_name_slug': 'test-forum-1'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/thread_list.html')
    
    def test_forum_title_block(self):
        response = self.client.get(reverse('main:thread_list', kwargs={'forum_name_slug': 'test-forum-1'}))
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    \n        Threads in Test Forum 1' in content,
            f"{FAILURE_HEADER}Title block does not contain 'TheUniHub - Threads in Test Forum 1'.{FAILURE_FOOTER}"
        )

    def test_forum_jumbotron_heading(self):
        response = self.client.get(reverse('main:thread_list', kwargs={'forum_name_slug': 'test-forum-1'}))
        content = response.content.decode()
        self.assertTrue(
            '<h1 class="jumbotron-heading">Test Forum 1</h1>' in content,
            f"{FAILURE_HEADER}Jumbotron heading 'Test Forum 1' is missing.{FAILURE_FOOTER}"
        )

    def test_forum_jumbotron_subheading(self):
        response = self.client.get(reverse('main:thread_list', kwargs={'forum_name_slug': 'test-forum-1'}))
        content = response.content.decode()
        self.assertTrue(
            'Search, view, and post on this forum.' in content,
            f"{FAILURE_HEADER}Jumbotron subheading is missing or incorrect.{FAILURE_FOOTER}"
        )
    
    def test_forum_jumbotron_info(self):
        response = self.client.get(reverse('main:thread_list', kwargs={'forum_name_slug': 'test-forum-1'}))
        content = response.content.decode()
        self.assertTrue(
            'First test forum' in content,
            f"{FAILURE_HEADER}Jumbotron info text is missing.{FAILURE_FOOTER}"
        )

    def test_forum_staff_edit_button(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:thread_list', kwargs={'forum_name_slug': 'test-forum-1'}))
        self.assertContains(response, 'Edit Forum')

    def test_forum_unknown(self):
        response = self.client.get(reverse('main:thread_list', kwargs={'forum_name_slug': 'nonexistent'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Forum not found')
        self.assertNotContains(response, 'Threads in')

    def test_forum_no_threads(self):
        Thread.objects.all().delete()
        response = self.client.get(reverse('main:thread_list', kwargs={'forum_name_slug': 'test-forum-1'}))
        self.assertContains(response, 'No threads in this forum yet')

    def test_add_forum_access_denied_unauthenticated(self):
        response = self.client.get(reverse('main:add_forum'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={reverse("main:add_forum")}')

    def test_add_forum_access_denied_non_staff(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:add_forum'))
        self.assertRedirects(response, reverse('main:index'))

    def test_add_forum_access_staff(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:add_forum'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/add_forum.html')
        self.assertContains(response, 'Create a Forum')
        self.assertContains(response, 'Create Forum')

    def test_add_forum_form_submission(self):
        self.client.login(username='staffuser', password='staffpass123')
        data = {
            'name': 'New Forum',
            'description': 'New forum description'
        }
        response = self.client.post(reverse('main:add_forum'), data)
        self.assertRedirects(response, reverse('main:index'))
        new_forum = Forum.objects.get(name='New Forum')
        self.assertEqual(new_forum.description, 'New forum description')
        self.assertEqual(new_forum.slug, 'new-forum')

    def test_add_forum_form_missing_field(self):
        self.client.login(username='staffuser', password='staffpass123')
        data = {
            'name': '',
            'description': 'Description only'
        }
        response = self.client.post(reverse('main:add_forum'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<strong>Error:</strong> Please correct the issues below')
        self.assertContains(response, 'This field is required')
        self.assertFalse(Forum.objects.filter(description='Description only').exists())

    def test_add_forum_form_invalid_name(self):
        self.client.login(username='staffuser', password='staffpass123')
        data = {
            'name': self._create_long_string(500),
            'description': 'Valid description'
        }
        response = self.client.post(reverse('main:add_forum'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ensure this value has at most 250 characters')
        self.assertFalse(Forum.objects.filter(description='Valid description').exists())

    def test_add_forum_form_invalid_description(self):
        self.client.login(username='staffuser', password='staffpass123')
        data = {
            'name': 'Valid Name',
            'description': self._create_long_string(5000)
        }
        response = self.client.post(reverse('main:add_forum'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ensure this value has at most 2000 characters')
        self.assertFalse(Forum.objects.filter(name='Valid Name').exists())

    def test_add_forum_form_duplicate_name(self):
        self.client.login(username='staffuser', password='staffpass123')
        data = {
            'name': 'Test Forum 1',
            'description': 'Different description'
        }
        response = self.client.post(reverse('main:add_forum'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Forum with this Name already exists')
        self.assertEqual(Forum.objects.filter(name='Test Forum 1').count(), 1)

    def test_edit_forum_access_denied_unauthenticated(self):
        response = self.client.get(reverse('main:edit_forum', kwargs={'forum_name_slug': 'test-forum-1'}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={reverse("main:edit_forum", kwargs={"forum_name_slug": "test-forum-1"})}')

    def test_edit_forum_access_denied_non_staff(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:edit_forum', kwargs={'forum_name_slug': 'test-forum-1'}))
        self.assertRedirects(response, reverse('main:thread_list', kwargs={'forum_name_slug': 'test-forum-1'}))

    def test_edit_forum_access_staff(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:edit_forum', kwargs={'forum_name_slug': 'test-forum-1'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/edit_forum.html')
        self.assertContains(response, 'Edit Forum: Test Forum 1')
        self.assertContains(response, 'value="Test Forum 1"')
        self.assertContains(response, 'First test forum')

    def test_edit_forum_unknown(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:edit_forum', kwargs={'forum_name_slug': 'nonexistent'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Forum Not Found')

    def test_edit_forum_form_submission(self):
        self.client.login(username='staffuser', password='staffpass123')
        data = {
            'name': 'Updated Forum',
            'description': 'Updated description'
        }
        response = self.client.post(reverse('main:edit_forum', kwargs={'forum_name_slug': 'test-forum-1'}), data)
        self.assertRedirects(response, reverse('main:thread_list', kwargs={'forum_name_slug': 'updated-forum'}))
        self.forum1.refresh_from_db()
        self.assertEqual(self.forum1.name, 'Updated Forum')
        self.assertEqual(self.forum1.description, 'Updated description')
        self.assertEqual(self.forum1.slug, 'updated-forum')

    def test_edit_forum_form_invalid_name(self):
        self.client.login(username='staffuser', password='staffpass123')
        data = {
            'name': '',
            'description': 'New description'
        }
        response = self.client.post(reverse('main:edit_forum', kwargs={'forum_name_slug': 'test-forum-1'}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        self.forum1.refresh_from_db()
        self.assertEqual(self.forum1.name, 'Test Forum 1')

    def test_edit_forum_form_duplicate_name(self):
        self.client.login(username='staffuser', password='staffpass123')
        data = {
            'name': 'Test Forum 2',
            'description': 'Trying to duplicate'
        }
        response = self.client.post(reverse('main:edit_forum', kwargs={'forum_name_slug': 'test-forum-1'}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Forum with this Name already exists')
        self.forum1.refresh_from_db()
        self.assertEqual(self.forum1.name, 'Test Forum 1')

    def test_delete_forum_access_denied_unauthenticated(self):
        response = self.client.get(reverse('main:delete_forum', kwargs={'forum_name_slug': 'test-forum-1'}))
        self.assertEqual(response.status_code, 302)

    def test_delete_forum_access_denied_non_staff(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:delete_forum', kwargs={'forum_name_slug': 'test-forum-1'}))
        self.assertRedirects(response, reverse('main:thread_list', kwargs={'forum_name_slug': 'test-forum-1'}))

    def test_delete_forum_access_staff(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:delete_forum', kwargs={'forum_name_slug': 'test-forum-1'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/delete_forum.html')
        self.assertContains(response, 'Test Forum 1')

    def test_delete_forum_unknown(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:delete_forum', kwargs={'forum_name_slug': 'nonexistent'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Forum Not Found')

    def test_delete_forum_submission(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.post(reverse('main:delete_forum', kwargs={'forum_name_slug': 'test-forum-1'}))
        self.assertRedirects(response, reverse('main:forum_list'))
        self.assertFalse(Forum.objects.filter(slug='test-forum-1').exists())
        self.assertFalse(Thread.objects.filter(slug='test-thread').exists())

class ThreadManagementTests(TestCase):
    
    def setUp(self):
        
        self.VALID_IMAGE = SimpleUploadedFile(
            name='default.jpg',
            content=open(os.path.join(settings.BASE_DIR, 'default.jpg'), 'rb').read(),
            content_type='image/jpg'
        )

        self.client = Client()

        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            bio='Test bio',
            university='edinburgh',
            school='Test School',
            department='Test Department',
            degree='Test Degree',
            start_year=2025,
            profile_picture=self.VALID_IMAGE
        )

        self.staff_user = User.objects.create_user(username='staffuser', password='staffpass123', is_staff=True)
        self.staff_profile = UserProfile.objects.create(
            user=self.staff_user,
            first_name='Staff',
            last_name='User',
            bio='Staff bio',
            university='edinburgh',
            school='Staff School',
            department='Staff Department',
            degree='Staff Degree',
            start_year=2025,
            profile_picture=self.VALID_IMAGE
        )

        self.forum = Forum.objects.create(
            name='Test Forum',
            description='Test forum description',
            slug='test-forum'
        )

        self.thread = Thread.objects.create(
            title='Test Thread',
            topic='Test topic',
            forum=self.forum,
            author=self.user,
            slug='test-thread'
        )

    def tearDown(self):
        profile_pics_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pictures')
        if os.path.exists(profile_pics_dir):
            for filename in os.listdir(profile_pics_dir):
                if filename.startswith('default'):
                    file_path = os.path.join(profile_pics_dir, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)

    def _create_long_string(self, length):
        return 'a' * length

    def test_thread_loads(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/thread_detail.html')

    def test_thread_title_block(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        content = response.content.decode()
        self.assertTrue(
            'TheUniHub - \n    \n        Test Thread' in content,
            f"{FAILURE_HEADER}Title block does not contain 'TheUniHub - Test Thread'.{FAILURE_FOOTER}"
        )

    def test_thread_jumbotron_heading(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        content = response.content.decode()
        self.assertTrue(
            '<h1 class="jumbotron-heading">Test Thread</h1>' in content,
            f"{FAILURE_HEADER}Jumbotron heading 'Test Thread' is missing.{FAILURE_FOOTER}"
        )

    def test_thread_jumbotron_subheading(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        content = response.content.decode()
        self.assertTrue(
            'Search, view, and post on this thread.' in content,
            f"{FAILURE_HEADER}Jumbotron subheading is missing or incorrect.{FAILURE_FOOTER}"
        )

    def test_thread_jumbotron_detail(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        content = response.content.decode()
        self.assertTrue(
            'Started by' in content,
            f"{FAILURE_HEADER}Jumbotron detail 'Started by' is missing.{FAILURE_FOOTER}"
        )

    def test_thread_content(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertContains(response, 'Test Thread')
        self.assertContains(response, 'Test topic')
        self.assertContains(response, 'Started by')

    def test_thread_unknown(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'nonexistent'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Thread not found')
        self.assertNotContains(response, 'Test Thread')

    def test_thread_save_button_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertContains(response, 'Save')

    def test_thread_edit_button_author(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertContains(response, 'Edit Thread')

    def test_thread_edit_button_non_author(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertNotContains(response, 'Edit Thread')

    def test_create_thread_access_denied_unauthenticated(self):
        response = self.client.get(reverse('main:create_thread', kwargs={'forum_name_slug': 'test-forum'}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={reverse("main:create_thread", kwargs={"forum_name_slug": "test-forum"})}')

    def test_create_thread_access_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:create_thread', kwargs={'forum_name_slug': 'test-forum'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/create_thread.html')
        self.assertContains(response, 'Create a Thread')
        self.assertContains(response, 'Start Thread')

    def test_create_thread_form_submission(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'New Thread',
            'topic': 'New topic'
        }
        response = self.client.post(reverse('main:create_thread', kwargs={'forum_name_slug': 'test-forum'}), data)
        self.assertRedirects(response, reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'new-thread'}))
        new_thread = Thread.objects.get(title='New Thread')
        self.assertEqual(new_thread.topic, 'New topic')
        self.assertEqual(new_thread.forum, self.forum)
        self.assertEqual(new_thread.author, self.user)
        self.assertEqual(new_thread.slug, 'new-thread')

    def test_create_thread_form_missing_field(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': '',
            'topic': 'Topic only'
        }
        response = self.client.post(reverse('main:create_thread', kwargs={'forum_name_slug': 'test-forum'}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<strong>Error:</strong> Please correct the issues below')
        self.assertContains(response, 'This field is required')
        self.assertFalse(Thread.objects.filter(topic='Topic only').exists())

    def test_create_thread_form_invalid_title(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': self._create_long_string(500),
            'topic': 'Valid topic'
        }
        response = self.client.post(reverse('main:create_thread', kwargs={'forum_name_slug': 'test-forum'}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ensure this value has at most 250 characters')
        self.assertFalse(Thread.objects.filter(topic='Valid topic').exists())

    def test_create_thread_form_banned_words(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'Fuck This',
            'topic': 'Test topic'
        }
        response = self.client.post(reverse('main:create_thread', kwargs={'forum_name_slug': 'test-forum'}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The title of your thread contains innappropriate content')
        self.assertFalse(Thread.objects.filter(title='Fuck This').exists())

    def test_create_thread_form_search(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'query': 'test search',
            'search': 'Search online'
        }
        response = self.client.post(reverse('main:create_thread', kwargs={'forum_name_slug': 'test-forum'}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Search for related threads')
        self.assertContains(response, 'test search')

    def test_edit_thread_access_denied_unauthenticated(self):
        response = self.client.get(reverse('main:edit_thread', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={reverse("main:edit_thread", kwargs={"forum_name_slug": "test-forum", "thread_title_slug": "test-thread"})}')

    def test_edit_thread_access_denied_non_author(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:edit_thread', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertRedirects(response, reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))

    def test_edit_thread_access_author(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:edit_thread', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/edit_thread.html')
        self.assertContains(response, 'Edit Thread: Test Thread')
        self.assertContains(response, 'Save Changes')

    def test_edit_thread_unknown(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:edit_thread', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'nonexistent'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Thread Not Found')

    def test_edit_thread_form_submission(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'Updated Thread',
            'topic': 'Updated topic'
        }
        response = self.client.post(reverse('main:edit_thread', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}), data)
        self.assertRedirects(response, reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'updated-thread'}))
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.title, 'Updated Thread')
        self.assertEqual(self.thread.topic, 'Updated topic')
        self.assertEqual(self.thread.slug, 'updated-thread')

    def test_edit_thread_form_missing_field(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': '',
            'topic': 'New topic'
        }
        response = self.client.post(reverse('main:edit_thread', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.title, 'Test Thread')
    
    def test_edit_thread_form_banned_words(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'Shit Thread',
            'topic': 'Test topic'
        }
        response = self.client.post(reverse('main:edit_thread', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'The title of your thread contains innappropriate content')
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.title, 'Test Thread')

    def test_delete_thread_access_denied_unauthenticated(self):
        response = self.client.get(reverse('main:delete_thread', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertEqual(response.status_code, 302)

    def test_delete_thread_access_denied_non_author(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:delete_thread', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertRedirects(response, reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))

    def test_delete_thread_access_author(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:delete_thread', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/delete_thread.html')
        self.assertContains(response, 'Delete Thread: Test Thread')
        self.assertContains(response, 'Yes, delete my thread')

    def test_delete_thread_unknown(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:delete_thread', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'nonexistent'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Thread Not Found')

    def test_delete_thread_submission(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('main:delete_thread', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertRedirects(response, reverse('main:thread_list', kwargs={'forum_name_slug': 'test-forum'}))
        self.assertFalse(Thread.objects.filter(slug='test-thread').exists())

    def test_save_thread_unauthenticated(self):
        response = self.client.post(reverse('main:save_thread', kwargs={'thread_title_slug': 'test-thread'}))
        self.assertEqual(response.status_code, 302)

    def test_save_thread_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('main:save_thread', kwargs={'thread_title_slug': 'test-thread'}))
        self.assertRedirects(response, reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.user_profile.refresh_from_db()
        self.assertIn(self.thread, self.user_profile.saved_threads.all())

    def test_unsave_thread_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        self.user_profile.saved_threads.add(self.thread)
        response = self.client.post(reverse('main:save_thread', kwargs={'thread_title_slug': 'test-thread'}))
        self.assertRedirects(response, reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.user_profile.refresh_from_db()
        self.assertNotIn(self.thread, self.user_profile.saved_threads.all())

class PostManagementTests(TestCase):
    
    def setUp(self):
        
        self.VALID_IMAGE = SimpleUploadedFile(
            name='default.jpg',
            content=open(os.path.join(settings.BASE_DIR, 'default.jpg'), 'rb').read(),
            content_type='image/jpg'
        )

        self.client = Client()

        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            bio='Test bio',
            university='edinburgh',
            school='Test School',
            department='Test Department',
            degree='Test Degree',
            start_year=2025,
            profile_picture=self.VALID_IMAGE
        )

        self.other_user = User.objects.create_user(username='otheruser', password='otherpass123')
        self.other_profile = UserProfile.objects.create(
            user=self.other_user,
            first_name='Other',
            last_name='User',
            bio='Other bio',
            university='edinburgh',
            school='Other School',
            department='Other Department',
            degree='Other Degree',
            start_year=2025,
            profile_picture=self.VALID_IMAGE
        )

        self.forum = Forum.objects.create(
            name='Test Forum',
            description='Test forum description',
            slug='test-forum'
        )

        self.thread = Thread.objects.create(
            title='Test Thread',
            topic='Test topic',
            forum=self.forum,
            author=self.user,
            slug='test-thread'
        )

        self.post = Post.objects.create(
            thread=self.thread,
            author=self.user,
            content='Test post',
            written_on=timezone.now()
        )

    def tearDown(self):
        profile_pics_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pictures')
        if os.path.exists(profile_pics_dir):
            for filename in os.listdir(profile_pics_dir):
                if filename.startswith('default'):
                    file_path = os.path.join(profile_pics_dir, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)

    def _create_long_string(self, length):
        return 'a' * length

    def test_posts_load_on_thread(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/thread_detail.html')
        self.assertContains(response, 'Discussion')
        self.assertContains(response, 'Test post')
        self.assertContains(response, 'testuser')

    def test_posts_empty_on_thread(self):
        self.client.login(username='testuser', password='testpass123')
        Post.objects.all().delete()
        response = self.client.get(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No posts currently in this thread.')

    def test_post_edit_button_author(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertContains(response, '<a href="/main/forum/test-forum/thread/test-thread/1/edit_post/"')

    def test_post_edit_button_non_author(self):
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.get(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertNotContains(response, '<a href="/main/forum/test-forum/thread/test-thread/1/edit_post/"')

    def test_add_post_unauthenticated(self):
        response = self.client.get(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertRedirects(response, '/accounts/login/?next=/main/forum/test-forum/thread/test-thread/')

    def test_add_post_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertContains(response, 'Add a Post')
        self.assertContains(response, 'Post')

    def test_add_post_form_submission(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'content': 'New post'}
        response = self.client.post(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}), data)
        self.assertRedirects(response, reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        new_post = Post.objects.get(content='New post')
        self.assertEqual(new_post.author, self.user)
        self.assertEqual(new_post.thread, self.thread)

    def test_add_post_form_missing_field(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'content': ''}
        response = self.client.post(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        self.assertFalse(Post.objects.filter(content='').exists())

    def test_add_post_form_banned_words(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'content': 'Fuck you'}
        response = self.client.post(
            reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}),
            data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.filter(content='Fuck you').exists())

    def test_edit_post_access_denied_unauthenticated(self):
        response = self.client.get(reverse('main:edit_post', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread', 'post_id': self.post.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={reverse("main:edit_post", kwargs={"forum_name_slug": "test-forum", "thread_title_slug": "test-thread", "post_id": self.post.id})}')

    def test_edit_post_access_denied_non_author(self):
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.get(reverse('main:edit_post', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread', 'post_id': self.post.id}))
        self.assertRedirects(response, reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))

    def test_edit_post_access_author(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:edit_post', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread', 'post_id': self.post.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/edit_post.html')
        self.assertContains(response, 'Edit Post: Test Thread')
        self.assertContains(response, 'Save Changes')

    def test_edit_post_time_limit_exceeded(self):
        self.client.login(username='testuser', password='testpass123')
        self.post.written_on = timezone.now() - timedelta(days=1)
        self.post.save()
        response = self.client.get(reverse('main:edit_post', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread', 'post_id': self.post.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You\'re not within the time limit to edit this post')

    def test_edit_post_unknown(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:edit_post', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread', 'post_id': 999}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Thread/Post Not Found')

    def test_edit_post_form_submission(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'content': 'Updated post'}
        response = self.client.post(reverse('main:edit_post', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread', 'post_id': self.post.id}), data)
        self.assertRedirects(response, reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.post.refresh_from_db()
        self.assertEqual(self.post.content, 'Updated post')
        self.assertIsNotNone(self.post.edited_on)

    def test_edit_post_form_missing_field(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'content': ''}
        response = self.client.post(reverse('main:edit_post', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread', 'post_id': self.post.id}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        self.post.refresh_from_db()
        self.assertEqual(self.post.content, 'Test post')

    def test_edit_post_form_banned_words(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'content': 'Fuck you'}
        response = self.client.post(reverse('main:edit_post', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread', 'post_id': self.post.id}), data)
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.content, 'Test post')

    def test_delete_post_access_denied_unauthenticated(self):
        response = self.client.get(reverse('main:delete_post', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread', 'post_id': self.post.id}))
        self.assertEqual(response.status_code, 302)

    def test_delete_post_access_denied_non_author(self):
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.get(reverse('main:delete_post', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread', 'post_id': self.post.id}))
        self.assertRedirects(response, reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))

    def test_delete_post_access_author(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:delete_post', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread', 'post_id': self.post.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/delete_post.html')
        self.assertContains(response, 'Delete Post: Test Thread')
        self.assertContains(response, 'Yes, delete my post')

    def test_delete_post_time_limit_exceeded(self):
        self.client.login(username='testuser', password='testpass123')
        self.post.written_on = timezone.now() - timedelta(days=1)
        self.post.save()
        response = self.client.get(reverse('main:delete_post', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread', 'post_id': self.post.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You\'re not within the time limit to delete this post')

    def test_delete_post_unknown(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:delete_post', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread', 'post_id': 999}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Thread/Post Not Found')

    def test_delete_post_submission(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('main:delete_post', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread', 'post_id': self.post.id}))
        self.assertRedirects(response, reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

class PollManagementTests(TestCase):
    
    def setUp(self):
        
        self.VALID_IMAGE = SimpleUploadedFile(
            name='default.jpg',
            content=open(os.path.join(settings.BASE_DIR, 'default.jpg'), 'rb').read(),
            content_type='image/jpg'
        )

        self.client = Client()

        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            bio='Test bio',
            university='edinburgh',
            school='Test School',
            department='Test Department',
            degree='Test Degree',
            start_year=2025,
            profile_picture=self.VALID_IMAGE
        )

        self.staff_user = User.objects.create_user(username='staffuser', password='staffpass123', is_staff=True)
        self.staff_profile = UserProfile.objects.create(
            user=self.staff_user,
            first_name='Staff',
            last_name='User',
            bio='Staff bio',
            university='edinburgh',
            school='Staff School',
            department='Staff Department',
            degree='Staff Degree',
            start_year=2025,
            profile_picture=self.VALID_IMAGE
        )

        self.forum = Forum.objects.create(
            name='Test Forum',
            description='Test forum description',
            slug='test-forum'
        )
        self.thread = Thread.objects.create(
            title='Test Thread',
            topic='Test topic',
            forum=self.forum,
            author=self.user,
            slug='test-thread'
        )

        self.post = Post.objects.create(
            thread=self.thread,
            author=self.user,
            content='Test post',
            written_on=timezone.now()
        )

    def tearDown(self):
        profile_pics_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pictures')
        if os.path.exists(profile_pics_dir):
            for filename in os.listdir(profile_pics_dir):
                if filename.startswith('test_image'):
                    file_path = os.path.join(profile_pics_dir, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)

    def test_poll_display_on_thread(self):
        self.client.login(username='testuser', password='testpass123')
        poll = Poll(thread=self.thread, question='Test Poll')
        poll.save(skip_validation=True)
        PollOption.objects.create(poll=poll, option_text='Option 1')
        PollOption.objects.create(poll=poll, option_text='Option 2')
        poll.full_clean()
        response = self.client.get(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Poll: Test Poll')
        self.assertContains(response, 'Option 1 (0 votes)')
        self.assertContains(response, 'Option 2 (0 votes)')
        self.assertContains(response, 'Vote')

    def test_no_poll_on_thread(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There is no poll for this thread yet.')

    def test_add_poll_button_staff(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertContains(response, '<a href="/main/forum/test-forum/thread/test-thread/add_poll/"')

    def test_add_poll_button_non_staff(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertNotContains(response, '<a href="/main/forum/test-forum/thread/test-thread/add_poll/"')

    def test_add_poll_access_denied_unauthenticated(self):
        response = self.client.get(reverse('main:add_poll', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={reverse("main:add_poll", kwargs={"forum_name_slug": "test-forum", "thread_title_slug": "test-thread"})}')

    def test_add_poll_access_denied_non_staff(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('main:add_poll', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertRedirects(response, reverse('main:index'))

    def test_add_poll_access_staff(self):
        self.client.login(username='staffuser', password='staffpass123')
        response = self.client.get(reverse('main:add_poll', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/add_poll.html')
        self.assertContains(response, 'Add a Poll in Test Thread')
        self.assertContains(response, 'Poll Question')
        self.assertContains(response, 'Poll Options')
        self.assertContains(response, 'Create Poll')

    def test_add_poll_form_submission(self):
        self.client.login(username='staffuser', password='staffpass123')
        data = {
            'question': 'Test Poll Question',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '2',
            'form-MAX_NUM_FORMS': '5',
            'form-0-option_text': 'Option 1',
            'form-1-option_text': 'Option 2',
        }
        response = self.client.post(reverse('main:add_poll', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}), data)
        self.assertRedirects(response, reverse('main:thread_detail', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}))
        poll = Poll.objects.get(question='Test Poll Question')
        self.assertEqual(poll.thread, self.thread)
        options = PollOption.objects.filter(poll=poll)
        self.assertEqual(options.count(), 2)
        self.assertEqual(options[0].option_text, 'Option 1')
        self.assertEqual(options[1].option_text, 'Option 2')

    def test_add_poll_form_missing_question(self):
        self.client.login(username='staffuser', password='staffpass123')
        data = {
            'question': '',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '2',
            'form-MAX_NUM_FORMS': '5',
            'form-0-option_text': 'Option 1',
            'form-1-option_text': 'Option 2',
        }
        response = self.client.post(reverse('main:add_poll', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        self.assertFalse(Poll.objects.filter(question='').exists())

    def test_add_poll_form_too_few_options(self):
        self.client.login(username='staffuser', password='staffpass123')
        data = {
            'question': 'Test Poll Question',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '2',
            'form-MAX_NUM_FORMS': '5',
            'form-0-option_text': 'Option 1',
        }
        response = self.client.post(reverse('main:add_poll', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A poll must have at least 2 options.')
        self.assertFalse(Poll.objects.filter(question='Test Poll Question').exists())

    def test_add_poll_form_too_many_options(self):
        self.client.login(username='staffuser', password='staffpass123')
        data = {
            'question': 'Test Poll Question',
            'form-TOTAL_FORMS': '6',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '2',
            'form-MAX_NUM_FORMS': '5',
            'form-0-option_text': 'Option 1',
            'form-1-option_text': 'Option 2',
            'form-2-option_text': 'Option 3',
            'form-3-option_text': 'Option 4',
            'form-4-option_text': 'Option 5',
            'form-5-option_text': 'Option 6',
        }
        response = self.client.post(reverse('main:add_poll', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A poll cannot have more than 5 options.')
        self.assertFalse(Poll.objects.filter(question='Test Poll Question').exists())

    def test_add_poll_form_unknown_thread(self):
        self.client.login(username='staffuser', password='staffpass123')
        data = {
            'question': 'Test Poll Question',
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '2',
            'form-MAX_NUM_FORMS': '5',
            'form-0-option_text': 'Option 1',
            'form-1-option_text': 'Option 2',
        }
        response = self.client.post(reverse('main:add_poll', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'unknown-thread'}), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Thread not found')

    def test_vote_poll_unauthenticated(self):
        self.client.login(username='staffuser', password='staffpass123')
        poll = Poll(thread=self.thread, question='Test Poll')
        poll.save(skip_validation=True)
        option1 = PollOption.objects.create(poll=poll, option_text='Option 1')
        PollOption.objects.create(poll=poll, option_text='Option 2')
        poll.full_clean()
        self.client.logout()
        data = {'option_id': option1.id}
        response = self.client.post(reverse('main:poll_vote', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={reverse("main:poll_vote", kwargs={"forum_name_slug": "test-forum", "thread_title_slug": "test-thread"})}')

    def test_vote_poll_authenticated(self):
        self.client.login(username='staffuser', password='staffpass123')
        poll = Poll(thread=self.thread, question='Test Poll')
        poll.save(skip_validation=True)
        option1 = PollOption.objects.create(poll=poll, option_text='Option 1')
        PollOption.objects.create(poll=poll, option_text='Option 2')
        poll.full_clean()
        data = {'option_id': option1.id}
        response = self.client.post(reverse('main:poll_vote', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success', 'votes': 1})
        option1.refresh_from_db()
        self.assertEqual(option1.votes, 1)
        poll.refresh_from_db()
        self.assertTrue(self.staff_user in poll.voted_users.all())

    def test_vote_poll_already_voted(self):
        self.client.login(username='staffuser', password='staffpass123')
        poll = Poll(thread=self.thread, question='Test Poll')
        poll.save(skip_validation=True)
        option1 = PollOption.objects.create(poll=poll, option_text='Option 1')
        option2 = PollOption.objects.create(poll=poll, option_text='Option 2')
        poll.full_clean()
        poll.voted_users.add(self.staff_user)
        data = {'option_id': option2.id}
        response = self.client.post(reverse('main:poll_vote', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'status': 'error', 'message': 'You have already voted on this poll!'})
        option2.refresh_from_db()
        self.assertEqual(option2.votes, 0)

    def test_vote_poll_invalid_option(self):
        self.client.login(username='testuser', password='testpass123')
        poll = Poll(thread=self.thread, question='Test Poll')
        poll.save(skip_validation=True)
        PollOption.objects.create(poll=poll, option_text='Option 1')
        PollOption.objects.create(poll=poll, option_text='Option 2')
        poll.full_clean()
        data = {'option_id': 999}
        response = self.client.post(reverse('main:poll_vote', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {'status': 'error', 'message': 'Poll option not found'})

    def test_vote_poll_no_poll(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'option_id': 1}
        response = self.client.post(reverse('main:poll_vote', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'test-thread'}), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {'status': 'error', 'message': 'Poll not found'})

    def test_vote_poll_invalid_thread(self):
        self.client.login(username='testuser', password='testpass123')
        data = {'option_id': 1}
        response = self.client.post(reverse('main:poll_vote', kwargs={'forum_name_slug': 'test-forum', 'thread_title_slug': 'unknown-thread'}), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {'status': 'error', 'message': 'Thread not found'})