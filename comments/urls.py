from django.urls import include, path
from posts.views import KnowHowViewSet, PhotoViewSet, VideoViewSet
from comments.views import (
    KnowHowCommentViewSet,
    PhotoCommentViewSet,
    VideoCommentViewSet,
)
from comments.routers import SimpleNestedURL

knowhow_comment_router = SimpleNestedURL(
    KnowHowViewSet, KnowHowCommentViewSet, "knowhows", "comments", "post"
)
photo_comment_router = SimpleNestedURL(
    PhotoViewSet, PhotoCommentViewSet, "photos", "comments", "post"
)
video_comment_router = SimpleNestedURL(
    VideoViewSet, VideoCommentViewSet, "videos", "comments", "post"
)

urlpatterns = []
urlpatterns = (
    knowhow_comment_router.get_nested_registered_urls()
    + photo_comment_router.get_nested_registered_urls()
    + video_comment_router.get_nested_registered_urls()
)
