from django.shortcuts import render, redirect
from .forms import ContactForm, UpdateProfileForm, UpdateUserForm, ImageForm, JournalForm, UpdateJournalForm, EntryForm, CommentForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
# from django.contrib import messages
# from django.http import HttpResponse
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializers import *
from .models import Profile, Journal, Entry, Image, Comment, Like
from rest_framework.decorators import api_view, renderer_classes

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
    entries = Entry.objects.filter(
        journal__user__profile__follows__in=[request.user.id]
).order_by('-created_at')
    if request.method == "POST":
        form = JournalForm(request.POST, request.FILES)
        if form.is_valid():
            journal=form.save(commit=False)
            journal.user=request.user
            form.save()
            return redirect("core:dashboard")
    form=JournalForm()
    return render(request, 'dashboard.html', {'form':form, 'entries':entries})

##Here I need to go ahead and add journal profile view
##need to have form to update profile and then also update 
#need to create journal profile HTML
##need to create journal entries 
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
        if form.is_valid() :
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
    if request.method=="POST":
        current_user = request.user.profile
        data=request.POST
        action = data.get("follow")
        if action=="follow":
            current_user.follows.add(profile)
        elif action=="unfollow":
            current_user.follows.remove(profile)
        current_user.save()
    return render(request, 'core/profile.html', {'profile': profile})

#journal profile and dashboard views
@login_required(login_url='login')
def journal_profile(request,pk):
    journal = Journal.objects.get(pk=pk)
    if request.method=='POST':
        commentForm=CommentForm(request.POST)
        if commentForm.is_valid():
            user = request.user
            comment = commentForm.save(commit=False)
            comment.user=user
            comment.journal=journal
            comment.save()
            return redirect("core:journal_profile", pk=journal.pk)
    comments = Comment.objects.filter(journal=journal).order_by('-created_at')
    commentForm=CommentForm()
    return render(request, 'core/journal.html', {'journal': journal, 'commentForm':commentForm, 'comments':comments})

@login_required(login_url='login')
def journal_dashboard(request,pk):
    journal = Journal.objects.get(pk=pk)
    entries = journal.journal_entries.all
    return render(request, 'core/journal_dashboard.html', {'journal': journal, 'entries': entries})

def update_journal(request, pk):
    journal = Journal.objects.get(pk=pk)
    if request.method == "POST":
        form = UpdateJournalForm(request.POST, request.FILES, instance=journal)
        if form.is_valid():
            form.save()
            return redirect("core:dashboard")
    form=JournalForm(instance=journal)
    return render(request, 'core/update_journal.html', {'form':form})

#entry create:
@login_required(login_url='login')
def create_entry(request,pk):
    journal= Journal.objects.get(pk=pk)
    if request.method == 'POST':
        entryForm = EntryForm(request.POST,request.FILES)
        if entryForm.is_valid():
            new_entry = entryForm.save(commit=False)
            new_entry.journal=journal
            new_entry.save()
            files = request.FILES.getlist('image')
            for f in files:
                img = Image(image=f)
                img.save()
                new_entry.image.add(img)
                new_entry.save()
            return redirect(to= 'core:journal_dashboard', pk=journal.pk)
    entryForm = EntryForm()
    return render(request, 'core/create_entry.html', {'journal': journal, 'entryForm': entryForm})

#view entry 
def entry_landing(request, pk):
    entry = Entry.objects.get(pk=pk)
    if request.method=='POST':
        commentForm=CommentForm(request.POST)
        if commentForm.is_valid():
            user = request.user
            comment = commentForm.save(commit=False)
            comment.user=user
            comment.entry=entry
            comment.save()
            return redirect("core:entry_landing", pk=entry.pk)
    comments = Comment.objects.filter(entry=entry).order_by('-created_at')
    commentForm=CommentForm()
    return render(request, 'core/entry_landing.html', {'entry': entry, 'commentForm':commentForm, 'comments':comments})

#update entry
def update_entry(request, pk):
    entry = Entry.objects.get(pk=pk)
    if request.method == 'POST':
        entryForm = EntryForm(request.POST, request.FILES, instance=entry)
        if entryForm.is_valid():

            new_entry=entryForm.save()
            files = request.FILES.getlist('image')
            for f in files:
                img = Image(image=f)
                img.save()
                new_entry.image.add(img)
                new_entry.save()
            return redirect(to='core:entry_landing', pk=entry.pk)
    entryForm = EntryForm(instance=entry)
    return render(request, 'core/update_entry.html', {'entryForm': entryForm, 'entry':entry})

#edit comment
@login_required(login_url='login')
def edit_comment(request, pk):
    comment=Comment.objects.get(pk=pk)
    if request.method == 'POST':
        commentForm=CommentForm(request.POST, instance=comment)
        if commentForm.is_valid():
            commentForm.save()
            if comment.journal:
                return redirect('core:journal_profile', pk=comment.journal.pk)
            else:
                return redirect('core:entry_landing', pk=comment.entry.pk)
    commentForm = CommentForm(instance=comment)
    return render(request, 'core/edit_comment.html', {'commentForm':commentForm, 'comment': comment})

#edit user and profile
@login_required(login_url='login')
def update_user(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='core:dashboard')
    else:
        user_form=UpdateUserForm(instance=request.user)
        profile_form=UpdateProfileForm(instance=request.user.profile)
    return render(request, 'core/update_profile.html', {'user_form':user_form, 'profile_form':profile_form,})

@login_required(login_url='login')
def image_upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_obj = form.instance
            return render(request, 'core/image_upload.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
    return render(request, 'core/image_upload.html', {'form': form})

@login_required(login_url='login')
def entry_likes(request,pk):
    entry = Entry.objects.get(pk=pk)
    for islike in entry.entry_likes.all():
        if islike.user == request.user:
            islike.like= True
            islike.save()
    else:
        new_like = Like(like=True, user=request.user, entry=entry)
        new_like.save()
    return redirect('core:entry_landing', pk=entry.pk)

def entry_unlike(request,pk):
    entry = Entry.objects.get(pk=pk)
    for islike in entry.entry_likes.all():
        if islike.user == request.user:
            islike.like= False
    return redirect('core:entry_landing', pk=entry.pk) 


# @api_view(('GET',))
# @login_required(login_url='login')
# def delete_user(request, pk):
#     # context = {}

#     try:
#         current_user = request.user
#         current_user.delete()
#         # print('User has been deleted')
#     except User.DoesNotExist:
#         messages.info(request, 'User does not exist')

from django.contrib.auth import logout as auth_logout, get_user_model
from django.views.decorators.http import require_http_methods
@login_required
# @api_view(('POST',))
# @require_http_methods(['POST'])
def remove_account(request):
    user_pk = request.user.pk
    auth_logout(request)
    User = get_user_model()
    User.objects.filter(pk=user_pk).update(is_active=False)
    return redirect(to='core:dashboard')
    # return Response({"Success": "User deactivated"}, status=status.HTTP_200_OK)

@login_required
@api_view(('POST',))
@require_http_methods(['POST'])
def delete_account(request):
    user_pk = request.user.pk
    auth_logout(request)
    User = get_user_model()
    User.objects.filter(pk=user_pk).delete()
    return Response({"Success": "User deleted"}, status=status.HTTP_200_OK)

