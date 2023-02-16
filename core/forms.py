from django import forms
from django.contrib.auth.models import User
from .models import Profile, Image, Journal, Entry, Comment

#note that this form needs to be set up in the email settings 
#change backend to 
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = '<your_email>'
# EMAIL_HOST_PASSWORD = 'your_password>'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
class ContactForm(forms.Form):
    name = forms.CharField(max_length = 50)
    subject = forms.CharField(max_length = 50)
    email_address = forms.EmailField(max_length = 150)
    message = forms.CharField(widget = forms.Textarea, max_length = 2000)

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username']

class UpdateProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    location = forms.CharField(max_length=100,
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_img = forms.ImageField(required=False)
    
    class Meta:
        model = Profile
        fields = ['email', 'bio', 'location', 'profile_img']
    
    
class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Image
        fields = ('image', 'title', 'description')

PRIVACY = [(0,"Private"),(1,"Followers Only"), (2,"Public")]

class JournalForm(forms.ModelForm):
    title = forms.CharField(required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    cover_img = forms.ImageField(required=False)
    default_privacy = forms.IntegerField(label='Select Journal Default Privacy Level', widget=forms.Select(choices=PRIVACY))

    class Meta:
        model = Journal
        fields=['title','location','description', 'cover_img', 'default_privacy']  


class UpdateJournalForm(forms.ModelForm):
    title = forms.CharField(required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    cover_img = forms.ImageField(required=False)
    default_privacy = forms.IntegerField(label='Select Journal Default Privacy Level', widget=forms.Select(choices=PRIVACY))

    class Meta:
        model = Journal
        fields=['title','location','description', 'cover_img', 'default_privacy']  

class EntryForm(forms.ModelForm):
    title = forms.CharField(required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    entry_privacy = forms.IntegerField(label='Select Entry Privacy Level', widget=forms.Select(choices=PRIVACY))
    image = forms.ImageField(required=False,widget=forms.ClearableFileInput(attrs={
    'multiple': True}))
    class Meta: 
        model = Entry
        fields = ['title', 'location', 'body', 'entry_privacy']

class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': '3', 'placeholder': 'Share your thoughts'}))

    class Meta:
        model = Comment
        fields = ['comment']

SEARCH_TYPES = (
    ('album', 'Album',),
    ('artist', 'Artist',),
    ('track', 'Track',),
)
class SpotifySearchForm(forms.Form):
    search_type = forms.ChoiceField(label='Filter',required=True,
                                    choices=SEARCH_TYPES)
    search_string = forms.CharField(label='',max_length=100)