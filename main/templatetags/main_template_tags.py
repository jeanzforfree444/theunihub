from django import template
from main.models import Category, Forum

register = template.Library()

@register.inclusion_tag('main/categories.html')
def get_category_list(current_category=None):

    return {'categories': Category.objects.all(), 'current_category': current_category}

@register.inclusion_tag('main/favourite_articles.html', takes_context=True)
def get_favourites_list(context, current_article=None):
    
    user = context['request'].user
    
    if user.is_authenticated and hasattr(user, 'userprofile'):
    
        favourites = user.userprofile.favourite_articles.all()
    
    else:
    
        favourites = []

    return {'favourites': favourites, 'current_article': current_article}

@register.inclusion_tag('main/forums.html')
def get_forum_list(current_forum=None):

    return {'forums': Forum.objects.all(), 'current_forum': current_forum}

@register.inclusion_tag('main/saved_threads.html', takes_context=True)
def get_saved_list(context, current_thread=None):
    
    user = context['request'].user
    
    if user.is_authenticated and hasattr(user, 'userprofile'):
    
        saved = user.userprofile.saved_threads.all()
    
    else:
    
        saved = []

    return {'saved': saved, 'current_thread': current_thread}