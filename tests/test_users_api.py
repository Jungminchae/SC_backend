import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from rest_framework.reverse import reverse
from users.models import Profile

pytest_mark = pytest.mark.django_db


def make_test_user():
    user = get_user_model().objects.create_user(
        email="test3355@admin.com", password="test1030911"
    )
    return user


# ------------------------------------#
@pytest_mark
def test_register_with_email(client):
    url = reverse("sign-up-email")
    data = {
        "email": "test3355@admin.com",
        "password1": "test1030911",
        "password2": "test1030911",
    }
    response = client.post(url, data)
    assert response.status_code == 201


# ------------------------------------#
@pytest_mark
def test_make_profile_should_pass(client):
    user_1 = make_test_user()
    client.force_login(user_1)
    url = "/users/profiles/"
    # avatart 생략 가능
    data = {"name": "testmon", "bio": "안녕하세요!"}
    # profile create
    response = client.post(url, data)
    assert response.status_code == 201


@pytest_mark
def test_make_profile_should_not_pass(client):
    # login 없이 생성 불가
    url = "/users/profiles/"
    data = {"name": "testmon", "bio": "안녕하세요!"}
    response = client.post(url, data)
    assert response.status_code == 403


# ------------------------------------#
@pytest_mark
def test_follow_and_unfollow_user(client):
    # user & profile create
    user_1 = make_test_user()
    profile_1 = mixer.blend(Profile, user=user_1)
    user_2 = mixer.blend(get_user_model(), username=None)
    profile_2 = mixer.blend(Profile, user=user_2)
    # login
    client.force_login(user_1)
    url = reverse("toggle-follow")
    data = {"email": user_2.email}
    # follow
    response_1 = client.post(url, data)
    assert response_1.status_code == 204
    assert profile_2 == profile_1.followings.first()
    assert profile_1 == profile_2.followers.first()
    # # unfollow
    response_2 = client.post(url, data)
    assert response_2.status_code == 204
    assert profile_1.followings.first() is None
    assert profile_2.followers.first() is None
