import pytest
from mixer.backend.django import mixer
from posts.models import KnowHowPost, Bookmark
from tests.utils import (
    make_many_users_and_profiles,
    one_user_login,
    get_user_login,
)

pytestmark = pytest.mark.django_db


# 북마크
# 북마크 생성
@pytest.mark.skip
def test_bookmark_make_should_pass(client):
    post_1 = mixer.blend(KnowHowPost, only_me=False)
    client = one_user_login(client)
    url = "/posts/bookmarks/"
    post_title = post_1.title
    input_url = f"https://kairos-test.com/posts/{post_title}/"
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
