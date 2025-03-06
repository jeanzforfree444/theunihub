import os
import django
import random
from django.contrib.auth.models import User
from rango.models import Category, Article, Comment, Forum, Thread, Post, Poll, PollOption, UserProfile
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'theunihub.settings')

def create_users():
    """Creates sample users and returns a list of user instances."""

    users = []
    
    user_data = [
        {'username': 'euan_galloway', 'first_name': 'Euan', 'last_name': 'Galloway', 'email': 'euan_galloway@hotmail.com', 'password': 'password123', 'staff': False, 'bio': 'I helped with the marketing of this company!'},
        {'username': 'phoebe6504', 'first_name': 'Phoebe', 'last_name': 'Hope', 'email': 'phoebe_hope@gmail.com', 'password': 'password123', 'staff': True, 'bio': ''},
        {'username': 'urangoo143', 'first_name': 'Urangoo', 'last_name': 'Ganzorig', 'email': 'urangoo_ganzorig@live.com', 'password': 'password123', 'staff': False},
    ]
    
    for data in user_data:
    
        user, created = User.objects.get_or_create(username=data['username'], email=data['email'], is_staff=data['staff'])
    
        if created:
            
            user.set_password(data['password'])
            
            user.save()
            
            profile = UserProfile.objects.create(
                user=user,
                first_name=data['first_name'],
                last_name=data['last_name'],
                bio=data['bio'],
                university=random.choice([uni[0] for uni in Category.UNIVERSITY_CHOICES]),
                profile_picture="profile_pictures/default.jpg"
            )

            users.append(user)
    
    return users

def create_categories():
    """Creates sample categories."""
    category_data = [
        {"name": "Computer Science", "description": "Discussion about CS topics."},
        {"name": "Mathematics", "description": "All things numbers and equations."},
        {"name": "Physics", "description": "Talk about quantum mechanics, relativity, etc."},
    ]
    
    categories = []
    for data in category_data:
        category, created = Category.objects.get_or_create(name=data["name"], description=data["description"])
        categories.append(category)
    
    return categories

def create_articles(users, categories):
    """Creates sample articles."""
    articles = []
    article_data = [
        {"title": "Introduction to AI", "summary": "Basics of Artificial Intelligence.", "content": "Full AI article content..."},
        {"title": "Quantum Computing", "summary": "An overview of quantum mechanics in computing.", "content": "Full quantum computing article..."},
        {"title": "Data Science Trends", "summary": "Trends in data science for 2025.", "content": "Full data science trends article..."},
    ]
    
    for data in article_data:
        article = Article.objects.create(
            category=random.choice(categories),
            title=data["title"],
            summary=data["summary"],
            content=data["content"],
            views=random.randint(10, 500),
            points=random.randint(1, 100),
            author=random.choice(users),
            created_on=timezone.now(),
        )
        articles.append(article)
    
    return articles

def create_comments(users, articles):
    """Creates sample comments for articles."""
    comment_data = [
        "Great article! Thanks for sharing.",
        "I found this very helpful.",
        "This topic is fascinating!",
    ]
    
    for article in articles:
        for user in users:
            Comment.objects.create(
                article=article,
                author=user,
                content=random.choice(comment_data),
                written_on=timezone.now(),
            )

def create_forums():
    """Creates sample forums."""
    forums = []
    forum_data = [
        {"name": "General Discussion", "description": "Talk about anything."},
        {"name": "Tech Talk", "description": "Discuss the latest in technology."},
        {"name": "Academic Advice", "description": "Ask for and share academic advice."},
    ]
    
    for data in forum_data:
        forum = Forum.objects.create(name=data["name"], description=data["description"], created_on=timezone.now())
        forums.append(forum)
    
    return forums

def create_threads(users, forums):
    """Creates sample threads in forums."""
    threads = []
    thread_data = [
        {"title": "What's the best programming language?", "forum": "Tech Talk"},
        {"title": "Tips for first-year students?", "forum": "Academic Advice"},
        {"title": "Is AI going to take over jobs?", "forum": "General Discussion"},
    ]
    
    for data in thread_data:
        forum = Forum.objects.get(name=data["forum"])
        thread = Thread.objects.create(
            forum=forum,
            title=data["title"],
            author=random.choice(users),
            created_on=timezone.now(),
        )
        threads.append(thread)
    
    return threads

def create_posts(users, threads):
    """Creates posts within threads."""
    post_data = [
        "I totally agree!",
        "Interesting point, but I think...",
        "Can you elaborate on that?",
    ]
    
    for thread in threads:
        for user in users:
            Post.objects.create(
                thread=thread,
                author=user,
                content=random.choice(post_data),
                created_on=timezone.now(),
            )

def create_favourites(users, articles):
    """Adds random articles to users' favourites."""
    for user in users:
        profile = user.userprofile
        fav_articles = random.sample(articles, k=random.randint(1, len(articles)))
        profile.favourite_articles.set(fav_articles)

django.setup()

def populate():
    """Main function to populate the database."""

    print("Populating TheUniHub database...")

    # Create users
    users = create_users()
    print(f"Created {len(users)} users.")

    # Create categories
    categories = create_categories()
    print(f"Created {len(categories)} categories.")

    # Create articles
    articles = create_articles(users, categories)
    print(f"Created {len(articles)} articles.")

    # Create comments
    create_comments(users, articles)
    print("Created comments.")

    # Create forums
    forums = create_forums()
    print(f"Created {len(forums)} forums.")

    # Create threads
    threads = create_threads(users, forums)
    print(f"Created {len(threads)} threads.")

    # Create posts
    create_posts(users, threads)
    print("Created posts.")

    # Add favourite articles
    create_favourites(users, articles)
    print("Assigned favourite articles.")

    print("Database population complete.")

if __name__ == '__main__':
    
    populate()