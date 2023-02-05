from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.contrib.auth.models import User, auth
# from django.contrib import messages
# from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from .models import Profile

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]



# def index(request):
#     return render(request, 'index.html')


# @login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form':form})

# @login_required(login_url='login_url')
# def logout(request):
#     auth.logout(request)
#     return redirect('login_url')

def home(request):
    return render(request, 'sitefront/index.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Limn Message"
            body = {
                "name": form.cleaned_data['name'],
                "message_subject": form.cleaned_data['subject'],
                "email_address": form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())
            try: 
                send_mail(subject, message, 'maple.megan333@gmail.com', ['maple.megan333@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header')
            return redirect("core:home")
    form = ContactForm()
    return render(request, 'sitefront/contact.html', {'form':form})

# Displays all available user (profiles), excluding the logged-in user
@login_required(login_url='login')
def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, 'core/profile_list.html', {'profiles': profiles})

# Displays specific profile information by primary key value
@login_required(login_url='login')
def profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    return render(request, 'core/profile.html', {'profile': profile})