from django import forms
from main.models import Article, Category, UserProfile, Comment, Forum, Thread, Post, Poll, PollOption, UNIVERSITY_CHOICES
from django.contrib.auth.models import User
from django.utils import timezone

class CategoryForm(forms.ModelForm):

    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH, help_text="Please enter the category name:")

    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 80}), max_length=Category.DESCRIPTION_MAX_LENGTH, help_text="Please enter the category description:")

    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    points = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:

        model = Category

        fields = ('name', 'description',)

class ArticleForm(forms.ModelForm):

    title = forms.CharField(max_length=Article.TITLE_MAX_LENGTH, help_text="Please enter the title of the article:")

    summary = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 80}), max_length=Article.SUMMARY_MAX_LENGTH, help_text="Please enter the summary of the article:")

    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 10, 'cols': 80}), max_length=Article.CONTENT_MAX_LENGTH, help_text="Please enter the content of the article:")

    article_picture = forms.ImageField(required=True, help_text="Please upload an image for the article:")

    related_university = forms.ChoiceField(choices=[('', 'Select a university')] + UNIVERSITY_CHOICES, required=False, help_text="Enter if this article is related to a specific university:")

    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    points = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    created_on = forms.DateTimeField(widget=forms.HiddenInput())

    last_visit = forms.DateTimeField(widget=forms.HiddenInput(), required=False)

    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:

        model = Article

        exclude = ('category', 'author',)
    
class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:

        model = User
              
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):

    first_name = forms.CharField(max_length=UserProfile.NAME_MAX_LENGTH, required=True)

    last_name = forms.CharField(max_length=UserProfile.NAME_MAX_LENGTH, required=True)

    start_year = forms.IntegerField(initial=timezone.now().year)

    class Meta:

        model = UserProfile
        
        fields = ('first_name', 'last_name', 'university', 'school', 'department', 'degree', 'start_year', 'profile_picture',)

class CommentForm(forms.ModelForm):

    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 80}), max_length=Comment.CONTENT_MAX_LENGTH, help_text="Please enter your comment:")

    class Meta:

        model = Comment

        exclude = ('article', 'user', 'written_on',)

class ForumForm(forms.ModelForm):

    name = forms.CharField(max_length=Forum.NAME_MAX_LENGTH, help_text="Please enter the forum name:")

    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 80}), max_length=Forum.DESCRIPTION_MAX_LENGTH, help_text="Please enter the forum description:")

    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:

        model = Forum

        fields = ('name', 'description',)

class ThreadForm(forms.ModelForm):

    title = forms.CharField(max_length=Thread.TITLE_MAX_LENGTH, help_text="Enter the title of your thread:")

    topic = forms.CharField(max_length=Thread.TOPIC_MAX_LENGTH, help_text="Enter the topic of your thread:")
    
    related_university = forms.ChoiceField(choices=[('', 'Select a university')] + UNIVERSITY_CHOICES, required=False, help_text="Enter if this thread is related to a specific university:")

    class Meta:

        model = Thread
        
        fields = ['title', 'topic', 'related_university']

class PostForm(forms.ModelForm):

    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 80}), max_length=Post.CONTENT_MAX_LENGTH, help_text="Enter your post:")

    class Meta:
        
        model = Post
        
        fields = ['content']

class PollForm(forms.ModelForm):

    question = forms.CharField(max_length=Poll.QUESTION_MAX_LENGTH, help_text="Enter the poll question:")

    class Meta:
    
        model = Poll
    
        fields = ['question']

class PollOptionForm(forms.ModelForm):

    option_text = forms.CharField(max_length=PollOption.OPTION_MAX_LENGTH, help_text="Enter an option for the poll:")

    class Meta:
        
        model = PollOption
        
        fields = ['option_text']