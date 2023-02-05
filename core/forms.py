from django import forms
from django.contrib.auth.models import User
from .models import Profile

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
    
    class Meta:
        model = Profile
        fields = ['email', 'bio', 'location']
    
    