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
]
