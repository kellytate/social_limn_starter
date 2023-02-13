from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def is_follower_of_user(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    A decorator to check logged in user is a follower of profile
    '''

    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_authenticated and u is in 
    )