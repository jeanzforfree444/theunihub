from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone

UNIVERSITY_CHOICES = [
    # Scottish Universities
    ('aberdeen', 'University of Aberdeen'),
    ('abertay', 'Abertay University'),
    ('caledonian', 'Glasgow Caledonian University'),
    ('dundee', 'University of Dundee'),
    ('edinburgh', 'University of Edinburgh'),
    ('glasgow', 'University of Glasgow'),
    ('heriot_watt', 'Heriot-Watt University'),
    ('napier', 'Edinburgh Napier University'),
    ('qmu', 'Queen Margaret University'),
    ('rgu', 'Robert Gordon University'),
    ('st_andrews', 'University of St. Andrews'),
    ('stirling', 'University of Stirling'),
    ('strathclyde', 'University of Strathclyde'),
    ('uws', 'University of the West of Scotland'),
    ('uhi', 'University of the Highlands and Islands'),
    
    # Northern Irish Universities
    ('queens', "Queen's University of Belfast"),
    ('ulster', 'University of Ulster'),
    
    # Welsh Universities
    ('aberystwyth', 'Aberystwyth University'),
    ('bangor', 'Bangor University'),
    ('cardiff', 'Cardiff University'),
    ('cardiff_met', 'Cardiff Metropolitan University'),
    ('usw', 'University of South Wales'),
    ('swansea', 'Swansea University'),
    ('tsd', 'University of Wales Trinity Saint David'),
    ('wrexham', 'Wrexham University'),

    # English & International Universities
    ('oxford', 'University of Oxford'),
    ('cambridge', 'University of Cambridge'),
    ('imperial', 'Imperial College London'),
    ('ucl', 'University College London'),
    ('kcl', "King's College London"),
    ('lse', 'London School of Economics'),
    ('harvard', 'Harvard University'),
    ('mit', 'Massachusetts Institute of Technology'),
    ('stanford', 'Stanford University'),
    ('berkeley', 'University of California, Berkeley'),
]

def validate_image_file(value):

    if not value.name.endswith(('.png', '.jpg', '.jpeg')):

        raise ValidationError('Only PNG, JPG, and JPEG files are allowed.')

#Model representing a category for articles or content
class Category(models.Model):
    #Maximum lengths for category name and description
    NAME_MAX_LENGTH = 150

    DESCRIPTION_MAX_LENGTH = 1000

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True) #Category must be unique

    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH)

    views = models.IntegerField(default=0)

    points = models.IntegerField(default=0)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        #Automatically generate a slug from the category name before saving
        self.slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)

    class Meta:
        # Default ordering: alphabetically by name
        ordering = ['name']

        # Plural display name in the admin interface
        verbose_name_plural = 'Categories'

    def __str__(self):
        # String representation of category
        return self.name

# Model representing an article
class Article(models.Model):
    # Maximum lengths for articles title, summary, and content
    TITLE_MAX_LENGTH = 500

    SUMMARY_MAX_LENGTH = 2000

    CONTENT_MAX_LENGTH = 20000

    # Link the article to category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    title = models.CharField(max_length=TITLE_MAX_LENGTH)

    summary = models.CharField(max_length=SUMMARY_MAX_LENGTH)

    content = models.CharField(max_length=CONTENT_MAX_LENGTH)

    article_picture = models.ImageField(upload_to='article_images', blank=True)

    views = models.IntegerField(default=0)

    points = models.IntegerField(default=0)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='articles', null=True, blank=True)

    created_on = models.DateTimeField(default=timezone.now)

    updated_on = models.DateTimeField(null=True, blank=True)

    # Optional field linking the article to a university
    related_university = models.CharField(max_length=250, choices=UNIVERSITY_CHOICES, blank=True, null=True)

    slug = models.SlugField(unique=True) # URL-friendly version of the title

    def save(self, *args, **kwargs):
        # Generate a slug if not already set
        if not self.slug:
        
            self.slug = slugify(self.title)

        # If the article already exists in the database (has a primary key)
        if self.pk:
        
            original = Article.objects.get(pk=self.pk)
            # Check if only 'views' or 'points' have changed and other key fields remain the same
            if (self.views != original.views or self.points != original.points) and all(
                getattr(self, field) == getattr(original, field)
                for field in ['title', 'summary', 'content', 'article_picture', 'category', 'author']
            ):
                # Update only the 'views' and 'points' fields without modifying updated_on
                super(Article, self).save(update_fields=['views', 'points'])
                
                return

            # Set updated timestamp if any other field has changed
            self.updated_on = timezone.now()

        # Call the superclass save method to handle actual saving
        super(Article, self).save(*args, **kwargs)

    class Meta:

        ordering = ['title']

        verbose_name_plural = 'Articles'

    def __str__(self):

        return f'{self.title} by {self.author} in {self.category.name}'

# Model representing a comment on an article
class Comment(models.Model):
    # Maximum length for the comment content
    CONTENT_MAX_LENGTH = 2000

    article = models.ForeignKey(Article, on_delete=models.CASCADE) # The article to which this comment belongs

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    content = models.CharField(max_length=CONTENT_MAX_LENGTH)

    written_on = models.DateTimeField(default=timezone.now)

    edited_on = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # If updating an existing comment, set the edited timestamp to current time
        if self.pk:

            self.edited_on = timezone.now()

        super(Comment, self).save(*args, **kwargs)

    class Meta:

        ordering = ['-written_on']

        verbose_name_plural = 'Comments'

    def __str__(self):

        return f'Comment by {self.author} on {self.article.title}'

# Model representing a forum
class Forum(models.Model):
    # Maximum length for the forum name and description
    NAME_MAX_LENGTH = 250

    DESCRIPTION_MAX_LENGTH = 2000
    
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True) # Unique name of the forum
    
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        # Automatically generate a slug from the forum name before saving
        self.slug = slugify(self.name)

        super(Forum, self).save(*args, **kwargs)

    class Meta:

        ordering = ['name']

        verbose_name_plural = 'Forums'

    def __str__(self):
    
        return self.name

# Model representing a thread within a forum
class Thread(models.Model):

    TITLE_MAX_LENGTH = 250

    TOPIC_MAX_LENGTH = 20000
    
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=TITLE_MAX_LENGTH)

    topic = models.CharField(max_length=TOPIC_MAX_LENGTH)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    started_on = models.DateTimeField(default=timezone.now)
    
    updated_on = models.DateTimeField(null=True, blank=True)

    related_university = models.CharField(max_length=250, choices=UNIVERSITY_CHOICES, blank=True, null=True)

    slug = models.SlugField(unique=True) # URL-friendly version of the thread title

    def save(self, *args, **kwargs):
        # Automatically generate a slug from the thread title before saving
        self.slug = slugify(self.title)
        # If updating an existing thread, update the 'updated_on' timestamp
        if self.pk:

            self.updated_on = timezone.now()

        super(Thread, self).save(*args, **kwargs)

    class Meta:

        ordering = ['title']

        verbose_name_plural = 'Threads'

    def __str__(self):
        # String representation showing title, author, and the forum it belongs to
        return f'{self.title} by {self.author} in {self.forum.name}'

# Model representing a post within a thread
class Post(models.Model):
    # Maximum length for the post content
    CONTENT_MAX_LENGTH = 20000
    
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE) # The thread to which the post belongs
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) # The author of the post

    content = models.CharField(max_length=CONTENT_MAX_LENGTH)
    
    written_on = models.DateTimeField(default=timezone.now)

    edited_on = models.DateTimeField(null=True, blank=True)
    
    likes = models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        # If updating an existing post, set the edited timestamp to the current time
        if self.pk:

            self.edited_on = timezone.now()

        super(Post, self).save(*args, **kwargs)

    class Meta:

        ordering = ['-written_on']

        verbose_name_plural = 'Posts'

    def __str__(self):
        # String representation showing the post's author and the thread title it belongs to
        return f'Post by {self.author} on {self.thread.title}'

# Model representing a poll attached to a thread
class Poll(models.Model):
    # Maximum length for poll question
    QUESTION_MAX_LENGTH = 250
    
    thread = models.OneToOneField(Thread, on_delete=models.CASCADE) # One-to-one relationship with a thread
    
    question = models.CharField(max_length=QUESTION_MAX_LENGTH)

    class Meta:

        ordering = ['question']

        verbose_name_plural = 'Polls'

    def __str__(self):
        # String representation showing the poll question and the thread title
        return f'{self.question} on {self.thread.title}'

# Model representing an option in a poll
class PollOption(models.Model):
    # Maximum length for option text
    OPTION_MAX_LENGTH = 250
    
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="options") # Link to the poll; allows reverse lookup with "options"
    
    option_text = models.CharField(max_length=OPTION_MAX_LENGTH)
    
    votes = models.PositiveIntegerField(default=0)

    voted_users = models.ManyToManyField(User, blank=True)

    class Meta:

        ordering = ['option_text']

        verbose_name_plural = 'Poll Options'

    def __str__(self):
        # String representation showing option text, poll question, and vote count
        return f'{self.option_text} on {self.poll.question} with {self.votes} vote(s)'

# Model representing a user profile with additional information
class UserProfile(models.Model):
    # Maximum lengths for first and last names, biography, university, school, department, and degree fields
    NAME_MAX_LENGTH = 100

    BIO_MAX_LENGTH = 150

    UNIVERSITY_MAX_LENGTH = 250

    SCHOOL_MAX_LENGTH = 250

    DEPARTMENT_MAX_LENGTH = 250

    DEGREE_MAX_LENGTH = 250

    user = models.OneToOneField(User, on_delete=models.CASCADE) # One-to-one relationship with the built-in User model

    first_name = models.CharField(max_length=NAME_MAX_LENGTH)

    last_name = models.CharField(max_length=NAME_MAX_LENGTH)

    bio = models.CharField(max_length=BIO_MAX_LENGTH)

    university = models.CharField(max_length=UNIVERSITY_MAX_LENGTH, choices=UNIVERSITY_CHOICES, null=True, blank=True)

    school = models.CharField(max_length=SCHOOL_MAX_LENGTH, null=True, blank=True)

    department = models.CharField(max_length=DEPARTMENT_MAX_LENGTH, null=True, blank=True)

    degree = models.CharField(max_length=DEGREE_MAX_LENGTH, null=True, blank=True)

    start_year = models.IntegerField(default=timezone.now().year, null=True, blank=True)

    profile_picture = models.ImageField(upload_to='profile_pictures', null=False)

    favourite_articles = models.ManyToManyField(Article, blank=True, related_name="favourited_by") # Articles favourited by the user - many-to-many relationship

    saved_threads = models.ManyToManyField(Thread, blank=True, related_name="saved_by") # Threads saved by the user - many-to-many relationship

    class Meta:

        ordering = ['user']

        verbose_name_plural = 'Profiles'

    def __str__(self):
        # String representation of the user profile
        return f"{self.first_name} {self.last_name} (@{self.user.username})"