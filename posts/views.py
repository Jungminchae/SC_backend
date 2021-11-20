from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import KnowHowPost, Photo, Video, Bookmark
from .serializers import (
    KnowHowPostSerializer,
    PhotoSerializer,
    VideoSerializer,
    BookMarkSerializer,
)
from .permissions import IsMe


# TODO: 권한 설정
# 글보기: 누구나 가능, 글쓰기: 삭제, 수정: 나만 가능
class KnowHowViewSet(ModelViewSet):
    queryset = KnowHowPost.objects.all()
    serializer_class = KnowHowPostSerializer

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

    # Knowhow 쓰기
    def create(self, request):
        # 로그인 상태의 유저만 질문하기 가능 - 기본 permission IsAuthenticaåted
        serializer = KnowHowPostSerializer(
            data=request.data, context={"request": request}
        )
        # 유효성검사
        if serializer.is_valid():
            knowhow = serializer.save(
                user=request.user,
            )
            knowhow_serializer = KnowHowPostSerializer(knowhow).data
            return Response(data=knowhow_serializer, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"])
    def knowhow_search(self, request):
        keyword = request.GET.get("keyword", None)
        # 제목 or 내용에 keyword가 포함된 object 필터링
        knowhow_list = KnowHowPost.objects.filter(
            Q(title__contains=keyword) | Q(content__contains=keyword)
        )

        # paginator
        paginator = self.paginator

        # 필터 되어 검색된 것이 있으면 return
        if len(knowhow_list):
            result = paginator.paginate_queryset(knowhow_list, request)
            serializer = KnowHowPostSerializer(result, many=True).data
            return paginator.get_paginated_response(serializer)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class PhotoViewSet(ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsMe]
        return [permission() for permission in permission_classes]


class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsMe]
        return [permission() for permission in permission_classes]


# Bookmark 보기, 생성, 수정, 삭제 나만 가능
class BookMarkViewSet(ModelViewSet):
    queryset = Bookmark
    serializer_class = BookMarkSerializer
    permission_classes = [IsMe]
