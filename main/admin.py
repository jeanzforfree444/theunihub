from django.contrib import admin
from main.models import Category, Article, Comment, Forum, Thread, Post, Poll, PollOption, UserProfile

#Admin class for the category model
class CategoryAdmin(admin.ModelAdmin):
    #Automatically generate 'slug' field based on name field
    prepopulated_fields = {'slug': ('name',)}
    #Order alphabetically
    ordering = ['name']

#Admin class for the Article model
class ArticleAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}
    #Display these fields in the admin list view for better overview
    list_display = ('title', 'category', 'author')

    ordering = ['title']

#Admin class for the Comment Model
class CommentAdmin(admin.ModelAdmin):
    #Display these fields in the admin list view to show related article, author and content
    list_display = ('article', 'author', 'content')

#Admin class for Forum model
class ForumAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('name',)}

    ordering = ['name']

#Admin class for te Thread Model
class ThreadAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}
    #Display these fields in the admin list to show thread title, association forum, and author
    list_display = ('title', 'forum', 'author')

    ordering = ['title']

#Custom admin class for the Post Model
class PostAdmin(admin.ModelAdmin):

    list_display = ('thread', 'author', 'content')

#Register models with the Django admin interface using their custom admin classes wheer defined
admin.site.register(Category, CategoryAdmin) #Register Category with custom settings

admin.site.register(Article, ArticleAdmin)

admin.site.register(Comment, CommentAdmin)

admin.site.register(Forum, ForumAdmin)

admin.site.register(Thread, ThreadAdmin)

admin.site.register(Post, PostAdmin)

#Register the following models using their default admin settings
admin.site.register(Poll)

admin.site.register(PollOption)

admin.site.register(UserProfile)