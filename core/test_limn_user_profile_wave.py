import pytest
from .models import User, Profile
from .test_limn_fixtures import create_user,user_one,profile_factory

def test_one_profile(user_one):
    assert user_one.username == 'user1'