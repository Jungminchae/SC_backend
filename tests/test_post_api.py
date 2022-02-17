import json
import pytest
from mixer.backend.django import mixer
from posts.models import KnowHowPost, Bookmark
from tests.utils import (
    make_many_users_and_profiles,
    one_user_login,
    get_user_login,
    get_dummy_image,
)

pytestmark = pytest.mark.django_db


# knowhow 글쓰기 - 전체공개
def test_knowhow_post_should_pass(client):
    client = one_user_login(client)
    tags = json.dumps(["어그로", "짱짱"])
    url = "/posts/knowhows/"
    data = {
        "title": "안녕하세요? 마케팅의 신이 되는 노하우를 알려드립니다",
        "content": "힝 속았지? 인간이 어떻게 신이 됩니까?",
        "tags": tags,
    }
    response = client.post(path=url, data=data)
    assert response.status_code == 201


def test_knowhow_post_with_cover_should_pass(client):
    client = one_user_login(client)
    tags = json.dumps(["어그로", "짱짱"])
    url = "/posts/knowhows/"
    data = {
        "title": "안녕하세요? 커버이미지를 담은 테스트",
        "content": "커버와 함께 쓰는 테스트",
        "tags": tags,
        "cover": get_dummy_image(),
    }
    response = client.post(path=url, data=data)
    assert response.status_code == 201


# knowhow 글쓰기 - 나만보기
def test_knowhow_post_only_me_should_pass(client):
    users, _ = make_many_users_and_profiles(2)
    client.force_login(users[0])
    tags = json.dumps(["테스트", "테스트1"])
    url = "/posts/knowhows/"
    data = {
        "title": "이건 나만 보는 글이에요",
        "content": "이건 나만 보는 글이에요",
        "tags": tags,
        "only_me": True,
    }
    response = client.post(path=url, data=data)
    assert response.status_code == 201


# knowhow 나만 보기 글은 나만 볼 수 있음
def test_knowhow_other_people_see_only_me_should_not_pass(client):
    post_1 = mixer.blend(KnowHowPost, only_me=True)
    client = one_user_login(client)
    url = f"/posts/knowhows/{post_1.id}/"
    response = client.get(path=url)
    assert response.status_code == 403


# knowhow 나의 글만 모아보기
def test_knowhow_see_only_me_should_pass(client):
    users, _ = make_many_users_and_profiles(2)
    client.force_login(users[0])
    # my posts
    mixer.cycle(50).blend(KnowHowPost, user=users[0])
    # other posts
    mixer.cycle(50).blend(KnowHowPost, user=users[1])
    url = "/posts/knowhows/all-my-knowhows/"
    response = client.get(path=url)
    assert response.status_code == 200
    assert len(response.json()) == 50


# knowhow "나만 보기" 글만 보기
def test_all_my_knowhows_should_pass(client):
    users, _ = make_many_users_and_profiles(1)
    client.force_login(users[0])
    url = "/posts/knowhows/all-my-knowhows/?type=only_me"
    mixer.cycle(50).blend(KnowHowPost, user=users[0], only_me=True)
    mixer.cycle(50).blend(KnowHowPost, user=users[0], only_me=False)
    response = client.get(path=url, content_type="application/json", follow=True)
    my_posts = response.json()
    tests = [True is my_post["only_me"] for my_post in my_posts]
    assert response.status_code == 200
    assert False not in tests


# knowhow 수정 - PUT
def test_knowhow_update_should_pass(client):
    users, _ = make_many_users_and_profiles(2)
    knowhow = mixer.blend(KnowHowPost, user=users[0])
    client.force_login(users[0])
    url = f"/posts/knowhows/{knowhow.id}/"
    data = {
        "title": "I changed title",
        "content": knowhow.content,
        "tags": list(knowhow.tags.values()),
    }
    response = client.put(path=url, data=data, content_type="application/json")
    changed_knowhow = response.json()
    assert response.status_code == 200
    assert changed_knowhow["title"] != knowhow.title
    assert changed_knowhow["content"] == knowhow.content
    assert changed_knowhow["tags"] == list(knowhow.tags.values())
    # 다른 유저가 내 글을 수정할 수 없음
    client.force_login(users[1])
    response = client.put(path=url, data=data, content_type="application/json")
    assert response.status_code == 403


# knowhow 지우기
def test_knowhow_delete_should_pass(client):
    users, _ = make_many_users_and_profiles(2)
    knowhow = mixer.blend(KnowHowPost, user=users[0])
    url = f"/posts/knowhows/{knowhow.id}/"

    # 다른 유저는 내 글을 지울 수 없음
    client.force_login(users[1])
    response = client.put(path=url, content_type="application/json")
    assert response.status_code == 403
    # 글 삭제
    client.force_login(users[0])
    response = client.delete(path=url)
    assert response.status_code == 204


# knowhow 좋아요
def test_knowhow_like_and_unlike_should_pass(client):
    users, profiles = make_many_users_and_profiles(1)
    knowhow = mixer.blend(KnowHowPost, user=users[0])
    url = f"/posts/knowhows/likes/{knowhow.id}/"
    client.force_login(users[0])
    response = client.post(path=url)
    assert response.status_code == 201
    response = client.delete(path=url)
    assert response.status_code == 204


# knowhow 카테고리별 필터링
@pytest.mark.skip
def test_knowhow_filter_by_category_should_pass(client):
    # login
    # 필터링 할 때 내 글은 보여야 할까?
    client = one_user_login(client)
    knowhows = mixer.cycle(50).blend(KnowHowPost)
    category = "something"  # FIXME
    url = f"/posts/knowhows?category={category}"
    response = client.get(path=url)
    assert response.status_code == 200
    assert False not in [knowhow.category == category for knowhow in knowhows]

def test_get_all_posts_should_pass(client):
    url = "/posts/knowhows/"
    response = client.get(path=url)
    assert response.status_code == 200

# ------------------------------------#
# 사진/동영상
# 사진 올리기

# 사진 삭제

# 내 사진 보기

# 사진 수정

# 동영상 올리기

# 동영상 삭제

# 내 동영상 보기

# 동영상 수정
# ------------------------------------#
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


# 북마크 수정하기


# 북마크 삭제하기

# ------------------------------------#
