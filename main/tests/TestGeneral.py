from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class TemplateTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_comment_templates(self):
        response = self.client.get(reverse("edit_comment", args=["category_slug", "article_slug", 1]))
        self.assertTemplateUsed(response, "edit_comment.html")

        response = self.client.get(reverse("delete_comment", args=["category_slug", "article_slug", 1]))
        self.assertTemplateUsed(response, "delete_comment.html")

    def test_poll_templates(self):
        response = self.client.get(reverse("poll_vote", args=["forum_slug", "thread_slug"]))
        self.assertTemplateUsed(response, "poll_vote.html")

        response = self.client.get(reverse("add_poll", args=["forum_slug", "thread_slug"]))
        self.assertTemplateUsed(response, "add_poll.html")

    def test_article_templates(self):
        response = self.client.get(reverse("show_article", args=["category_slug", "article_slug"]))
        self.assertTemplateUsed(response, "article.html")

        response = self.client.get(reverse("add_article", args=["category_slug"]))
        self.assertTemplateUsed(response, "add_article.html")

        response = self.client.get(reverse("edit_article", args=["category_slug", "article_slug"]))
        self.assertTemplateUsed(response, "edit_article.html")

        response = self.client.get(reverse("delete_article", args=["category_slug", "article_slug"]))
        self.assertTemplateUsed(response, "delete_article.html")

    def test_edit_templates(self):
        response = self.client.get(reverse("edit_profile"))
        self.assertTemplateUsed(response, "edit_profile.html")

        response = self.client.get(reverse("edit_category", args=["category_slug"]))
        self.assertTemplateUsed(response, "edit_category.html")

        response = self.client.get(reverse("edit_forum", args=["forum_slug"]))
        self.assertTemplateUsed(response, "edit_forum.html")

        response = self.client.get(reverse("edit_post", args=["forum_slug", "thread_slug", 1]))
        self.assertTemplateUsed(response, "edit_post.html")

        response = self.client.get(reverse("edit_thread", args=["forum_slug", "thread_slug"]))
        self.assertTemplateUsed(response, "edit_thread.html")

    def test_auth_templates(self):
        response = self.client.get(reverse("register_profile"))
        self.assertTemplateUsed(response, "profile_registration.html")

        response = self.client.get(reverse("delete_account_confirmation"))
        self.assertTemplateUsed(response, "confirm_delete_account.html")

        response = self.client.get(reverse("delete_account"))
        self.assertTemplateUsed(response, "delete_account.html")

    def test_stats_template(self):
        response = self.client.get(reverse("show_stats"))
        self.assertTemplateUsed(response, "stats.html")

    def test_profile_templates(self):
        response = self.client.get(reverse("profile", args=["testuser"]))
        self.assertTemplateUsed(response, "profile.html")

        response = self.client.get(reverse("list_users"))
        self.assertTemplateUsed(response, "list_users.html")

        response = self.client.get(reverse("saved_threads"))
        self.assertTemplateUsed(response, "saved_threads.html")

    def test_static_templates(self):
        static_pages = [
            ("index", "index.html"),
            ("about", "about.html"),
            ("contact", "contact.html"),
            ("privacy", "privacy.html"),
            ("mission_vision", "mission_vision.html"),
            ("values", "values.html"),
            ("faqs", "faqs.html"),
        ]
        for url_name, template in static_pages:
            response = self.client.get(reverse(url_name))
            self.assertTemplateUsed(response, template)

    def test_forum_templates(self):
        response = self.client.get(reverse("forum_list"))
        self.assertTemplateUsed(response, "forum_list.html")

        response = self.client.get(reverse("thread_list", args=["forum_slug"]))
        self.assertTemplateUsed(response, "thread_list.html")

        response = self.client.get(reverse("thread_detail", args=["forum_slug", "thread_slug"]))
        self.assertTemplateUsed(response, "thread_detail.html")

        response = self.client.get(reverse("create_thread", args=["forum_slug"]))
        self.assertTemplateUsed(response, "create_thread.html")

    def test_search_template(self):
        response = self.client.get(reverse("search_results"))
        self.assertTemplateUsed(response, "search_results.html")
