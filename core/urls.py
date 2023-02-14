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
    path('home/', views.home, name='home'),
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
    path('journals/<int:pk>/create_entry/', views.create_entry, name='create_entry'), 
    path('entries/<int:pk>/', views.entry_landing, name='entry_landing'),
    path('entries/<int:pk>/update_entry/', views.update_entry, name='update_entry'),
    path('comments/<int:pk>/edit_comment/', views.edit_comment, name='edit_comment'),
    path('entries/<int:pk>/like/', views.entry_likes, name='entry_likes'),
    path('entries/<int:pk>/unlike/', views.entry_unlike, name='entry_unlike'),
    path('journals/<int:pk>/like/', views.journal_likes, name='journal_likes'),
    path('journals/<int:pk>/unlike/', views.journal_unlike, name='journal_unlike'),
    path('comments/<int:pk>/like/', views.comment_likes, name='comment_likes'),
    path('comments/<int:pk>/unlike/', views.comment_unlike, name='comment_unlike'),
    path('search/users/', views.searchUsers, name='search_users'),
    path('search/', views.search_page, name='search_page'),
    path('search/user/entries', views.searchUserEntries, name='search_user_entries'),
    path('search/user/journals', views.searchUserJournals, name='search_user_journals'),

]
