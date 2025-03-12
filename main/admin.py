from django.contrib import admin
from main.models import Category, Article, Comment, Forum, Thread, Post, Poll, PollOption, UserProfile

class CategoryAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('name',)}

    ordering = ['name']
    
class ArticleAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}

    list_display = ('title', 'category', 'author')

    ordering = ['title']

class CommentAdmin(admin.ModelAdmin):

    list_display = ('article', 'author', 'content')

class ForumAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('name',)}

    ordering = ['name']

class ThreadAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}

    list_display = ('title', 'forum', 'author')

    ordering = ['title']

class PostAdmin(admin.ModelAdmin):

    list_display = ('thread', 'author', 'content')

admin.site.register(Category, CategoryAdmin)

admin.site.register(Article, ArticleAdmin)

admin.site.register(Comment, CommentAdmin)

admin.site.register(Forum, ForumAdmin)

admin.site.register(Thread, ThreadAdmin)

admin.site.register(Post, PostAdmin)

admin.site.register(Poll)

admin.site.register(PollOption)

admin.site.register(UserProfile)