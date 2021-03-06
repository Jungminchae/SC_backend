from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    KnowHowViewSet,
    PhotoViewSet,
    VideoViewSet,
    BookMarkViewSet,
    AllPostView,
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
    path("knowhows/likes/<int:pk>/", like_knowhow, name="like-or-unlike-knowhow"),
    path("photos/likes/<int:pk>/", like_photo, name="like-or-unlike-photo"),
    path("videos/likes/<int:pk>/", like_video, name="like-or-unlike-video"),
    path("all/", AllPostView.as_view(), name="all-posts"),
]

urlpatterns += router.urls
