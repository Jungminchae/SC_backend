import requests
from json.decoder import JSONDecodeError
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter


STATE = settings.STATE
GOOGLE_CALLBACK_URI = settings.GOOGLE_CALLBACK_URI
GOOGLE_CLIENT_ID = settings.SOCIAL_AUTH_GOOGLE_CLIENT_ID
GOOGLE_SECRET = settings.SOCIAL_AUTH_GOOGLE_SECRET


# 비동기 호출 불가
def google_login(request):
    """
    Code Request
    """
    scope = "https://www.googleapis.com/auth/userinfo.email"
    return redirect(
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={GOOGLE_CLIENT_ID}"
        f"&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}"
    )


def google_callback(request):
    code = request.GET.get("code")
    """
    Access Token Request
    """
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={GOOGLE_CLIENT_ID}"
        f"&client_secret={GOOGLE_SECRET}"
        f"&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}"
        f"&state={STATE}"
    )
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")
    """
    Email Request
    """
    email_req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}"
    )
    email_req_status = email_req.status_code
    if email_req_status != 200:
        return JsonResponse(
            {"err_msg": "failed to get email"}, status=status.HTTP_400_BAD_REQUEST
        )
    email_req_json = email_req.json()
    email = email_req_json.get("email")

    User = get_user_model()

    """
    Signup or Signin Request
    """
    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse(
                {"err_msg": "email exists but not social user"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if social_user.provider != "google":
            return JsonResponse(
                {"err_msg": "no matching social type"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 기존에 Google로 가입된 유저
        data = {"access_token": access_token, "code": code}
        accept = requests.post(
            f"{settings.BASE_URL}users/google/login/finish/", data=data
        )
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)
        accept_json = accept.json()
        # accept_json.pop("user", None)
        return JsonResponse(accept_json, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {"access_token": access_token, "code": code}
        accept = requests.post(
            f"{settings.BASE_URL}users/google/login/finish/", data=data
        )
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop("user", None)
        return JsonResponse(accept_json, status=status.HTTP_201_CREATED)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


@api_view(["POST"])
def follow_user(request):
    """
    내가 팔로우 할 사람 이메일을 받아 -> 그 사람이 존재하는지 체크 ->
    존재하면 팔로우, 존재하지 않으면 404
    """
    me = request.user
    email = request.data["email"]
    followed_user = get_object_or_404(get_user_model(), email=email, is_active=True)
    # 내 팔로잉 목록에 추가
    me.followings.add(followed_user)
    # 상대방 팔로워 목록에 나 추가
    followed_user.followers.add(me)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def unfollow_user(request):
    """
    내가 언팔로우 할 사람 이메일을 받아 -> 그 사람이 존재하는지 체크 ->
    존재하면 언팔로우, 존재하지 않으면 404
    """
    me = request.user
    email = request.data["email"]
    followed_user = get_object_or_404(get_user_model(), email=email, is_active=True)
    # 내팔로잉 목록에서 제거
    me.followings.remove(followed_user)
    # 상대방 팔로워 목록에 나 제거
    followed_user.followers.remove(me)
    return Response(status=status.HTTP_204_NO_CONTENT)
