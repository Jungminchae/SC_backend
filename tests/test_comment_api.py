import json
import pytest
from mixer.backend.django import mixer
from posts.models import KnowHowPost
from comments.models import KnowHowComment, PhotoComment, VideoComment
from tests.utils import (
    make_many_users_and_profiles,
    one_user_login,
    get_user_login,
    get_dummy_image,
)

pytestmark = pytest.mark.django_db

def test_create_comment_should_pass(client):
    client = one_user_login(client)
    # Knowhow 글 작성
    knowhow = mixer.blend(KnowHowPost)
    # comment 작성
    url = f"/comments/knowhows/{knowhow.id}/"
    data = {
        "post": knowhow.id,
        "comment": "댓글을 작성했습니다"
    }
    response = client.post(url, data)
    assert response.status_code == 201

def test_create_reply_should_pass(client):
    client = one_user_login(client)
    knowhow = mixer.blend(KnowHowPost)
    comment = mixer.blend(KnowHowComment, post=knowhow)
    url = f"/comments/knowhows/{knowhow.id}/"
    data = {
        "post": knowhow.id,
        "comment": "답글을 작성했습니다",
        "parent": comment.id
    }
    response = client.post(url, data)
    assert response.status_code == 201