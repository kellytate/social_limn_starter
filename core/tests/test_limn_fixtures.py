import pytest
from django.contrib.auth.models import User as djangoAuthUser
from core.views import *
from core.models import User, Profile


@pytest.fixture
def create_user(username):
    return User.objects.create(username)

@pytest.fixture
def profile_factory(create_user, username, email=None, bio=None, location=None, spotify_auth=None, follows=None,):
    new_user = create_user(username)
    profile = Profile.objects.create(
        user=new_user,
        follows=follows,
        email=email,
        bio=bio,
        locaiton = location,
        spotify_auth=spotify_auth
    )

@pytest.fixture
def user_one(profile_factory):
    return profile_factory('user1','email','bio','location','spotify')


# testing our own user fixture
import uuid
@pytest.fixture
def test_password():
    return 'strong-test-pass'

# Tests authenticated user
@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)
    return make_user


# Creates and logs in a user
@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(username=user.username, password=test_password)
        return client, user
    return make_auto_login

