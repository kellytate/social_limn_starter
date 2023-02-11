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
    path('journals/<int:pk>/update/', views.update_journal, name='update_journal')
]
