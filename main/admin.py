from django.contrib import admin
from main.models import Category, Article, Comment, Forum, Thread, Post, Poll, PollOption, UserProfile

# Admin class for the Category model
class CategoryAdmin(admin.ModelAdmin):

    # Automatically generates slug field based on the category name
    prepopulated_fields = {'slug': ('name',)}

    # Orders categories alphabetically by name
    ordering = ['name']

# Admin class for the Article model
class ArticleAdmin(admin.ModelAdmin):

    # Automatically generates slug field based on the article title
    prepopulated_fields = {'slug': ('title',)}

    # Display these fields in the administration view to show related category, title, and author
    list_display = ('category', 'title', 'author')

    # Orders articles alphabetically by title
    ordering = ['title']

# Admin class for the Comment model
class CommentAdmin(admin.ModelAdmin):

    # Display these fields in the administration view to show related article, author, and content
    list_display = ('article', 'author', 'content')

# Admin class for Forum model
class ForumAdmin(admin.ModelAdmin):

    # Automatically generates slug field based on the forum name
    prepopulated_fields = {'slug': ('name',)}

    # Orders forums alphabetically by name
    ordering = ['name']

# Admin class for the Thread model
class ThreadAdmin(admin.ModelAdmin):

    # Automatically generates slug field based on the thread title
    prepopulated_fields = {'slug': ('title',)}

    # Display these fields in the administration view to show related forum, title, and author
    list_display = ('forum', 'title', 'author')

    # Orders threads alphabetically by title
    ordering = ['title']

# Admin class for the Post model
class PostAdmin(admin.ModelAdmin):

    # Display these fields in the administration view to show related thread, author, and content
    list_display = ('thread', 'author', 'content')

# Register each model with the Django administration view using their admin classes; if they have been defined
admin.site.register(Category, CategoryAdmin)

admin.site.register(Article, ArticleAdmin)

admin.site.register(Comment, CommentAdmin)

admin.site.register(Forum, ForumAdmin)

admin.site.register(Thread, ThreadAdmin)

admin.site.register(Post, PostAdmin)

# Register the following models using their default administration view settings
admin.site.register(Poll)

admin.site.register(PollOption)

admin.site.register(UserProfile)