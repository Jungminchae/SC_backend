import requests
from json.decoder import JSONDecodeError
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404, ListAPIView
from dj_rest_auth.registration.views import RegisterView
from .serializers import UserSerializer, ProfileSerializer
from .models import Profile


class SignupView(RegisterView):
    model = get_user_model()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def create(self, request):
        data = request.data
        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        if serializer.is_valid():
            profile = serializer.save(
                user=request.user,
            )
            profile_serializer = ProfileSerializer(profile)
            return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


@api_view(["POST"])
def toggle_follow(request):
    me = request.user
    email = request.data.get("email")
    followed_user = get_object_or_404(get_user_model(), email=email, is_active=True)

    following_user = Profile.objects.get(user=me)
    followed_user = Profile.objects.get(user=followed_user)

    if (followed_user in following_user.followings.all()) and (
        following_user in followed_user.followers.all()
    ):
        following_user.followings.remove(followed_user)
        followed_user.followers.remove(following_user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        following_user.followings.add(followed_user)
        followed_user.followers.add(following_user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyFollwingView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        if user.followings:
            queryset = self.queryset.filter(user__in=user.followings)
            return queryset
        return super().get_queryset()
