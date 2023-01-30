import pytest

from .models import User, Profile


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

