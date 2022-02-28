import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from posts.models import Video
from comments.models import VideoComment
from tests.utils import (
    one_user_login,
)

pytestmark = pytest.mark.django_db


def test_get_all_video_comment_with_login_should_pass(client):
    client = one_user_login(client)
    video = mixer.blend(Video)
    mixer.cycle(50).blend(VideoComment, post=video)

    url = f"/comments/videos/{video.id}/"
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.json()) == 50


def test_get_all_video_comment_without_login_should_pass(client):
    video = mixer.blend(Video)
    mixer.cycle(50).blend(VideoComment, post=video)

    url = f"/comments/videos/{video.id}/"
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.json()) == 50


def test_create_video_comment_should_pass(client):
    client = one_user_login(client)
    # video 글 작성
    video = mixer.blend(Video)
    # comment 작성
    url = f"/comments/videos/{video.id}/"
    data = {"post": video.id, "comment": "댓글을 작성했습니다"}
    response = client.post(url, data)
    assert response.status_code == 201
    assert response.json()["comment"] == data["comment"]


def test_edit_video_comment_should_pass(client):
    # login
    User = get_user_model()
    user_1 = mixer.blend(User, username=None)
    client.force_login(user_1)
    # video 글 작성
    video = mixer.blend(Video)
    # comment 작성
    comment = mixer.blend(VideoComment, post=video, user=user_1)

    url = f"/comments/videos/{video.id}/{comment.id}/"
    data = {"comment": "댓글을 수정했습니다"}
    response = client.patch(url, data, content_type="application/json")
    assert response.status_code == 200
    assert response.json()["comment"] == data["comment"]


def test_delete_video_comment_should_pass(client):
    # login
    User = get_user_model()
    user_1 = mixer.blend(User, username=None)
    client.force_login(user_1)
    # video 글 작성
    video = mixer.blend(Video)
    # comment 작성
    comment = mixer.blend(VideoComment, post=video, user=user_1)
    url = f"/comments/videos/{video.id}/{comment.id}/"
    response = client.delete(url)
    assert response.status_code == 204


def test_create_video_reply_should_pass(client):
    client = one_user_login(client)
    video = mixer.blend(Video)
    comment = mixer.blend(VideoComment, post=video)
    url = f"/comments/videos/{video.id}/"
    data = {"post": video.id, "comment": "답글을 작성했습니다", "parent": comment.id}
    response = client.post(url, data)
    assert response.status_code == 201
    assert response.json()["comment"] == data["comment"]


def test_edit_video_reply_should_pass(client):
    # login
    User = get_user_model()
    user_1 = mixer.blend(User, username=None)
    client.force_login(user_1)

    video = mixer.blend(Video)
    # 댓글 생성
    mixer.blend(VideoComment, post=video)
    # 답글 생성
    comment_2 = mixer.blend(VideoComment, post=video, user=user_1)

    url = f"/comments/videos/{video.id}/{comment_2.id}/"
    data = {
        "comment": "답글을 수정했습니다",
    }
    response = client.patch(url, data, content_type="application/json")
    assert response.status_code == 200
    assert response.json()["comment"] == data["comment"]


def test_delete_video_reply_should_pass(client):
    # login
    User = get_user_model()
    user_1 = mixer.blend(User, username=None)
    client.force_login(user_1)

    video = mixer.blend(Video)
    # 댓글 생성
    mixer.blend(VideoComment, post=video)
    # 답글 생성
    comment_2 = mixer.blend(VideoComment, post=video, user=user_1)

    url = f"/comments/videos/{video.id}/{comment_2.id}/"
    response = client.delete(url)
    assert response.status_code == 204


def test_do_like_and_unlike_video_comment_should_pass(client):
    client = one_user_login(client)

    video = mixer.blend(Video)
    comment = mixer.blend(VideoComment, post=video)

    url = f"/comments/videos/{video.id}/{comment.id}/likes/"
    # 좋아요
    response = client.post(url)
    assert response.status_code == 201
    # 좋아요 해제
    response = client.post(url)
    assert response.status_code == 204
