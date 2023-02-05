import pytest
from core.models import Profile
from core.models import User as our_user
from django.contrib.auth.models import User
from .test_limn_fixtures import create_user,user_one,profile_factory

@pytest.fixture
@pytest.mark.django_db
def create_user(django_user_model):
    def make_user(**kwargs):
        return django_user_model.objects.create_user(**kwargs)
    return make_user

# @pytest.mark.django_db
def test_create_one_user(create_user):
    user_name = "Test_name"
    expected = "Test_name"


    new_user = create_user(username=user_name)
    assert new_user.username == expected
    assert new_user.id == 1

# @pytest.mark.django_db
def test_create_multiple_users(create_user):
    
    name_one = "first_name"
    name_two = "second_name"
    name_three = "more_name"

    first_user = create_user(username=name_one)
    second_user=create_user(username=name_two)
    third_user = create_user(username=name_three)

    assert first_user.id == 2
    assert second_user.id == 3
    assert third_user.id == 4

    assert first_user.username == "first_name"
    assert second_user.username == "second_name"
    assert third_user.username == "more_name"
    

