import pytest 
from django.contrib.auth.models import User as djangoAuthUser
from core.models import Profile, User as ourUser
from core.views import *
from core.tests.test_limn_fixtures import *


# testing client
from django.urls import reverse
@pytest.mark.django_db
def test_view(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200


# Logs in a user and gets dashboard (authenticated) view
@pytest.mark.django_db
def test_auth_view_nominal(auto_login_user):
    client, user = auto_login_user()
    url = reverse('core:dashboard')
    response = client.get(url)
    assert 'dashboard' in str(response.content)
    assert response.status_code == 200

# Logs in a user, gets profile view, checks that username is present in response
@pytest.mark.django_db
def test_profile_view_nominal(auto_login_user):
    client, user = auto_login_user()
    url = reverse('core:profile', kwargs={'pk': user.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert user.username in str(response.content)

@pytest.mark.django_db
def test_profile_list_view_nominal(auto_login_user):
    client, user = auto_login_user()
    url = reverse('core:profile_list')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_view_no_auth_does_not_render_auth_dashboard(client):
    url = reverse('core:dashboard')
    response = client.get(url)
    print(response.content)
    assert 'dashboard' not in str(response.content)
    assert response.status_code == 302
