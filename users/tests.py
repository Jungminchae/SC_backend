import pytest
from mixer.backend.django import mixer
from django.contrib.auth import get_user_model
from users.models import Profile

pytest_mark = pytest.mark.django_db


@pytest_mark
def test_user_model_create():
    user_1 = mixer.blend(get_user_model(), username=None)
    assert isinstance(user_1.email, str) == True, "email should be str"
    assert user_1.username == None, "username is none"


@pytest_mark
def test_profile_model_create():
    user_1 = mixer.blend(get_user_model(), username=None)
    profile_1 = mixer.blend(Profile, user=user_1)
    assert user_1.profile.first().name == profile_1.name
