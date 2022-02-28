import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from posts.models import KnowHowPost, Bookmark
from tests.utils import (
    make_many_users_and_profiles,
    one_user_login,
    get_user_login,
    get_user_and_client_login,
)

pytestmark = pytest.mark.django_db


# 북마크
# 북마크 생성
def test_bookmark_make_should_pass(client):
    post_1 = mixer.blend(KnowHowPost, only_me=False)
    client = one_user_login(client)
    url = "/posts/bookmarks/"
    post_title = post_1.title
    input_url = "https://kairos-test.com"
    data = {"name": post_title, "urls": input_url}
    response = client.post(path=url, data=data)
    assert response.status_code == 201


# 북마크 내 리스트 불러오기
def test_bookmark_list_should_pass(client):
    users, _ = make_many_users_and_profiles(1)
    mixer.cycle(10).blend(Bookmark, user=users[0])
    url = "/posts/bookmarks/mine/"
    client = get_user_login(client, users[0])
    response = client.get(path=url)
    assert response.status_code == 200


def test_partial_update_bookmark_name_should_pass(client):
    User = get_user_model()
    user_1 = mixer.blend(User, username=None)
    client.force_login(user_1)

    bookmark_1 = mixer.blend(Bookmark, user=user_1)
    url = f"/posts/bookmarks/{bookmark_1.id}/"
    data = {"name": "북마크 이름 변경 테스트"}
    response = client.patch(path=url, data=data, content_type="application/json")
    assert response.status_code == 200


def test_partial_update_bookmark_url_should_pass(client):
    User = get_user_model()
    user_1 = mixer.blend(User, username=None)
    client.force_login(user_1)

    bookmark_1 = mixer.blend(Bookmark, user=user_1)
    url = f"/posts/bookmarks/{bookmark_1.id}/"
    data = {"url": "https://kairos-test.com/sexy-bookmark"}
    response = client.patch(path=url, data=data, content_type="application/json")
    assert response.status_code == 200


def test_partial_update_bookmark_name_and_url_should_pass(client):
    User = get_user_model()
    user_1 = mixer.blend(User, username=None)
    client.force_login(user_1)

    bookmark_1 = mixer.blend(Bookmark, user=user_1)
    url = f"/posts/bookmarks/{bookmark_1.id}/"
    data = {"name": "북마크 이름 변경 테스트", "url": "https://kairos-test.com/sexy-bookmark"}
    response = client.patch(path=url, data=data, content_type="application/json")
    assert response.status_code == 200


def test_delete_bookmark_should_pass(client):
    logged_in_user = get_user_and_client_login(client)

    bookmark_1 = mixer.blend(Bookmark, user=logged_in_user)
    url = f"/posts/bookmarks/{bookmark_1.id}/"
    response = client.delete(path=url)
    assert response.status_code == 204
