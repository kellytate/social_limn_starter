import pytest 
from django.contrib.auth.models import User as djangoAuthUser
from core.models import Profile, User as ourUser
from core.views import *


# testing client
from django.urls import reverse
# this works
@pytest.mark.django_db
def test_view(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200

# testing our own user fixture
import uuid
@pytest.fixture
def test_password():
    return 'strong-test-pass'

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

# Logs in a user and gets dashboard (authenticated) view
@pytest.mark.django_db
def test_auth_view(auto_login_user):
    client, user = auto_login_user()
    url = reverse('core:dashboard')
    response = client.get(url)
    assert response.status_code == 200

# Logs in a user, gets profile view, checks that username is present in response
@pytest.mark.django_db
def test_profile_view(auto_login_user):
    client, user = auto_login_user()
    url = reverse('core:profile', kwargs={'pk': user.pk})
    response = client.get(url)
    assert response.status_code == 200
    print(response.content)
    assert user.username in str(response.content)
