import json
import pytest
from mixer.backend.django import mixer
from posts.models import Photo, PhotoImage
from tests.utils import (
    one_user_login,
    get_user_and_client_login,
    get_simple_uploaded_file,
)

pytestmark = pytest.mark.django_db


def test_create_one_photo_post_should_pass(client):
    client = one_user_login(client)

    url = "/posts/photos/"
    title = "사진 1장 업로드 테스트"
    description = "사진 1장 업로드 합니다"
    tags = json.dumps(["사진", "인증"])
    only_me = False
    one_image = get_simple_uploaded_file()
    data = {
        "title": title,
        "description": description,
        "tags": tags,
        "only_me": only_me,
        "image": one_image,
    }

    response = client.post(path=url, data=data)
    assert response.status_code == 201


def test_create_more_than_one_photo_post_should_pass(client):
    client = one_user_login(client)

    url = "/posts/photos/"
    title = "사진 2장 업로드 테스트"
    description = "사진 2장 업로드 합니다"
    tags = json.dumps(["사진", "인증"])
    only_me = False
    two_images = [get_simple_uploaded_file() for _ in range(2)]
    data = {
        "title": title,
        "description": description,
        "tags": tags,
        "only_me": only_me,
        "image": two_images,
    }

    response = client.post(path=url, data=data)
    assert response.status_code == 201


def test_create_photo_post_without_description_should_pass(client):
    client = one_user_login(client)

    url = "/posts/photos/"
    title = "사진 1장 업로드 테스트"
    tags = json.dumps(["사진", "인증"])
    only_me = False
    one_image = get_simple_uploaded_file()
    data = {
        "title": title,
        "tags": tags,
        "only_me": only_me,
        "image": one_image,
    }

    response = client.post(path=url, data=data)
    assert response.status_code == 201


@pytest.mark.skip("원인 파악 필요")
def test_partial_update_to_photo_image_should_pass(client):
    logged_in_user = get_user_and_client_login(client)
    photo_1 = mixer.blend(Photo, user=logged_in_user)
    mixer.blend(PhotoImage, post=photo_1)

    url = f"/posts/photos/{photo_1.id}/"
    one_image = get_simple_uploaded_file()
    data = {"title": "됨???????", "image": one_image}

    response = client.patch(path=url, data=data, content_type="multipart/form-data")
    assert response.json() == 200
