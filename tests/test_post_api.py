import json
import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from users.models import Profile
from posts.models import KnowHowPost

pytestmark = pytest.mark.django_db


def make_many_users_and_profiles(user_num):
    User = get_user_model()
    user_list = mixer.cycle(user_num).blend(User, username=None)
    profile_list = [mixer.blend(Profile, user=user) for user in user_list]
    return user_list, profile_list


def one_user_login(c):
    User = get_user_model()
    user_1 = mixer.blend(User, username=None)
    profile_1 = mixer.blend(Profile, user=user_1)
    c.force_login(user_1)
    return c


def get_user_login(c, user):
    c = c.force_login(user)
    return c


# knowhow 내가 쓴글만 모아보기
@pytest.mark.skip
def test_all_my_knowhows_should_pass(client):
    client = one_user_login(client)
    url = "/posts/knowhows/mine/"
    response = client.get(url)
    assert response.status_code == 200
    my_posts = response.json()
    tests = [response.wsgi_request.user == my_post.user for my_post in my_posts]
    assert False not in tests


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
    # 다른 사람이 볼 수 없어야함
    client.force_login(users[1])
    url = "/posts/knowhows/1/"
    response = client.get(path=url)
    assert response.status_code == 403  #


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


# ------------------------------------#

# 북마크
# 북마크 생성

# 북마크 내 리스트 불러오기

# 북마크 수정하기

# 북마크 삭제하기

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
# 코멘트
