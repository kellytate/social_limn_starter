from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile, Image, Journal, Entry, Comment, Video, Place
from mapbox_location_field.forms import LocationField as FormLocationField
#note that this form needs to be set up in the email settings 
#change backend to 
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = '<your_email>'
# EMAIL_HOST_PASSWORD = 'your_password>'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

class ContactForm(forms.Form):
    
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
                'placeholder': 'Name',
                'style': 'width: 400px; color: #92A7A0; background-color: #1f1e1d; border-radius: 8px; padding: 8px; border: none, border-bottom: 2px solid #92A7A0',
                'class': 'form-control'}))

    subject = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
                'placeholder': 'Subject',
                'style': 'width: 400px; color: #92A7A0; background-color: #1f1e1d; border-radius: 8px; padding: 8px; border: none; border-bottom: 2px solid #92A7A0',
                'class': 'form-control'}))

    email_address = forms.EmailField(max_length=150, widget=forms.TextInput(attrs={
                'placeholder': 'Email',
                'style': 'width: 400px; color: #92A7A0; background-color: #1f1e1d; border-radius: 8px; padding: 8px; border: none; border-bottom: 2px solid #92A7A0',
                'class': 'form-control'}))

    message = forms.CharField(max_length=2000, widget=forms.Textarea(attrs={
                'placeholder': 'Share your thoughts...', 
                'class': 'form-control', 
                'style': 'height:60px; width:400px; color: #92A7A0; background-color: #1f1e1d; border: none; padding: 5px; border-radius: 8px; border-bottom: 2px solid #92A7A0'}))


class RegisterUserForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget=forms.TextInput(attrs={
                'placeholder': 'username',
                'type': 'input',
                'style': 'color: #92A7A0; background-color: #1f1e1d; border-radius: 8px; padding: 8px; border: none; border-bottom: 2px solid #92A7A0',
                'class': 'form-control'})

        self.fields['email'].widget=forms.EmailInput(attrs={
                'placeholder': 'email',
                'style': 'color: #92A7A0; background-color: #1f1e1d; border-radius: 8px; padding: 8px; border: none; border-bottom: 2px solid #92A7A0',
                'class': 'form-control'})

        self.fields['password1'].widget=forms.PasswordInput(attrs={
                'placeholder': 'password',
                'style': 'color: #92A7A0; background-color: #1f1e1d; border-radius: 8px; padding: 8px; border: none; border-bottom: 2px solid #92A7A0',
                'class': 'form-control'})

        self.fields['password2'].widget=forms.PasswordInput(attrs={
                'placeholder': 'confirm password',
                'style': 'color: #92A7A0; background-color: #1f1e1d; border-radius: 8px; padding: 8px; border: none; border-bottom: 2px solid #92A7A0',
                'class': 'form-control'})
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UpdateUserForm(forms.ModelForm):

    username = forms.CharField(max_length=100, required=True,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'styles': 'border-bottom: 2px solid #92A7A0'}))

    class Meta:
        model = User
        fields = ['username']

class UpdateProfileForm(forms.ModelForm):
    email = forms.EmailField(required=False, 
            widget=forms.TextInput(attrs={
                'placeholder': 'Email',
                'class': 'form-control',
                'styles': 'border-bottom: 2px solid #92A7A0'}))

    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'bio',
                'style': 'color: #92A7A0; background-color: #1f1e1d; border: none; padding: 5px; border-radius: 8px; border-bottom: 2px solid #92A7A0'}))
    
    location = forms.CharField(max_length=100, required=False, 
            widget=forms.TextInput(attrs={'placeholder': 'location',
                'class': 'form-control',
                'styles': 'border-bottom: 2px solid #92A7A0'}))

    profile_img = forms.ImageField(required=False,
            widget=forms.FileInput(attrs={
                'type': 'file',
                'class': 'form-control form-control-sm',
                'id': 'formFile',
                'style': 'background-color: #1f1e1d; color: #d3d9d9'}))
    
    class Meta:
        model = Profile
        fields = ['email', 'bio', 'location', 'profile_img']
    
class ImageForm(forms.ModelForm):
    """Form for the Image model"""
    
    class Meta:
        model = Image
        fields = ('image', 'title', 'description')

PRIVACY = [(0,"Private"),(1,"Followers Only"), (2,"Public")]

class JournalForm(forms.ModelForm):
    """Form for the Journal model"""
    title = forms.CharField(required=True, 
            widget=forms.TextInput(attrs={
                'placeholder': 'Title', 
                'style': 'color: #92A7A0; background-color: #1f1e1d; border-radius: 5px; padding: 5px; border: none;  border-bottom: 2px solid #92A7A0;',
                'class': 'form-control',}))

    location = forms.CharField(required=False, 
            widget=forms.TextInput(attrs={
                'placeholder': 'Location',
                'style': 'color: #92A7A0; background-color: #1f1e1d; border-radius: 5px; padding: 5px; border: none;  border-bottom: 2px solid #92A7A0;',
                'class': 'form-control'}))

    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
                'placeholder': 'Description', 
                'class': 'form-control', 
                'style': 'cols:10; color: #92A7A0; background-color: #1f1e1d; border-radius: 5px; padding: 5px; border: none;  border-bottom: 2px solid #92A7A0;',}))
    
    cover_img = forms.ImageField(required=False, widget=forms.FileInput(attrs={
                'type': 'file',
                'class': 'form-control form-control-sm',
                'id': 'formFile',
                'style': 'background-color: #1f1e1d; color: #d3d9d9'}))
    
    default_privacy = forms.IntegerField(label='Select Journal Default Privacy Level',
            widget=forms.Select(choices=PRIVACY, attrs={
                'class': 'form-control','style': 'color: #d3d9d9; border: none; background-color: #1f1e1d'}))

    class Meta:
        model = Journal
        fields=['title','location','description', 'cover_img', 'default_privacy']  

class UpdateJournalForm(forms.ModelForm):
    title = forms.CharField(required=False, 
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'styles': 'border-bottom: 2px solid #92A7A0'}))

    location = forms.CharField(required=False, 
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'styles': 'border-bottom: 2px solid #92A7A0'}))

    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
                'class': 'form-control',
                'styles': 'border-bottom: 2px solid #92A7A0',
                'rows': 5}))

    cover_img = forms.ImageField(required=False, widget=forms.FileInput(attrs={
                'type': 'file',
                'class': 'form-control form-control-sm',
                'id': 'formFile',
                'style': 'background-color: #1f1e1d; color: #d3d9d9'}))

    default_privacy = forms.IntegerField(label='Select Journal Default Privacy Level',
            widget=forms.Select(choices=PRIVACY, attrs={
                'class': 'form-control','style': 'color: #d3d9d9; border: none; background-color: #1f1e1d'}))

    class Meta:
        model = Journal
        fields=['title','location','description', 'cover_img', 'default_privacy']  

class EntryForm(forms.ModelForm):
    title = forms.CharField(required=False, 
            widget=forms.TextInput(attrs={
                'placeholder': 'Title', 
                'style': 'color: #92A7A0; background-color: #1f1e1d; border-radius: 8px; padding: 5px; border: none; border-bottom: 2px solid #92A7A0',
                'class': 'form-control'}))

    location = forms.CharField(required=False, 
            widget=forms.TextInput(attrs={
                'placeholder': 'Location', 
                'style': 'color: #92A7A0; background-color: #1f1e1d; border-radius: 8px; padding: 5px; border: none; border-bottom: 2px solid #92A7A0',
                'class': 'form-control'}))
    
    body = forms.CharField(required=True, widget=forms.Textarea(attrs={
                'placeholder': 'Tell your story...', 
                'class': 'form-control', 
                'style': 'color: #92A7A0; background-color: #1f1e1d; border: none; padding: 5px; border-radius: 8px; border-bottom: 2px solid #92A7A0'}))
    
    entry_privacy = forms.IntegerField(label='Select Entry Privacy Level', widget=forms.Select(choices=PRIVACY, attrs={
                'class': 'form-control',
                'style': 'color: #d3d9d9; border: none; border-bottom: 2px solid #92A7A0; background-color: #1f1e1d'}))

    image = forms.ImageField(required=False,widget=forms.ClearableFileInput(attrs={
                'multiple': True,
                'type': 'file',
                'class': 'form-control form-control-sm',
                'style': 'color: #d3d9d9; background-color: #1f1e1d; class: form-control form-control-sm;' }))
    
    class Meta: 
        model = Entry
        fields = ['title', 'location', 'body', 'entry_privacy']

class CommentForm(forms.ModelForm):
            
    comment = forms.CharField(widget=forms.Textarea(attrs={
                'rows': '3', 
                'placeholder': 'Share your thoughts', 
                'class': 'form-control', 
                'style': 'width: 400px; color: #92A7A0; background-color: #1f1e1d; border-radius: 8px; padding: 8px; border: none; border-bottom: 2px solid #92A7A0',}))

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

class VideoForm(forms.ModelForm):
    title = forms.CharField(required=False, 
            widget=forms.TextInput(attrs={
                'placeholder': 'Video Title', 
                'style': 'color: #92A7A0; background-color: #1f1e1d; border-radius: 8px; padding: 5px; border: none; border-bottom: 2px solid #92A7A0',
                'class': 'form-control'}))
    source_url = forms.CharField(required=False, 
            widget=forms.TextInput(attrs={
                'placeholder': 'Video URL', 
                'style': 'color: #92A7A0; background-color: #1f1e1d; border-radius: 8px; padding: 5px; border: none; border-bottom: 2px solid #92A7A0',
                'class': 'form-control'}))
    
    class Meta:
        model = Video
        fields = ['title', 'source_url']

class LocationForm(forms.Form):
    search_string = forms.CharField(label='',max_length=100)

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = "__all__" 

REPORT_TYPES = (
    ('onThisDay', 'Memories for this Day',),
    ('spotify', 'Playlist for this Day',),
    ('spotify_range', 'Create a playlist for Date Range',),
    ('onThisDayRange', 'View Memories for Date Range',),
)
class ReportsForm(forms.Form):
    search_type = forms.ChoiceField(label='Report Type',required=True,
                                    choices=REPORT_TYPES)

class DateInput(forms.DateInput):
    input_type = 'date'

class JournalMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.title

    
class OnThisDayForm(forms.Form):
    def label_from_instance(self, obj):
        return f'{obj.title}'

    memory_date = forms.DateField(widget=DateInput)
    journals = forms.ModelMultipleChoiceField(
        widget = forms.CheckboxSelectMultiple(),
        queryset = None)

    def __init__(self,user, *args, **kwargs): # Correctly obtains slug from url
        super(OnThisDayForm,self).__init__(*args, **kwargs) 
        self.fields['journals'].label_from_instance = self.label_from_instance
        self.fields['journals'].queryset = Journal.objects.filter(user=user).exclude(is_archived=True)

class OnThisDayRangeForm(forms.Form):
    def label_from_instance(self, obj):
        return f'{obj.title}'

    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)
    journals = forms.ModelMultipleChoiceField(
        widget = forms.CheckboxSelectMultiple(),
        queryset = None)

    def __init__(self,user, *args, **kwargs): # Correctly obtains slug from url
        super(OnThisDayRangeForm,self).__init__(*args, **kwargs) 
        self.fields['journals'].label_from_instance = self.label_from_instance
        self.fields['journals'].queryset = Journal.objects.filter(user=user).exclude(is_archived=True)
            

    