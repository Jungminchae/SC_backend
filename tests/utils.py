import random
import string
import tempfile
import requests
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from users.models import Profile


# 다수의 유저 리스트와 프로필 리스트 생성하기
def make_many_users_and_profiles(user_num):
    User = get_user_model()
    user_list = mixer.cycle(user_num).blend(User, username=None)
    profile_list = [mixer.blend(Profile, user=user) for user in user_list]
    return user_list, profile_list


# 1명의 유저 로그인
def one_user_login(c):
    User = get_user_model()
    user_1 = mixer.blend(User, username=None)
    _ = mixer.blend(Profile, user=user_1)
    c.force_login(user_1)
    return c


# TODO: 삭제
# 1명의 유저만 로그인 profile X
def get_user_login(c, user):
    c.force_login(user)
    return c


# TODO: 삭제
# 1명의 테스트 유저 생성
def make_test_user():
    user = get_user_model().objects.create_user(
        email="test3355@admin.com", password="test1030911"
    )
    return user


# 1명의 유저와 프로필 만들기
def make_test_user_and_profile(data):
    user = make_test_user()
    profile = mixer.blend(Profile, user=user, **data)
    return user, profile


# 이미지 업로드 테스트용 이미지 가져오기 from picsum
def get_dummy_image(image_number):
    url = f"https://picsum.photos/id/{image_number}/256/256"
    image = requests.get(url)
    with tempfile.NamedTemporaryFile(suffix=".jpg", dir="./") as f:
        f.write(image.content)
        byte_image = open(f.name, "rb")
    return byte_image


def get_simple_uploaded_file():
    fake_name = "".join(
        [random.choice(string.ascii_letters + string.digits) for _ in range(10)]
    )
    uploaded_photo = SimpleUploadedFile(
        f"{fake_name}.jpeg", b"file_content", content_type="multipart/form-data"
    )
    return uploaded_photo


def get_user_and_client_login(client):
    User = get_user_model()
    user_1 = mixer.blend(User, username=None)
    client.force_login(user_1)
    return user_1
