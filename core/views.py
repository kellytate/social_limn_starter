import requests
import json
import os
from .utils import Calendar
import spotipy
import datetime
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from django.shortcuts import render, redirect
from .forms import RegisterUserForm, ContactForm, UpdateProfileForm, UpdateUserForm, ImageForm, JournalForm, UpdateJournalForm, EntryForm, CommentForm, SpotifySearchForm, VideoForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.conf import settings
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializers import *
from .models import Profile, Journal, Entry, Image, Comment, Like, Song, Video
from rest_framework.decorators import api_view, renderer_classes
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from cloudinary.forms import cl_init_js_callbacks

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]



# def index(request):
#     return render(request, 'index.html')


@login_required(login_url='login')

def dashboard(request):
    entries = Entry.objects.filter(
        journal__user__profile__follows__in=[request.user.id]
).exclude(is_archived=True).order_by('-created_at')
    if request.method == "POST":
        form = JournalForm(request.POST, request.FILES)
        if form.is_valid():
            journal=form.save(commit=False)
            journal.user=request.user
            form.save()
            return redirect("core:dashboard")
    form=JournalForm()
    journals = Journal.objects.filter(user=request.user).exclude(is_archived=True)
    return render(request, 'dashboard.html', {'form':form, 'entries':entries, 'journals':journals})

##Here I need to go ahead and add journal profile view
##need to have form to update profile and then also update 
#need to create journal profile HTML
##need to create journal entries 
def signup(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterUserForm()
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

    # entries = Entry.objects.filter(
    #     journal__user__profile__follows__in=[request.user.id]).exclude(is_archived=True).order_by('-created_at')

    journals_followers = Journal.objects.filter(user__profile__follows__in=[request.user.id]).filter(user=profile.user).exclude(is_archived=True).exclude(default_privacy=0)
    journals_public = Journal.objects.filter(user__profile__follows__in=[request.user.id]).filter(user=profile.user).exclude(is_archived=True).exclude(default_privacy=0).exclude(default_privacy=1).order_by('-created_at')

    journals = journals_public
    
    if journals_followers:
        journals = journals_followers

    if request.method=="POST":
        current_user = request.user.profile
        data=request.POST
        action = data.get("follow")
        if action=="follow":
            current_user.follows.add(profile)
        elif action=="unfollow":
            current_user.follows.remove(profile)
        current_user.save()
    return render(request, 'core/profile.html', {'profile': profile, 'journals': journals})

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
    likeCounts = {}
    for comment in comments:
        count = Like.objects.filter(comment=comment).exclude(like = False).count()
        likeCounts[comment.id] = count
    likes = Like.objects.filter(journal=journal).exclude(like = False)
    entries = Entry.objects.filter(journal=journal).exclude(is_archived=True).exclude(entry_privacy=0)
    return render(request, 'core/journal.html', {'journal': journal, 'commentForm':commentForm, 'comments':comments, 'likes':likes, 'likeCounts':likeCounts, 'entries': entries})

@login_required(login_url='login')
def journal_dashboard(request,pk):
    journal = Journal.objects.get(pk=pk)
    
    if request.user != journal.user:
        return(redirect("core:journal_profile", pk=journal.pk))

    entries = Entry.objects.filter(journal=journal).exclude(is_archived=True)
    cal= []
    for entry in entries:
        cal.append({'id': entry.pk,
        'title': entry.title,
        'start':entry.created_at.strftime('%Y-%m-%d'),
        'url': entry.get_html_url})
        
    likes = Like.objects.filter(journal=journal).exclude(like = False)
    return render(request, 'core/journal_dashboard.html', {'journal': journal, 'entries': entries, 'likes':likes, 'cal':cal})

def update_journal(request, pk):
    journal = Journal.objects.get(pk=pk)

    if request.user != journal.user:
        return(redirect("core:journal_profile", pk=journal.pk))

    if request.method == "POST":
        form = UpdateJournalForm(request.POST, request.FILES, instance=journal)
        if form.is_valid():
            form.save()
            return redirect("core:dashboard")
    form=JournalForm(instance=journal)
    return render(request, 'core/update_journal.html', {'form':form})

def delete_journal(request, pk):
    journal = Journal.objects.get(pk=pk)
    if request.method=="POST":
        journal.is_archived = True
        journal.save()
        for entry in journal.journal_entries.all():
            entry.is_archived = True
            entry.save()
    
        return redirect('core:dashboard')

#entry create:
@login_required(login_url='login')
def create_entry(request,pk):
    journal= Journal.objects.get(pk=pk)
    if request.method == 'POST':
        entryForm = EntryForm(request.POST,request.FILES)
        videoForm = VideoForm(request.POST)
        if entryForm.is_valid():
            new_entry = entryForm.save(commit=False)
            new_entry.journal=journal
            new_entry.save()
            new_video = videoForm.save(commit=False)
            new_video.entry=new_entry
            new_video.save()
            new_entry.save()
            files = request.FILES.getlist('image')
            for f in files:
                img = Image(image=f)
                img.save()
                new_entry.image.add(img)
                new_entry.save()
            return redirect(to= 'core:journal_dashboard', pk=journal.pk)
    entryForm = EntryForm()
    videoForm = VideoForm()
    return render(request, 'core/create_entry.html', {'journal': journal, 'entryForm': entryForm, "videoForm":videoForm})

#view entry 
def entry_landing(request, pk):
    entry = Entry.objects.get(pk=pk)

    # if entry.privacy != 2 or entry.privacy != 0 and user not in entry.journal.user.followed_by:
    #     return(redirect("core:profile", pk=entry.journal.user.pk))

    if request.method=='POST':
        commentForm=CommentForm(request.POST)
        if commentForm.is_valid():
            user = request.user
            comment = commentForm.save(commit=False)
            comment.user=user
            comment.entry=entry
            comment.save()
            return redirect("core:entry_landing", pk=entry.pk)
    likes= Like.objects.filter(entry=entry).exclude(like = False)
    comments = Comment.objects.filter(entry=entry).order_by('-created_at')
    images = Image.objects.filter(entry=entry).exclude(is_archived=True)
    likeCounts = {}
    song = Song.objects.filter(entry=entry).exclude(is_archived=True)
    videos = Video.objects.filter(entry=entry).exclude(is_archived=True)
    frame_key = settings.IFRAME_KEY
    for comment in comments:
        count = Like.objects.filter(comment=comment).exclude(like = False).count()
        likeCounts[comment.id] = count
    commentForm=CommentForm()
    return render(request, 'core/entry_landing.html', {'entry': entry, 'commentForm':commentForm, 'comments':comments, 'likes':likes, 'likeCounts':likeCounts, 'images':images, 'song':song, "frame_key":frame_key, "videos": videos})

#update entry
def update_entry(request, pk):
    entry = Entry.objects.get(pk=pk)

    if request.user != entry.journal.user:
        return(redirect("core:entry_landing", pk=entry.pk))

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
    song=Song.objects.filter(entry=entry).exclude(is_archived=True)
    frame_key = settings.IFRAME_KEY
    images = Image.objects.filter(entry=entry).exclude(is_archived=True)
    return render(request, 'core/update_entry.html', {'entryForm': entryForm, 'entry':entry, 'images':images, 'song':song, "frame_key":frame_key})
#delete image:
def delete_image(request, pk,ok):
    image = Image.objects.get(pk=pk)
    if request.method=="POST":
        image.is_archived = True
        image.save()
    return redirect('core:update_entry', pk=ok)


#delete entry
def delete_entry(request, pk):
    entry = Entry.objects.get(pk=pk)
    if request.method=="POST":
        entry.is_archived = True
        entry.save()
    
        return redirect('core:journal_dashboard', pk=entry.journal.pk)

#edit comment
@login_required(login_url='login')
def edit_comment(request, pk):
    comment=Comment.objects.get(pk=pk)

    if request.user != comment.user:
        return

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

#delete Comment:
def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    if request.method=="POST":
        comment.is_archived = True
        comment.save()
        if comment.journal:
                return redirect('core:journal_profile', pk=comment.journal.pk)
        else:
                return redirect('core:entry_landing', pk=comment.entry.pk)

def reply_comment(request, pk):
    parent_comment = Comment.objects.get(pk=pk)
    if request.method == 'POST':
        commentForm=CommentForm(request.POST)
        if commentForm.is_valid():
            comment = commentForm.save(commit=False)
            comment.user = request.user
            comment.parent = parent_comment
            comment.save()
            if parent_comment.journal:
                comment.journal=parent_comment.journal
                comment.save()
                return redirect('core:journal_profile', pk=parent_comment.journal.pk)
            else:
                comment.entry=parent_comment.entry
                comment.save()
                return redirect('core:entry_landing', pk=parent_comment.entry.pk)

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
    new_like=None
    for islike in entry.entry_likes.all():
        if islike.user == request.user:
            islike.like= True
            islike.save()
            new_like=islike
    if not new_like:
        new_like = Like(like=True, user=request.user, entry=entry)
        new_like.save()
    return redirect('core:entry_landing', pk=entry.pk)

def entry_unlike(request,pk):
    entry = Entry.objects.get(pk=pk)
    for islike in entry.entry_likes.all():
        if islike.user == request.user:
            islike.like= False
            islike.save()
    return redirect('core:entry_profile', pk=entry.pk)

@login_required(login_url='login')
def journal_likes(request,pk):
    journal = Journal.objects.get(pk=pk)
    new_like=None
    for islike in journal.journal_likes.all():
        if islike.user == request.user:
            islike.like= True
            islike.save()
            new_like=islike
    if not new_like:
        new_like = Like(like=True, user=request.user, journal=journal)
        new_like.save()
    return redirect('core:journal_profile', pk=journal.pk)

def journal_unlike(request,pk):
    journal = Journal.objects.get(pk=pk)
    for islike in journal.journal_likes.all():
        if islike.user == request.user:
            islike.like= False
            islike.save()
    return redirect('core:journal_profile', pk=journal.pk)  

@login_required(login_url='login')
def comment_likes(request,pk):
    comment = Comment.objects.get(pk=pk)
    new_like=None
    for islike in comment.comment_likes.all():
        if islike.user == request.user:
            islike.like= True
            islike.save()
            new_like=islike
    if not new_like:
        new_like = Like(like=True, user=request.user, comment=comment)
        new_like.save()
    if comment.entry:
        return redirect('core:entry_landing', pk=comment.entry.pk)
    return redirect('core:journal_profile', pk=comment.journal.pk)

def comment_unlike(request,pk):
    comment = Comment.objects.get(pk=pk)
    for islike in comment.comment_likes.all():
        if islike.user == request.user:
            islike.like= False
            islike.save()
    if comment.entry:
        return redirect('core:entry_landing', pk=comment.entry.pk) 
    return redirect('core:journal_profile', pk=comment.journal.pk)
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


def search_page(request):
    return render(request, 'core/search.html')

def searchUsers(request):
    if request.method=='GET':
        query=request.GET.get('q')

        submitButton = request.GET.get('submit')
        
        if query is not None:
            checking = Q(username__icontains=query)
            results=User.objects.filter(checking)
            return render(request, 'core/search.html', {'results':results, 'submitButton':submitButton})

    return render(request, 'core/search.html')

def searchUserEntries(request):
    if request.method=='GET':
        query=request.GET.get('a')

        submitButton = request.GET.get('submit')
        
        if query is not None:
            checking = Q(title__icontains=query) | Q(body__icontains=query)
            results=Entry.objects.filter(journal__user=request.user).filter(checking)
            return render(request, 'core/search.html', {'results':results, 'submitButton':submitButton})

    return render(request, 'core/search.html')

def searchUserJournals(request):
    if request.method=='GET':
        query=request.GET.get('j')

        submitButton = request.GET.get('submit')
        
        if query is not None:
            checking = Q(title__icontains=query) | Q(description__icontains=query)
            results=Journal.objects.filter(user=request.user).filter(checking)
            return render(request, 'core/search.html', {'results':results, 'submitButton':submitButton})
    return render(request, 'core/search.html')

def searchAllEntries(request):
    if request.method=='GET':
        query=request.GET.get('aa')

        submitButton = request.GET.get('submit')
        
        if query is not None:
            checking = Q(title__icontains=query) | Q(body__icontains=query)
            results=Entry.objects.filter(checking)
            return render(request, 'core/search.html', {'results':results, 'submitButton':submitButton})

    return render(request, 'core/search.html')


def searchAllJournals(request):
    if request.method=='GET':
        query=request.GET.get('jj')

        submitButton = request.GET.get('submit')
        
        if query is not None:
            checking = Q(title__icontains=query) | Q(description__icontains=query)
            results=Journal.objects.filter(checking)
            return render(request, 'core/search.html', {'results':results, 'submitButton':submitButton})
    return render(request, 'core/search.html')

RESULT_KEY_MAP = (
    ('artist', 'artists',),
    ('album', 'albums',),
    ('playlist', 'playlists',),
    ('track', 'tracks',),
)

def search_spotify(request, pk):
    results = None
    result_count = None
    # We will lose the POST data every time we use pagination
    # One way of keeping this data is to add it to a session
    # Make sure we only add this data when we're actually using pagination
    # ('page' in request.GET)
    spotipyid = settings.SPOTIPY_CLIENT_ID
    spotipySecret = settings.SPOTIPY_CLIENT_SECRET
    my_creds = SpotifyClientCredentials(client_id=spotipyid, client_secret=spotipySecret)
    if not request.method == 'POST' and 'page' in request.GET:
        if 'search-post' in request.session:
            request.POST = request.session['search-post']
            request.method = 'POST'

    if request.method == 'POST':
        form = SpotifySearchForm(request.POST)
        request.session['search-post'] = request.POST

        if form.is_valid():
            search_type = form.cleaned_data['search_type']
            search_string = form.cleaned_data['search_string']

            spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
            response_content = spotify.search(q=search_string, type=search_type, limit=20)
            # Deal with any strange responses from Spotify
            #
            print(response_content)
            result_key = dict(RESULT_KEY_MAP)[search_type]
            search_results=[]
            if result_key == 'artist':
                for artist in response_content[result_key]['items']:
                    result = spotify.artist_top_tracks(artist['uri'])
                    search_results.extend(result['tracks'][:10])
            
            elif result_key == 'album':
                for album in response_content[result_key]['items']:
                    results = spotify.album_tracks(album['uri'])
                    search_results.extend(results['items'])
            else:
                search_results = response_content[result_key]['items']
        
            result_count = response_content[result_key]['total']
            paginator = Paginator(
                search_results, settings.SEARCH_RESULTS_PER_PAGE
            )

            page = request.GET.get('page')
            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                results = paginator.page(1)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)
    else:
        form = SpotifySearchForm()

    
    #player =requests.get('iframe.ly/api/iframely?url=https://open.spotify.com/album/4E4NBueuClmsr8tVkZgV0K&api_key=7c27dc4b622df14eeffcf7')

    context = {
        'search_results': results,
        'form': form,
        'result_count': result_count,
        'search_limit': settings.SPOTIFY_LIMIT,
        'entry': Entry.objects.get(pk=pk)
    }
    return render(request, 'core/spotify_search.html', context)

@login_required(login_url='login')
def add_song(request,pk):
    entry = Entry.objects.get(pk=pk)
    songs = Song.objects.filter(entry=entry).exclude(is_archived=True)
    if songs:
        for song in songs:
            song.is_archived=True
            song.save()
    if request.method=="POST":
        new_song = Song()
        new_song.entry=entry
        new_song.title = request.POST.get('title')
        new_song.source_url = request.POST.get('source')
        new_song.save()
    return redirect('core:entry_landing', pk=entry.pk)

def upload(request):
    context = dict(backend_form = ImageForm())

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        context['posted'] = form.instance
        if form.is_valid():
            form.save()

    return render(request, 'core/upload.html', context)

def notify_endpoint():
    return