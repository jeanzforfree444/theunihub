from django.urls import path
from main import views

app_name = 'main' # Name of Django app

urlpatterns = [
    # Home and static pages
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('mission_vision/', views.MissionVisionView.as_view(), name='mission_vision'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('values/', views.ValuesView.as_view(), name='values'),
    path('faqs/', views.FAQsView.as_view(), name='faqs'),

    # Stats and user account management
    path('stats/', views.StatsView.as_view(), name='show_stats'),
    path('register_profile/', views.RegisterProfileView.as_view(), name='register_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('users/', views.ListUsersView.as_view(), name='list_users'),
    path('delete_account_confirm/', views.DeleteAccountConfirmationView.as_view(), name='delete_account_confirmation'),
    path('delete_account/', views.DeleteAccountView.as_view(), name='delete_account'),

    # Category management
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<slug:category_name_slug>/', views.ShowCategoryView.as_view(), name='show_category'),
    path('add_category/', views.AddCategoryView.as_view(), name='add_category'),
    path('category/<slug:category_name_slug>/edit_category/', views.EditCategoryView.as_view(), name='edit_category'),
    path('category/<slug:category_name_slug>/delete_category/', views.DeleteCategoryView.as_view(), name='delete_category'),
    path('like_category/', views.LikeCategoryView.as_view(), name='like_category'),
    path('dislike_category/', views.DislikeCategoryView.as_view(), name='dislike_category'),

    # Article management
    path('category/<slug:category_name_slug>/article/<slug:article_title_slug>/', views.ShowArticleView.as_view(), name='show_article'),
    path('category/<slug:category_name_slug>/add_article/', views.AddArticleView.as_view(), name='add_article'),
    path('category/<slug:category_name_slug>/article/<slug:article_title_slug>/edit_article/', views.EditArticleView.as_view(), name='edit_article'),
    path('category/<slug:category_name_slug>/article/<slug:article_title_slug>/delete_article/', views.DeleteArticleView.as_view(), name='delete_article'),
    path('category/<slug:category_name_slug>/article/<slug:article_title_slug>/<int:comment_id>/edit_comment/', views.EditCommentView.as_view(), name='edit_comment'),
    path('category/<slug:category_name_slug>/article/<slug:article_title_slug>/<int:comment_id>/delete_comment/', views.DeleteCommentView.as_view(), name='delete_comment'),
    path('like_article/', views.LikeArticleView.as_view(), name='like_article'),
    path('dislike_article/', views.DislikeArticleView.as_view(), name='dislike_article'),
    path('favourite/<slug:article_title_slug>/', views.favourite_article, name='favourite_article'),

    # Suggestions and search
    path('suggest/', views.CategoryForumSuggestionView.as_view(), name='category_forum_suggest'),
    path('search/', views.SearchView.as_view(), name='search_results'),

    # Forum and thread management
    path('forum/', views.ForumListView.as_view(), name='forum_list'),
    path('forum/<slug:forum_name_slug>/', views.ThreadListView.as_view(), name='thread_list'),
    path('add_forum/', views.AddForumView.as_view(), name='add_forum'),
    path('forum/<slug:forum_name_slug>/edit_forum/', views.EditForumView.as_view(), name='edit_forum'),
    path('forum/<slug:forum_name_slug>/delete_forum/', views.DeleteForumView.as_view(), name='delete_forum'),
    path('forum/<slug:forum_name_slug>/create/', views.CreateThreadView.as_view(), name='create_thread'),
    path('forum/<slug:forum_name_slug>/thread/<slug:thread_title_slug>/', views.ThreadDetailView.as_view(), name='thread_detail'),
    path('forum/<slug:forum_name_slug>/thread/<slug:thread_title_slug>/edit_thread/', views.EditThreadView.as_view(), name='edit_thread'),
    path('forum/<slug:forum_name_slug>/thread/<slug:thread_title_slug>/delete_thread/', views.DeleteThreadView.as_view(), name='delete_thread'),
    path('forum/<slug:forum_name_slug>/thread/<slug:thread_title_slug>/<int:post_id>/edit_post/', views.EditPostView.as_view(), name='edit_post'),
    path('forum/<slug:forum_name_slug>/thread/<slug:thread_title_slug>/<int:post_id>/delete_post/', views.DeletePostView.as_view(), name='delete_post'),
    path('save/<slug:thread_title_slug>/', views.save_thread, name='save_thread'),

    # Polls within threads
    path('forum/<slug:forum_name_slug>/thread/<slug:thread_title_slug>/vote/', views.PollVoteView.as_view(), name='poll_vote'),
    path('forum/<slug:forum_name_slug>/thread/<slug:thread_title_slug>/add_poll/', views.AddPollView.as_view(), name='add_poll'),
]