from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

# List of university choices for associating users and content with specific institutions
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
    """
    Validates that an uploaded image file has an allowed extension.
    
    Args:
        value: The file object being uploaded.
    
    Raises:
        ValidationError: If the file extension is not .png, .jpg, or .jpeg.
    """

    if not value.name.endswith(('.png', '.jpg', '.jpeg')):

        raise ValidationError('Only PNG, JPG, and JPEG files are allowed.')

# Model representing a category for organising articles
class Category(models.Model):

    # Maximum lengths for category name and description
    NAME_MAX_LENGTH = 150

    DESCRIPTION_MAX_LENGTH = 1000

    # Unique name of the category, limited to 150 characters
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True) #Category must be unique

    # Detailed description of the category, up to 1000 characters
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH)

    # Tracks the number of views this category has received, defaults to 0
    views = models.IntegerField(default=0)

    # Points system for ranking or engagement, defaults to 0
    points = models.IntegerField(default=0)

    # URL-friendly slug, automatically generated from the name, must be unique
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to auto-generate a slug from the category name.
        
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

        self.slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)

    class Meta:

        # Orders categories alphabetically by name in queries and admin interface
        ordering = ['name']

        # Sets the plural name displayed in the Django admin interface
        verbose_name_plural = 'Categories'

    def __str__(self):
        """Returns a string representation of the category, which is its name."""
        
        return self.name

# Model representing an article within the platform
class Article(models.Model):

    # Maximum lengths for articles title, summary, and content
    TITLE_MAX_LENGTH = 500

    SUMMARY_MAX_LENGTH = 2000

    CONTENT_MAX_LENGTH = 20000

    # Foreign key linking the article to a Category; deletes article if category is deleted
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # Unique title of the article, limited to 500 characters
    title = models.CharField(max_length=TITLE_MAX_LENGTH, unique=True)

    # Brief summary of the article, up to 2000 characters
    summary = models.CharField(max_length=SUMMARY_MAX_LENGTH)

    # Full content of the article, up to 20000 characters
    content = models.CharField(max_length=CONTENT_MAX_LENGTH)

    # Optional image associated with the article, stored in 'article_images' directory
    article_image = models.ImageField(upload_to='article_images', validators=[validate_image_file], null=True, blank=True)

    # Tracks the number of views for the article, defaults to 0
    views = models.IntegerField(default=0)

    # Points for engagement or ranking, defaults to 0
    points = models.IntegerField(default=0)

    # Author of the article, set to null if the user is deleted
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='articles', null=True, blank=True)

    # Timestamp of when the article was created, defaults to current time
    created_on = models.DateTimeField(default=timezone.now)

    # Timestamp of the last update, null if not updated
    updated_on = models.DateTimeField(null=True, blank=True)

    # Optional university related to the article, chosen from UNIVERSITY_CHOICES
    related_university = models.CharField(max_length=250, choices=UNIVERSITY_CHOICES, blank=True, null=True)

    # Unique URL-friendly slug generated from the title, must be unique
    slug = models.SlugField(unique=True) # URL-friendly version of the title

    def save(self, *args, **kwargs):
        """
        Custom save method to generate a slug and handle update timestamps.
        
        - Generates a slug from the title if not already set.
        - Updates 'updated_on' only if significant fields change (not just views/points).
        
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        
        if not self.slug:
        
            self.slug = slugify(self.title)

        if self.pk: # Check if this is an update to an existing article
        
            original = Article.objects.get(pk=self.pk)

            if (self.views != original.views or self.points != original.points) and all(
                getattr(self, field) == getattr(original, field)
                for field in ['title', 'summary', 'content', 'article_image', 'category', 'author']
            ):
                
                # Update only views and points without changing updated_on
                super(Article, self).save(update_fields=['views', 'points'])
                
                return

            # Set updated_on for any other significant change
            self.updated_on = timezone.now()

        super(Article, self).save(*args, **kwargs)

    class Meta:

        # Orders articles alphabetically by title
        ordering = ['title']

        # Sets the plural name in the admin interface
        verbose_name_plural = 'Articles'

    def __str__(self):
        """Returns a string representation of the article with title, author, and category."""

        return f'{self.title} by {self.author} in {self.category.name}'

# Model representing a comment on an article
class Comment(models.Model):

    # Maximum length for the comment content
    CONTENT_MAX_LENGTH = 2000

    # Foreign key linking the comment to an Article; deletes comment if article is deleted
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    # Author of the comment, set to null if the user is deleted
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Text content of the comment, up to 2000 characters
    content = models.CharField(max_length=CONTENT_MAX_LENGTH)

    # Timestamp of when the comment was written, defaults to current time
    written_on = models.DateTimeField(default=timezone.now)

    # Timestamp of the last edit, null if not edited
    edited_on = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Custom save method to update the 'edited_on' timestamp when a comment is modified.
        
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

        if self.pk: # If this is an update

            self.edited_on = timezone.now()

        super(Comment, self).save(*args, **kwargs)

    class Meta:

        # Orders comments by written date, newest first
        ordering = ['-written_on']

        # Sets the plural name in the admin interface
        verbose_name_plural = 'Comments'

    def __str__(self):
        """Returns a string representation of the comment with author and article title."""

        return f'Comment by {self.author} on {self.article.title}'

# Model representing a forum for discussion topics
class Forum(models.Model):

    # Maximum lengths for the forums name and description
    NAME_MAX_LENGTH = 250

    DESCRIPTION_MAX_LENGTH = 2000
    
    # Unique name of the forum, limited to 250 characters
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True) # Unique name of the forum
    
    # Detailed description of the forum’s purpose, up to 2000 characters
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH)

    # URL-friendly slug generated from the name, must be unique
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        """
        Custom save method to auto-generate a slug from the forum name.
        
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

        self.slug = slugify(self.name)

        super(Forum, self).save(*args, **kwargs)

    class Meta:

        # Orders forums alphabetically by name
        ordering = ['name']

        # Sets the plural name in the admin interface
        verbose_name_plural = 'Forums'

    def __str__(self):
    
        return self.name

# Model representing a thread within a forum
class Thread(models.Model):

    # Maximum lengths for the threads title and topic
    TITLE_MAX_LENGTH = 250

    TOPIC_MAX_LENGTH = 2000
    
    # Foreign key linking the thread to a Forum; deletes thread if forum is deleted
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    
    # Unique title of the thread, limited to 250 characters
    title = models.CharField(max_length=TITLE_MAX_LENGTH, unique=True)

    # Main topic of the thread, up to 2000 characters
    topic = models.CharField(max_length=TOPIC_MAX_LENGTH)
    
    # Author of the thread, set to null if the user is deleted
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Timestamp of when the thread was started, defaults to current time
    started_on = models.DateTimeField(default=timezone.now)
    
    # Timestamp of the last update, null if not updated
    updated_on = models.DateTimeField(null=True, blank=True)

    # Optional university related to the thread, chosen from UNIVERSITY_CHOICES
    related_university = models.CharField(max_length=250, choices=UNIVERSITY_CHOICES, blank=True, null=True)

    # URL-friendly slug generated from the title, must be unique 
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        """
        Custom save method to generate a slug and update the 'updated_on' timestamp.
        
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

        self.slug = slugify(self.title)

        if self.pk: # If this is an update

            self.updated_on = timezone.now()

        super(Thread, self).save(*args, **kwargs)

    class Meta:

        # Orders threads alphabetically by title
        ordering = ['title']

        # Sets the plural name in the admin interface
        verbose_name_plural = 'Threads'

    def __str__(self):
        """Returns a string representation of the thread with title, author, and forum."""
        
        return f'{self.title} by {self.author} in {self.forum.name}'

# Model representing a post within a thread
class Post(models.Model):

    # Maximum length for the post content
    CONTENT_MAX_LENGTH = 5000
    
    # Foreign key linking the post to a Thread; deletes post if thread is deleted
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE) # The thread to which the post belongs
    
    # Author of the post, set to null if the user is deleted
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) # The author of the post

    # Text content of the post, up to 5000 characters
    content = models.CharField(max_length=CONTENT_MAX_LENGTH)
    
    # Timestamp of when the post was written, defaults to current time
    written_on = models.DateTimeField(default=timezone.now)

    # Timestamp of the last edit, null if not edited
    edited_on = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        """
        Custom save method to update the 'edited_on' timestamp when a post is modified.
        
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

        if self.pk: # If this is an update

            self.edited_on = timezone.now()

        super(Post, self).save(*args, **kwargs)

    class Meta:

        # Orders posts by written date, newest first
        ordering = ['-written_on']

        # Sets the plural name in the admin interface
        verbose_name_plural = 'Posts'

    def __str__(self):
        """Returns a string representation of the post with author and thread title."""

        return f'Post by {self.author} on {self.thread.title}'

# Model representing a poll attached to a thread
class Poll(models.Model):
    
    # Maximum length for the poll question
    QUESTION_MAX_LENGTH = 250
    
    # Poll must have a least 2 and at most 5 options
    MIN_OPTIONS = 2
    
    MAX_OPTIONS = 5

    # One-to-one link to a Thread; deletes poll if thread is deleted
    thread = models.OneToOneField('Thread', on_delete=models.CASCADE)
    
    # Question on the poll, limited to 250 characters
    question = models.CharField(max_length=QUESTION_MAX_LENGTH)
    
    # Users who have voted in this poll, many-to-many relationship
    voted_users = models.ManyToManyField(User, blank=True)

    class Meta:
    
        # Orders polls alphabetically by question
        ordering = ['question']
    
        # Sets the plural name in the admin interface
        verbose_name_plural = 'Polls'

    def __str__(self):
        """Returns a string representation of the poll with question and thread title."""

        return f'{self.question} on {self.thread.title}'

    def clean(self):
        """
        Validates the number of poll options during model validation.
        
        Raises:
            ValidationError: If the number of options is less than MIN_OPTIONS or more than MAX_OPTIONS.
        """

        option_count = self.options.count() if self.pk else 0

        if option_count < self.MIN_OPTIONS:

            raise ValidationError(f'A poll must have at least {self.MIN_OPTIONS} options.')

        if option_count > self.MAX_OPTIONS:

            raise ValidationError(f'A poll cannot have more than {self.MAX_OPTIONS} options.')

    def save(self, *args, **kwargs):
        """
        Custom save method to enforce validation unless explicitly skipped.
        
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments, including 'skip_validation' to bypass clean().
        """

        skip_validation = kwargs.pop('skip_validation', False)
        
        if not skip_validation:
        
            self.full_clean()

        super().save(*args, **kwargs)

# Model representing an option on a poll
class PollOption(models.Model):

    # Maximum length for option text
    OPTION_MAX_LENGTH = 250

    # Foreign key linking the option to a Poll; deletes option if poll is deleted
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="options")

    # Text of the poll option, limited to 250 characters
    option_text = models.CharField(max_length=OPTION_MAX_LENGTH)

    # Number of votes this option has received, defaults to 0
    votes = models.PositiveIntegerField(default=0)

    class Meta:

        # Orders options alphabetically by text
        ordering = ['option_text']

        # Sets the plural name in the admin interface
        verbose_name_plural = 'Poll Options'

    def __str__(self):
        """Returns a string representation of the option with text, question, and vote count."""

        return f'{self.option_text} on {self.poll.question} with {self.votes} vote(s)'

# Model representing a user profile with additional personal and academic information
class UserProfile(models.Model):

    # Maximum lengths for first and last names, biography, university, school, department, and degree fields
    NAME_MAX_LENGTH = 100

    BIO_MAX_LENGTH = 150

    UNIVERSITY_MAX_LENGTH = 250

    SCHOOL_MAX_LENGTH = 250

    DEPARTMENT_MAX_LENGTH = 250

    DEGREE_MAX_LENGTH = 250

    # One-to-one link to the Django User model; deletes profile if user is deleted
    user = models.OneToOneField(User, on_delete=models.CASCADE) # One-to-one relationship with the built-in User model

    # User’s first name, limited to 100 characters
    first_name = models.CharField(max_length=NAME_MAX_LENGTH)

    # User’s last name, limited to 100 characters
    last_name = models.CharField(max_length=NAME_MAX_LENGTH)

    # User biography, up to 150 characters
    bio = models.CharField(max_length=BIO_MAX_LENGTH)

    # User’s university, chosen from UNIVERSITY_CHOICES, optional
    university = models.CharField(max_length=UNIVERSITY_MAX_LENGTH, choices=UNIVERSITY_CHOICES, null=True, blank=True)

    # User’s school within the university, optional
    school = models.CharField(max_length=SCHOOL_MAX_LENGTH, null=True, blank=True)

    # User’s department, optional
    department = models.CharField(max_length=DEPARTMENT_MAX_LENGTH, null=True, blank=True)

    # User’s degree program, optional
    degree = models.CharField(max_length=DEGREE_MAX_LENGTH, null=True, blank=True)

    # Year the user started their studies, defaults to current year
    start_year = models.IntegerField(default=timezone.now().year, null=True, blank=True)

    # Profile picture, stored in 'profile_pictures' directory, required field
    profile_picture = models.ImageField(upload_to='profile_pictures', null=False)

    # Articles favorited by the user, many-to-many relationship
    favourite_articles = models.ManyToManyField(Article, blank=True, related_name="favourited_by") # Articles favourited by the user - many-to-many relationship

    # Threads saved by the user, many-to-many relationship
    saved_threads = models.ManyToManyField(Thread, blank=True, related_name="saved_by") # Threads saved by the user - many-to-many relationship

    class Meta:

        # Orders profiles by the associated user’s username
        ordering = ['user']

        # Sets the plural name in the admin interface
        verbose_name_plural = 'Profiles'

    def __str__(self):
        """Returns a string representation of the profile with full name and username."""

        return f"{self.first_name} {self.last_name} (@{self.user.username})"