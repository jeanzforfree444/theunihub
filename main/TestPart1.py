#Tests for The UniHub app


#In order to run these test, please copy this module to your THEUNIHUB/theunihub/ directory
#once this is complete, run $ python manage.py test main.TestPart1

#The tests will then be run, and the output displayed

import os
import importlib
from django.urls import reverse
from django.test import TestCase
from django.conf import settings

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}THEUNIHUB TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class TestPart1StructureTests(TestCase):

    def setUp(self):

        #simple tests to probe out file data structure
        #also have test to show we have added theunihub to our list of INSTALLED_APPS

        #get working directiory
        self.project_base_dir = os.getcwd()
        #check to see if there is a main directory
        self.main_app_dir =os.path.join(self.project_base_dir, 'main')

    def test_project_created(self):

        #tests weather the theunihub configuration directory is present and correct
        
        #checks if the theunihub directory exists
        directory_exists = os.path.isdir(os.path.join(self.project_base_dir, 'theunihub'))

        #checks if the URL module exists
        urls_module_exits = os.path.isfile(os.path.join(self.project_base_dir, 'theunihub', 'urls.py'))

        #runs the directory_exists check
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}Your theunihub directory does not seem to exist please check if the right name is being used.{FAILURE_FOOTER}")

        #runs the urls_module_exists check
        self.assertTrue(urls_module_exits, f"{FAILURE_HEADER}Your projects urls.py module doesnt seem to exist. Did you use the startproject command?{FAILURE_FOOTER}")

    def test_theunihub_app_created(self):
        directory_exists = os.path.isdir(self.main_app_dir)

        is_python_package = os.path.isfile(os.path.join(self.main_app_dir, '__init__.py'))
        views_module_exists = os.path.isfile(os.path.join(self.main_app_dir, 'views.py'))

        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The main app directory does not exist. Did you use the startapp command?{FAILURE_FOOTER}")
        self.assertTrue(is_python_package, f"{FAILURE_HEADER}The main directory is missing files. Did you use the startapp command?{FAILURE_FOOTER}")
        self.assertTrue(views_module_exists, f"{FAILURE_HEADER}The main directory is missing files. Did you use the startapp command?{FAILURE_FOOTER}")

    def test_theunihub_has_urls_modules(self):

        module_exists = os.path.isfile(os.path.join(self.main_app_dir, "urls.py"))
        self.assertTrue(module_exists, f"{FAILURE_HEADER}The TheUniHub app's urls.py module is missing.{FAILURE_FOOTER}")

    def test_is_theunihub_app_configurated(self):

        is_app_configurated = 'main' in settings.INSTALLED_APPS

        self.assertTrue(is_app_configurated, f"{FAILURE_HEADER}The theunihub app is missing from your setting's INSTALLED APPS list.{FAILURE_FOOTER}")
    
    class IndexPageTests(TestCase):

        def setUp(self):

            self.views_modules = importlib.import_module('main.views')
            self.views_modules_listing = dir(self.views_modules)

            self.project_urls_module = importlib.import_module('theunihub.urls')
        
        def test_view_exists(self):

            name_exists = 'index' in self.views_modules_listing
            is_callable = callable(self.views_modules.index)

            self.assertTrue(name_exists, f"{FAILURE_HEADER}The index() view for theunihub does not exist.{FAILURE_FOOTER}")
            self.assertTrue(is_callable, f"{FAILURE_HEADER}Check that the index() view is correctly installed. It doesnt seem to be a function!{FAILURE_FOOTER}")
        
        def test_mappings_exists(self):

            index_mapping_exists = False
        
            for mapping in self.project_urls_module.urlpatterns:
                if hasattr(mapping, 'name'):
                    if mapping.name == 'index':
                        index_mapping_exists = True
        
            self.assertTrue(index_mapping_exists, f"{FAILURE_HEADER}The index URL mapping could not be found. Check your PROJECT'S urls.py module.{FAILURE_FOOTER}")
            self.assertEquals(reverse('rango:index'), '/rango/', f"{FAILURE_HEADER}The index URL lookup failed. Check main urls.py module. You're missing something in there.{FAILURE_FOOTER}")
    
    def test_response(self):

        response = self.client.get(reverse('main:index'))
        
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Requesting the index page failed. Check your URLs and view.{FAILURE_FOOTER}")
    
    def test_for_about_hyperlink(self):
       
        response = self.client.get(reverse('main:index'))
        
        single_quotes_check = '<a href=\'/main/about/\'>About</a>' in response.content.decode() or '<a href=\'/main/about\'>About</a>' in response.content.decode() 
        double_quotes_check = '<a href="/main/about/">About</a>' in response.content.decode() or '<a href="/main/about">About</a>' in response.content.decode()
        
        self.assertTrue(single_quotes_check or double_quotes_check, f"{FAILURE_HEADER}We couldn't find the hyperlink to the /rango/about/ URL in your index page. Check that it appears EXACTLY as in the book.{FAILURE_FOOTER}")

class Chapter3AboutPageTests(TestCase):
   
    def setUp(self):
        self.views_module = importlib.import_module('main.views')
        self.views_module_listing = dir(self.views_module)
    
    def test_view_exists(self):
        
        name_exists = 'about' in self.views_module_listing
        is_callable = callable(self.views_module.about)
        
        self.assertTrue(name_exists, f"{FAILURE_HEADER}We couldn't find the view for your about view! It should be called about().{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}Check you have defined your about() view correctly. We can't execute it.{FAILURE_FOOTER}")
    
    def test_mapping_exists(self):
        
        self.assertEquals(reverse('main:about'), '/main/about/', f"{FAILURE_HEADER}Your about URL mapping is either missing or mistyped.{FAILURE_FOOTER}")
    
    def test_response(self):
        
        response = self.client.get(reverse('main:about'))
        
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}When requesting the about view, the server did not respond correctly. Is everything correct in your URL mappings and the view?{FAILURE_FOOTER}")
    
    def test_for_index_hyperlink(self):
       
        response = self.client.get(reverse('main:about'))
        
        single_quotes_check = '<a href=\'/main/\'>Index</a>' in response.content.decode()
        double_quotes_check = '<a href="/main/">Index</a>' in response.content.decode()
        
        self.assertTrue(single_quotes_check or double_quotes_check, f"{FAILURE_HEADER}We could not find a hyperlink back to the index page in your about view. Check your about.html template, and try again.{FAILURE_FOOTER}")



