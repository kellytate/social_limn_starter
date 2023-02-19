from django.urls import path, include
# from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'core'

"""
After user is authenticated, these are the urls that will be available.
"""
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile_list', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name='profile'),
    # path('home/', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    #add path 
    # path('delete/<int:pk>', views.delete_user, name='delete_user'),
    path('remove/', views.remove_account, name='remove'),
    path('delete/', views.delete_account, name='delete'),
    path('update_profile/', views.update_user, name='update_profile'),
    path('image_upload/', views.image_upload, name='image_upload'),
    path('journals/<int:pk>/', views.journal_profile, name='journal_profile'), 
    path('journals/<int:pk>/dashboard/', views.journal_dashboard, name='journal_dashboard'),
    path('journals/<int:pk>/update/', views.update_journal, name='update_journal'),
    path('journals/<int:pk>/archive/', views.delete_journal, name='delete_journal'),
    path('journals/<int:pk>/create_entry/', views.create_entry, name='create_entry'), 
    path('entries/<int:pk>/', views.entry_landing, name='entry_landing'),
    path('entries/<int:pk>/update_entry/', views.update_entry, name='update_entry'),
    path('entries/<int:pk>/archive/', views.delete_entry, name='archive_entry'),
    path('images/<int:pk>/archive/<int:ok>', views.delete_image, name='archive_image'),
    path('comments/<int:pk>/edit_comment/', views.edit_comment, name='edit_comment'),
    path('comments/<int:pk>/archive_comment/', views.delete_comment, name='archive_comment'),
    path('comments/<int:pk>/reply/', views.reply_comment, name='reply_comment'),
    path('entries/<int:pk>/like/', views.entry_likes, name='entry_likes'),
    path('entries/<int:pk>/unlike/', views.entry_unlike, name='entry_unlike'),
    path('journals/<int:pk>/like/', views.journal_likes, name='journal_likes'),
    path('journals/<int:pk>/unlike/', views.journal_unlike, name='journal_unlike'),
    path('comments/<int:pk>/like/', views.comment_likes, name='comment_likes'),
    path('comments/<int:pk>/unlike/', views.comment_unlike, name='comment_unlike'),
    path('search/users/', views.searchUsers, name='search_users'),
    path('search/', views.search_page, name='search_page'),
    path('search/user/entries/', views.searchUserEntries, name='search_user_entries'),
    path('search/user/journals/', views.searchUserJournals, name='search_user_journals'),
    path('search/entries/', views.searchAllEntries, name='search_all_entries'),
    path('search/journals/', views.searchAllJournals, name='search_all_journals'),
    path('<int:pk>/search/spotify/', views.search_spotify, name='search_spotify'),
    path('entries/<int:pk>/song/', views.add_song, name='add_song'),
    path('notify_endpoint/', views.notify_endpoint, name='notify_endpoint'),
    path('upload/', views.upload, name='upload'),
    path('videos/<int:pk>/archive/<int:ok>/', views.delete_video, name='archive_video'),
    path('songs/<int:pk>/archive/<int:ok>/', views.delete_song, name='archive_song'),
    path('places/<int:pk>/archive/<int:ok>/', views.delete_place, name='archive_place'),
    path('entries/<int:pk>/addVideo/', views.another_video, name='add_video'),
    path('<int:pk>/search/location/', views.location_search, name='search_location'),
    path('entries/<int:pk>/place/', views.add_place, name='add_place'),
    path('profiles/<int:pk>/reports/', views.reports, name='reports'),
    path('profiles/<int:pk>/reports/entries_by_day', views.onThisDayReport, name='day_reports'),
    path('spotify_login', views.spotify_login, name="spotify_login"),
    path('profiles/<int:pk>/reports/playlist', views.spotify_report, name='spotify_report'),
    ]
