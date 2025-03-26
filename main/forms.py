from django import forms
from main.models import Article, Category, UserProfile, Comment, Forum, Thread, Post, Poll, PollOption, UNIVERSITY_CHOICES
from django.contrib.auth.models import User
from django.utils import timezone

#Form for creating or updating a category instance
class CategoryForm(forms.ModelForm):
    #Define a character field for the category name with a max length specified by the model.
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH, help_text="Please enter the category name:")
    #Define a character field for the category description with a Textarea widget for multi-line input
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 80}), max_length=Category.DESCRIPTION_MAX_LENGTH, help_text="Please enter the category description:")

    class Meta:

        model = Category #This form corresponds to the Category model
        #Includes these specified fields in the form
        fields = ('name', 'description',)

#Form for creating/updating an Article instance
class ArticleForm(forms.ModelForm):
    #Defining character fields
    title = forms.CharField(max_length=Article.TITLE_MAX_LENGTH, help_text="Please enter the title of the article:")

    summary = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 80}), max_length=Article.SUMMARY_MAX_LENGTH, help_text="Please enter the summary of the article:")

    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 80}), max_length=Article.CONTENT_MAX_LENGTH, help_text="Please enter the content of the article:")

    article_image = forms.ImageField(required=False, help_text="Please upload an image for the article:")

    related_university = forms.ChoiceField(choices=[('', 'Select a university (if applicable)')] + UNIVERSITY_CHOICES, required=False, help_text="Enter if this article is related to a specific university:")

    class Meta:

        model = Article

        fields = ('title', 'summary', 'content', 'article_image', 'related_university')
    
class UserForm(forms.ModelForm):
    #Define a password field that uses a PasswordInput widget for secure input
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:

        model = User
              
        fields = ('username', 'email', 'password',)

#Form for creating/updating a UserProfile instance
class UserProfileForm(forms.ModelForm):
    #Define fields
    first_name = forms.CharField(max_length=UserProfile.NAME_MAX_LENGTH, required=True)

    last_name = forms.CharField(max_length=UserProfile.NAME_MAX_LENGTH, required=True)

    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), max_length=UserProfile.BIO_MAX_LENGTH, required=True)

    #Define an integer field for the start year initializing to the current year
    start_year = forms.IntegerField(initial=timezone.now().year, required=False)
    #Define an image field for uploading a profile picture; this field is required
    profile_picture = forms.ImageField(required=True)

    class Meta:

        model = UserProfile
        
        fields = ('first_name', 'last_name', 'bio', 'university', 'school', 'department', 'degree', 'start_year', 'profile_picture',)

class CommentForm(forms.ModelForm):

    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 80}), max_length=Comment.CONTENT_MAX_LENGTH, help_text="Please enter your comment:")

    class Meta:

        model = Comment

        fields = ['content']

#Form for creating/updating a Forum instance
class ForumForm(forms.ModelForm):
    #Define fields
    name = forms.CharField(max_length=Forum.NAME_MAX_LENGTH, help_text="Please enter the forum name:")

    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 80}), max_length=Forum.DESCRIPTION_MAX_LENGTH, help_text="Please enter the forum description:")
    #Define a hidden character field for the slug , which is not required for user input
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:

        model = Forum

        fields = ('name', 'description',)


#Forum for creating or updating a Thread instance
class ThreadForm(forms.ModelForm):
    #Define fields
    title = forms.CharField(max_length=Thread.TITLE_MAX_LENGTH, help_text="Enter the title of your thread:")

    topic = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 80}), max_length=Thread.TOPIC_MAX_LENGTH, help_text="Enter the topic of your thread:")
    
    related_university = forms.ChoiceField(choices=[('', 'Select a university (if applicable)')] + UNIVERSITY_CHOICES, required=False, help_text="Enter if this thread is related to a specific university:")

    class Meta:

        model = Thread
        
        fields = ('title', 'topic', 'related_university')

#Form for creating/updating a Post instance
class PostForm(forms.ModelForm):
    #Define a character field for the post content using a Textarea widget
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 80}), max_length=Post.CONTENT_MAX_LENGTH, help_text="Enter your post:")

    class Meta:
        
        model = Post
        
        fields = ['content']

class PollForm(forms.Form):

    question = forms.CharField(max_length=Poll.QUESTION_MAX_LENGTH, help_text="Enter the poll question:")

    class Meta:
    
        model = Poll
    
        fields = ['question']

#Form for creating/updating a PollOption instance
class PollOptionForm(forms.ModelForm):
    #Define a character field for the poll option text
    option_text = forms.CharField(max_length=PollOption.OPTION_MAX_LENGTH, help_text="Enter an option for the poll:")

    class Meta:
        
        model = PollOption
        
        fields = ['option_text']