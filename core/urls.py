from django.urls import path, include
# from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'core'

"""
Django auth provides views for login, logout, and password management under
'accounts/'. We have to provide the template/html/react for those. 
"""
urlpatterns = [
    # path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('signup/', views.signup, name='signup'),
    path('profile_list', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name='profile'),
    # path('accounts/login', LoginView.as_view(), name='login_url'),

]
