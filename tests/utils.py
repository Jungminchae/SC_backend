from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from users.models import Profile


def make_many_users_and_profiles(user_num):
    User = get_user_model()
    user_list = mixer.cycle(user_num).blend(User, username=None)
    profile_list = [mixer.blend(Profile, user=user) for user in user_list]
    return user_list, profile_list


def one_user_login(c):
    User = get_user_model()
    user_1 = mixer.blend(User, username=None)
    _ = mixer.blend(Profile, user=user_1)
    c.force_login(user_1)
    return c


def get_user_login(c, user):
    c.force_login(user)
    return c


def make_test_user():
    user = get_user_model().objects.create_user(
        email="test3355@admin.com", password="test1030911"
    )
    return user


def make_test_user_and_profile(data):
    user = make_test_user()
    profile = mixer.blend(Profile, user=user, **data)
    return user, profile
