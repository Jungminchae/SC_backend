from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import status
from drf_multiple_model.views import ObjectMultipleModelAPIView
from .models import KnowHowPost, Photo, Video, Bookmark
from .serializers import (
    KnowHowPostSerializer,
    PhotoSerializer,
    VideoSerializer,
    BookMarkSerializer,
)
from core.utils import like_or_unlike
from core.permissions import IsMe, IsOnlyMyPost


class KnowHowViewSet(ModelViewSet):
    queryset = KnowHowPost.objects.all()
    serializer_class = KnowHowPostSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [AllowAny]
        elif self.action == "retrieve":
            permission_classes = [IsOnlyMyPost]
        else:
            permission_classes = [IsMe]
        return [permission() for permission in permission_classes]

    # "나만 보기" 설정한 유저의 글은 보이지 않음
    def get_queryset(self):
        if self.action == "list":
            queryset = super().get_queryset()
            queryset = queryset.select_related("user").filter(only_me=False)
            return queryset
        else:
            return super().get_queryset()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
            return super().perform_create(serializer)
        except ValueError:
            return serializer.error

    # 내글 모아보기
    @action(
        methods=["GET"],
        detail=False,
        url_path="all-my-knowhows",
        permission_classes=[IsMe],
    )
    def all_my_posts(self, request):
        queryset = super().get_queryset()

        if request.GET.get("type") == "only_me":
            queryset = queryset.select_related("user").filter(
                user=request.user, only_me=True
            )
        else:
            queryset = queryset.select_related("user").filter(user=request.user)

        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # @action(detail=False, methods=["GET"])
    # def knowhow_search(self, request):
    #     keyword = request.GET.get("keyword", None)
    #     # 제목 or 내용에 keyword가 포함된 object 필터링
    #     knowhow_list = KnowHowPost.objects.filter(
    #         Q(title__contains=keyword) | Q(content__contains=keyword)
    #     )

    #     # paginator
    #     paginator = self.paginator

    #     # 필터 되어 검색된 것이 있으면 return
    #     if len(knowhow_list):
    #         result = paginator.paginate_queryset(knowhow_list, request)
    #         serializer = KnowHowPostSerializer(result, many=True).data
    #         return paginator.get_paginated_response(serializer)
    #     else:
    #         return Response(status=status.HTTP_204_NO_CONTENT)


class PhotoViewSet(ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsMe]
        return [permission() for permission in permission_classes]

    # "나만 보기" 설정한 유저의 글은 보이지 않음
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related.filter(only_me=False)
        return queryset

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
            return super().perform_create(serializer)
        except ValueError:
            return serializer.error

class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsMe]
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    # "나만 보기" 설정한 유저의 글은 보이지 않음
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related.filter(only_me=False)
        return queryset

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
            return super().perform_create(serializer)
        except ValueError:
            return serializer.error


class BookMarkViewSet(ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookMarkSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsMe]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
            return super().perform_create(serializer)
        except ValueError:
            return serializer.error

    @action(methods=["GET"], detail=False)
    @permission_classes([IsMe])
    def mine(self, request):
        queryset = self.get_queryset().filter(user=self.request.user)
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class AllPostView(ObjectMultipleModelAPIView):
    querylist = [
        {"queryset": KnowHowPost.objects.all().select_related("user").filter(only_me=False), "serializer_class": KnowHowPostSerializer},
        {"queryset": Photo.objects.all(), "serializer_class": PhotoSerializer},
        {"queryset": Video.objects.all(), "serializer_class": VideoSerializer},
    ]
    permission_classes = [AllowAny]



@api_view(["POST", "DELETE"])
def like_knowhow(request, pk):
    user = request.user
    response = like_or_unlike(KnowHowPost, user, pk)
    return response


@api_view(["POST", "DELETE"])
def like_photo(request, pk):
    user = request.user
    response = like_or_unlike(Photo, user, pk)
    return response


@api_view(["POST", "DELETE"])
def like_video(request, pk):
    user = request.user
    response = like_or_unlike(Video, user, pk)
    return response
