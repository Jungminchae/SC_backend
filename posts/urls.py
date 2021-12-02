from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    KnowHowViewSet,
    PhotoViewSet,
    VideoViewSet,
    BookMarkViewSet,
    like_knowhow,
    like_photo,
    like_video,
)

router = DefaultRouter()
router.register("knowhows", KnowHowViewSet)
router.register("photos", PhotoViewSet)
router.register("videos", VideoViewSet)
router.register("bookmarks", BookMarkViewSet)

urlpatterns = [
    path("knowhows/<int:pk>", like_knowhow, name="like-or-unlike-knowhow"),
    path("photos/<int:pk>", like_photo, name="like-or-unlike-photo"),
    path("videos/<int:pk>", like_video, name="like-or-unlike-video"),
]

urlpatterns += router.urls
