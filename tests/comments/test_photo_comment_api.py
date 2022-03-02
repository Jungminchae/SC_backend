import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from posts.models import Photo
from comments.models import PhotoComment
from tests.utils import (
    one_user_login,
)

pytestmark = pytest.mark.django_db


def test_get_all_photo_comment_with_login_should_pass(client):
    client = one_user_login(client)
    photo = mixer.blend(Photo)
    mixer.cycle(50).blend(PhotoComment, post=photo)

    url = f"/comments/photos/{photo.id}/"
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.json()) == 50


def test_get_all_photo_comment_without_login_should_pass(client):
    photo = mixer.blend(Photo)
    mixer.cycle(50).blend(PhotoComment, post=photo)

    url = f"/comments/photos/{photo.id}/"
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.json()) == 50


def test_create_photo_comment_should_pass(client):
    client = one_user_login(client)
    # photo 글 작성
    photo = mixer.blend(Photo)
    # comment 작성
    url = f"/comments/photos/{photo.id}/"
    data = {"post": photo.id, "comment": "댓글을 작성했습니다"}
    response = client.post(url, data)
    assert response.status_code == 201
    assert response.json()["comment"] == data["comment"]


def test_edit_photo_comment_should_pass(client):
    # login
    User = get_user_model()
    user_1 = mixer.blend(User, username=None)
    client.force_login(user_1)
    # photo 글 작성
    photo = mixer.blend(Photo)
    # comment 작성
    comment = mixer.blend(PhotoComment, post=photo, user=user_1)

    url = f"/comments/photos/{photo.id}/{comment.id}/"
    data = {"comment": "댓글을 수정했습니다"}
    response = client.patch(url, data, content_type="application/json")
    assert response.status_code == 200
    assert response.json()["comment"] == data["comment"]


def test_delete_photo_comment_should_pass(client):
    # login
    User = get_user_model()
    user_1 = mixer.blend(User, username=None)
    client.force_login(user_1)
    # photo 글 작성
    photo = mixer.blend(Photo)
    # comment 작성
    comment = mixer.blend(PhotoComment, post=photo, user=user_1)
    url = f"/comments/photos/{photo.id}/{comment.id}/"
    response = client.delete(url)
    assert response.status_code == 204


def test_create_photo_reply_should_pass(client):
    client = one_user_login(client)
    photo = mixer.blend(Photo)
    comment = mixer.blend(PhotoComment, post=photo)
    url = f"/comments/photos/{photo.id}/"
    data = {"post": photo.id, "comment": "답글을 작성했습니다", "parent": comment.id}
    response = client.post(url, data)
    assert response.status_code == 201
    assert response.json()["comment"] == data["comment"]


def test_edit_photo_reply_should_pass(client):
    # login
    User = get_user_model()
    user_1 = mixer.blend(User, username=None)
    client.force_login(user_1)

    photo = mixer.blend(Photo)
    # 댓글 생성
    mixer.blend(PhotoComment, post=photo)
    # 답글 생성
    comment_2 = mixer.blend(PhotoComment, post=photo, user=user_1)

    url = f"/comments/photos/{photo.id}/{comment_2.id}/"
    data = {
        "comment": "답글을 수정했습니다",
    }
    response = client.patch(url, data, content_type="application/json")
    assert response.status_code == 200
    assert response.json()["comment"] == data["comment"]


def test_delete_photo_reply_should_pass(client):
    # login
    User = get_user_model()
    user_1 = mixer.blend(User, username=None)
    client.force_login(user_1)

    photo = mixer.blend(Photo)
    # 댓글 생성
    mixer.blend(PhotoComment, post=photo)
    # 답글 생성
    comment_2 = mixer.blend(PhotoComment, post=photo, user=user_1)

    url = f"/comments/photos/{photo.id}/{comment_2.id}/"
    response = client.delete(url)
    assert response.status_code == 204


def test_do_like_and_unlike_photo_comment_should_pass(client):
    client = one_user_login(client)

    photo = mixer.blend(Photo)
    comment = mixer.blend(PhotoComment, post=photo)

    url = f"/comments/photos/{photo.id}/{comment.id}/likes/"
    # 좋아요
    response = client.post(url)
    assert response.status_code == 201
    # 좋아요 해제
    response = client.post(url)
    assert response.status_code == 204
