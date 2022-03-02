import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from posts.models import KnowHowPost
from comments.models import KnowHowComment
from tests.utils import (
    one_user_login,
)

pytestmark = pytest.mark.django_db


def test_knowhow_comment_after_profile_deleted():
    comment = mixer.blend(KnowHowComment)
    comment_id = comment.id
    profile = comment.profile
    profile.delete()

    comment = KnowHowComment.objects.get(id=comment_id)

    assert comment.profile is None


def test_get_all_knowhow_comment_with_login_should_pass(client):
    client = one_user_login(client)
    knowhow = mixer.blend(KnowHowPost)
    mixer.cycle(50).blend(KnowHowComment, post=knowhow)

    url = f"/comments/knowhows/{knowhow.id}/"
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.json()) == 50


def test_get_all_knowhow_comment_without_login_should_pass(client):
    knowhow = mixer.blend(KnowHowPost)
    mixer.cycle(50).blend(KnowHowComment, post=knowhow)

    url = f"/comments/knowhows/{knowhow.id}/"
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.json()) == 50


def test_create_knowhow_comment_should_pass(client):
    client = one_user_login(client)
    # Knowhow 글 작성
    knowhow = mixer.blend(KnowHowPost)
    # comment 작성
    url = f"/comments/knowhows/{knowhow.id}/"
    data = {"post": knowhow.id, "comment": "댓글을 작성했습니다"}
    response = client.post(url, data)
    assert response.status_code == 201
    assert response.json()["comment"] == data["comment"]


def test_edit_knowhow_comment_should_pass(client):
    # login
    User = get_user_model()
    user_1 = mixer.blend(User, username=None)
    client.force_login(user_1)
    # Knowhow 글 작성
    knowhow = mixer.blend(KnowHowPost)
    # comment 작성
    comment = mixer.blend(KnowHowComment, post=knowhow, user=user_1)

    url = f"/comments/knowhows/{knowhow.id}/{comment.id}/"
    data = {"comment": "댓글을 수정했습니다"}
    response = client.patch(url, data, content_type="application/json")
    assert response.status_code == 200
    assert response.json()["comment"] == data["comment"]


def test_delete_knowhow_comment_should_pass(client):
    # login
    User = get_user_model()
    user_1 = mixer.blend(User, username=None)
    client.force_login(user_1)
    # Knowhow 글 작성
    knowhow = mixer.blend(KnowHowPost)
    # comment 작성
    comment = mixer.blend(KnowHowComment, post=knowhow, user=user_1)
    url = f"/comments/knowhows/{knowhow.id}/{comment.id}/"
    response = client.delete(url)
    assert response.status_code == 204


def test_create_knowhow_reply_should_pass(client):
    client = one_user_login(client)
    knowhow = mixer.blend(KnowHowPost)
    comment = mixer.blend(KnowHowComment, post=knowhow)
    url = f"/comments/knowhows/{knowhow.id}/"
    data = {"post": knowhow.id, "comment": "답글을 작성했습니다", "parent": comment.id}
    response = client.post(url, data)
    assert response.status_code == 201
    assert response.json()["comment"] == data["comment"]


def test_edit_knowhow_reply_should_pass(client):
    # login
    User = get_user_model()
    user_1 = mixer.blend(User, username=None)
    client.force_login(user_1)

    knowhow = mixer.blend(KnowHowPost)
    # 댓글 생성
    mixer.blend(KnowHowComment, post=knowhow)
    # 답글 생성
    comment_2 = mixer.blend(KnowHowComment, post=knowhow, user=user_1)

    url = f"/comments/knowhows/{knowhow.id}/{comment_2.id}/"
    data = {
        "comment": "답글을 수정했습니다",
    }
    response = client.patch(url, data, content_type="application/json")
    assert response.status_code == 200
    assert response.json()["comment"] == data["comment"]


def test_delete_knowhow_reply_should_pass(client):
    # login
    User = get_user_model()
    user_1 = mixer.blend(User, username=None)
    client.force_login(user_1)

    knowhow = mixer.blend(KnowHowPost)
    # 댓글 생성
    mixer.blend(KnowHowComment, post=knowhow)
    # 답글 생성
    comment_2 = mixer.blend(KnowHowComment, post=knowhow, user=user_1)

    url = f"/comments/knowhows/{knowhow.id}/{comment_2.id}/"
    response = client.delete(url)
    assert response.status_code == 204


def test_do_like_and_unlike_knowhow_comment_should_pass(client):
    client = one_user_login(client)

    knowhow = mixer.blend(KnowHowPost)
    comment = mixer.blend(KnowHowComment, post=knowhow)

    url = f"/comments/knowhows/{knowhow.id}/{comment.id}/likes/"
    # 좋아요
    response = client.post(url)
    assert response.status_code == 201
    # 좋아요 해제
    response = client.post(url)
    assert response.status_code == 204
