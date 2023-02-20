import requests
import json
import string
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from django.shortcuts import render, redirect
from .forms import RegisterUserForm, ContactForm, UpdateProfileForm, UpdateUserForm, ImageForm, JournalForm, UpdateJournalForm, EntryForm, CommentForm, SpotifySearchForm, VideoForm, PlaceForm, LocationForm, ReportsForm, OnThisDayForm
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
from .models import Profile, Journal, Entry, Image, Comment, Like, Song, Video, Place
from rest_framework.decorators import api_view, renderer_classes
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from cloudinary.forms import cl_init_js_callbacks

## helper functions here. 
def spotify_auth():
    scope = "user-read-recently-played playlist-modify-public user-top-read user-read-playback-position user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-private playlist-modify-private playlist-read-private"
    auth_manager = spotipy.oauth2.SpotifyOAuth(settings.SPOTIPY_CLIENT_ID, settings.SPOTIPY_CLIENT_SECRET, settings.SPOTIPY_REDIRECT_URI,
                                scope=scope)
    return auth_manager

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


## all Front end views here. 

def home(request):

    return render(request, 'sitefront/index.html')

def signup(request):

    if request.method == "POST":

        form = RegisterUserForm(request.POST)
    
        if form.is_valid():

            form.save()
            return redirect('login')
    else:

        form = RegisterUserForm()

    return render(request, 'registration/signup.html', {'form':form})


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
            
            return redirect("home")
        
    form = ContactForm()
    return render(request, 'sitefront/contact.html', {'form':form})


@login_required(login_url='login')
def dashboard(request):

    entries = Entry.objects.filter(
        journal__user__profile__follows__in=[request.user.id]
).exclude(is_archived=True).order_by('-created_at')
    
    if request.GET.get("code"):
        auth_manager = spotify_auth()
        code = request.GET.get("code", "")
        token = auth_manager.get_access_token(code=code)

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

# Displays all available user (profiles), excluding the logged-in user
@login_required(login_url='login')
def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, 'core/profile_list.html', {'profiles': profiles})

# Displays specific profile information by primary key value
@login_required(login_url='login')
def profile(request, pk):
    profile = Profile.objects.get(pk=pk)

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
            new_entry.title = entryForm.cleaned_data["title"]
            new_entry.save()
            if videoForm.is_valid():
                url = videoForm.cleaned_data["source_url"]
                if url:
                    title = request.POST.get('videoTitle')
                    newVideo = Video(title=title, entry=new_entry, source_url=url)
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
    items = []
    if images:
        for image in images:
            items.append(json.dumps({
                "src": image.image.url,
            }))
    likeCounts = {}
    song = Song.objects.filter(entry=entry).exclude(is_archived=True)
    videos = Video.objects.filter(entry=entry).exclude(is_archived=True)
    if videos:
        for video in videos:
            items.append(json.dumps({
                "src": video.source_url
            }))
    frame_key = settings.IFRAME_KEY
    place = Place.objects.filter(entry=entry).exclude(is_archived=True).first()
    placeMap=None
    if place:
        placeMap = f'https://maps.locationiq.com/v3/staticmap?key={settings.LOCATIONIQ_API_KEY}&markers=size:small|color:red|{place.latitude},{place.longitude}'

    for comment in comments:
        count = Like.objects.filter(comment=comment).exclude(like = False).count()
        likeCounts[comment.id] = count
    commentForm=CommentForm()
    return render(request, 'core/entry_landing.html', 
        {'entry': entry, 'commentForm':commentForm, 'comments':comments, 'likes':likes, 
        'likeCounts':likeCounts, 'images':images, 'song':song, "frame_key":frame_key, "videos": videos, 
        "place":place, 'placeMap':placeMap, "items":items})

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
    videos = Video.objects.filter(entry=entry).exclude(is_archived=True)
    videoForm=VideoForm()
    place = Place.objects.filter(entry=entry).exclude(is_archived=True).first()
    placeMap=None
    if place:
        placeMap = f'https://maps.locationiq.com/v3/staticmap?key={settings.LOCATIONIQ_API_KEY}&markers=size:small|color:red|{place.latitude},{place.longitude}'
    return render(request, 'core/update_entry.html', {'entryForm': entryForm, 'entry':entry, 'images':images, 'song':song, "frame_key":frame_key, "videos":videos, "videoForm":videoForm, "place":place, "placeMap":placeMap})

## add a delete video button.
def another_video(request, pk):
    if request.method=="POST":
        videoForm = VideoForm(request.POST)
        if videoForm.is_valid():
            video = videoForm.save(commit=False)
            entry = Entry.objects.get(pk=pk)
            video.entry=entry
            video.save()
            entry.save()
    return redirect('core:update_entry', pk=pk)
#delete image:
def delete_image(request, pk,ok):
    image = Image.objects.get(pk=pk)
    if request.method=="POST":
        image.is_archived = True
        image.save()
    return redirect('core:update_entry', pk=ok)

#video
def delete_video(request, pk,ok):
    video = Video.objects.get(pk=pk)
    if request.method=="POST":
        video.is_archived = True
        video.save()
    return redirect('core:update_entry', pk=ok)

#delete place:
def delete_song(request, pk,ok):
    song = Song.objects.get(pk=pk)
    if request.method=="POST":
        song.is_archived = True
        song.save()
    return redirect('core:update_entry', pk=ok)

#delete image:
def delete_place(request, pk,ok):
    place = Place.objects.get(pk=pk)
    if request.method=="POST":
        place.is_archived = True
        place.save()
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

def location_search(request, pk):
    
    results = None
    result_count = None
    # We will lose the POST data every time we use pagination
    # One way of keeping this data is to add it to a session
    # Make sure we only add this data when we're actually using pagination
    ## ('page' in request.GET)
    if not request.method == 'POST' and 'page' in request.GET:
        if 'search-post' in request.session:
            request.POST = request.session['search-post']
            request.method = 'POST'

    if request.method == 'POST':
        form = LocationForm(request.POST)

        if form.is_valid():
            search_string = form.cleaned_data['search_string']

            path = "https://us1.locationiq.com/v1/search.php"
            query_params = {
                "key": settings.LOCATIONIQ_API_KEY,
                "q": search_string,
                "format": "json"
            }

            response = requests.get(path, params=query_params)
            response_content = response.json()
            results=response_content
            # Deal with any strange responses from Spotify
            #
            print(response_content)
        
            result_count = len(response_content)
            paginator = Paginator(
                results, settings.SEARCH_RESULTS_PER_PAGE
            )

            page = request.GET.get('page')
            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                results = paginator.page(1)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)
    else:
        form = LocationForm()

    
    #player =requests.get('iframe.ly/api/iframely?url=https://open.spotify.com/album/4E4NBueuClmsr8tVkZgV0K&api_key=7c27dc4b622df14eeffcf7')

    context = {
        'search_results': results,
        'form': form,
        'result_count': result_count,
        'entry': Entry.objects.get(pk=pk)
    }
    return render(request, 'core/location_search.html', context)

def add_place(request,pk):
    entry = Entry.objects.get(pk=pk)
    places = Place.objects.filter(entry=entry).exclude(is_archived=True)
    if places:
        for place in places:
            place.is_archived=True
            place.save()
    if request.method=="POST":
        new_place=Place()
        new_place.entry=entry
        new_place.name = request.POST.get('name')
        new_place.longitude = request.POST.get('lon')
        new_place.latitude = request.POST.get('lat')
        new_place.save()
    return redirect('core:entry_landing', pk=entry.pk)

def notify_endpoint():
    return

# def image(request, pk):
#     image = Image.objects.get(pk=pk)

def reports(request, pk):
    profile = Profile.objects.get(pk=pk)
    reportsForm = ReportsForm()
    if request.method == "POST":
        reportsForm = ReportsForm(request.POST)
        if reportsForm.is_valid():
            if reportsForm.cleaned_data['search_type'] == 'onThisDay':
                return redirect('core:day_reports', pk=profile.pk)
            elif reportsForm.cleaned_data['search_type'] == 'spotify':
                return redirect('core:spotify_report', pk=profile.pk)

    return render(request, 'core/reports.html', {"reportsForm": reportsForm})

def onThisDayReport(request,pk):

    profile = Profile.objects.get(pk=pk)
    dateForm = OnThisDayForm()
    entries = None
    albums = []
    date=None
    trends = ""
    map = ''
    
    if request.method == "POST":
        dateForm = OnThisDayForm(request.POST)
        if dateForm.is_valid():
            date = dateForm.cleaned_data['memory_date']
            entries = Entry.objects.filter(journal__user=request.user).exclude(is_archived=True).filter(created_at__month=date.month).filter(created_at__day=date.day).order_by('-created_at')
            count = 1

            for entry in entries:
                images = Image.objects.filter(entry=entry)
                videos = Video.objects.filter(entry=entry)
                song = Song.objects.filter(entry=entry).exclude(is_archived=True).first()
                place = Place.objects.filter(entry=entry).exclude(is_archived=True).first()
                trends = trends + " " + entry.body

                if images:
                    for indx,image in enumerate(images):
                        if indx == 0:
                            albums.append(json.dumps({"src":image.image.url,
                                            "title": entry.title,
                                            "ID": count,	
                                            "kind":'album'}))
                        albums.append(json.dumps({
                            "src": image.image.url,
                        }))

                    if videos:
                        for video in videos:
                            albums.append(json.dumps({
                                "src": video.source_url, 
                                "albumID": count
                            }))
                    
                elif videos:
                    for indx, video in enumerate(videos):
                        if indx==0:
                            albums.append(json.dumps({"src":video.source_url,
                                                    "title": entry.title,
                                                    "ID": count,	
                                                    "kind":'album'}))
                        albums.append(json.dumps({
                            "src": video.source_url, 
                            "albumID": count
                        }))      
                
                if place:
                    if not map:
                        map = f'https://maps.locationiq.com/v3/staticmap?key={settings.LOCATIONIQ_API_KEY}&markers=size:small|color:red'
                    map = map + f'|{place.latitude},{place.longitude}'
                
                count +=1

    if trends:
        new = trends.translate(str.maketrans('', '', string.punctuation)).strip()
        new = new.replace('\n', ' ').replace('\r', ' ')
        trends = new 


    context={
    "dateForm": dateForm, 
    "entries":entries,
    "albums" : albums,
    "date":  date.strftime("%B %d") if date else date,
    "frame_key":settings.IFRAME_KEY,
    "trends": trends,
    "map": map
    }

    return render(request, 'core/on_this_day.html', context)


def spotify_login(request):
    scope = "user-read-recently-played user-top-read playlist-modify-public user-read-playback-position user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-private playlist-modify-private playlist-read-private"
    auth_manager = spotipy.oauth2.SpotifyOAuth(settings.SPOTIPY_CLIENT_ID, settings.SPOTIPY_CLIENT_SECRET, settings.SPOTIPY_REDIRECT_URI,
                                scope=scope)
    redirect_url = auth_manager.get_authorize_url() # Note: You should parse this somehow. It may not be in a pretty format.
    return redirect(redirect_url)

def spotify_report(request, pk):
    profile = Profile.objects.get(pk=pk)
    dateForm = OnThisDayForm()
    entries = None
    date=None
    songs = []
    playlist_url = None
    token_info = None

    scope = "user-read-recently-played playlist-modify-public user-top-read user-read-playback-position user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-private playlist-modify-private playlist-modify-public playlist-read-private"
    auth_manager = spotipy.oauth2.SpotifyOAuth(settings.SPOTIPY_CLIENT_ID, settings.SPOTIPY_CLIENT_SECRET, settings.SPOTIPY_REDIRECT_URI,
                                scope=scope)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    token_info = auth_manager.get_cached_token()
    print(token_info)

    if request.method == "POST":

        dateForm = OnThisDayForm(request.POST)
        if dateForm.is_valid():
            date = dateForm.cleaned_data['memory_date']
            entries = Entry.objects.filter(journal__user=request.user).exclude(is_archived=True).filter(created_at__month=date.month).filter(created_at__day=date.day).order_by('-created_at')

            for entry in entries:
                song = Song.objects.filter(entry=entry).exclude(is_archived=True).first()
                
                if song:
                    songs.append(song.source_url)

    if songs:
            #print(sp.me())
        user_id = sp.me()['id']
        playlist = sp.user_playlist_create(user_id, name=f'{request.user.username} {date.strftime("%B %d")} Playlist')
        playlist_id = playlist['id']
        print(playlist_id)
        sp.playlist_add_items(playlist_id, songs)
        playlist_url = playlist["external_urls"]["spotify"]

            
    context={
    "dateForm": dateForm, 
    "entries":entries,
    "date":  date.strftime("%B %d") if date else date,
    "songs" : songs,
    "token-info":token_info, 
    "frame_key":settings.IFRAME_KEY,
    "playlist_url": playlist_url
    }

    return render(request, 'core/playlist_report.html', context)

