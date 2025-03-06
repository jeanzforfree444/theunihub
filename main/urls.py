from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<slug:category_name_slug>/', views.ShowCategoryView.as_view(), name='show_category'),
    path('category/<slug:category_name_slug>/article/<slug:article_title_slug>/', views.ShowArticleView.as_view(), name='show_article'),
    path('add_category/', views.AddCategoryView.as_view(), name='add_category'),
    path('category/<slug:category_name_slug>/add_article/', views.AddArticleView.as_view(), name='add_article'),
    path('favourite/<slug:article_slug>/', views.favourite_article, name='favourite_article'),
    path('register_profile/', views.RegisterProfileView.as_view(), name='register_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('profiles/', views.ListProfilesView.as_view(), name='list_profiles'),
    path('delete-confirm/', views.DeleteAccountConfirmationView.as_view(), name='delete_account_confirmation'),
    path('delete-account/', views.DeleteAccountView.as_view(), name='delete_account'),
    path('like_category/', views.LikeCategoryView.as_view(), name='like_category'),
    path('like_article/', views.LikeArticleView.as_view(), name='like_article'),
    path('dislike_category/', views.DislikeCategoryView.as_view(), name='dislike_category'),
    path('dislike_article/', views.DislikeArticleView.as_view(), name='dislike_article'),
    path('suggest/', views.CategorySuggestionView.as_view(), name='suggest'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('mission_vision/', views.MissionVisionView.as_view(), name='mission_vision'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('values/', views.ValuesView.as_view(), name='values'),
    path('stats/', views.StatsView.as_view(), name='show_stats'),
    path('forum/', views.ForumListView.as_view(), name='forum_list'),
    path('add_forum/', views.AddForumView.as_view(), name='add_forum'),
    path('forum/<slug:forum_name_slug>/', views.ThreadListView.as_view(), name='thread_list'),
    path('forum/<slug:forum_name_slug>/create/', views.CreateThreadView.as_view(), name='create_thread'),
    path('forum/<slug:forum_name_slug>/thread/<slug:thread_title_slug>/', views.ThreadDetailView.as_view(), name='thread_detail'),
    path('save/<slug:thread_slug>/', views.save_thread, name='save_thread'),
    path('forum/<slug:forum_name_slug>/thread/<slug:thread_title_slug>/add_poll/', views.AddPollView.as_view(), name='add_poll'),
]