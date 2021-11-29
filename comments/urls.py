from rest_framework.routers import DefaultRouter
from .views import KnowHowCommentViewSet, PhotoCommentViewSet, VideoCommentViewSet

router = DefaultRouter()
router.register(r"knowhows/(?P<post_id>\d+)", KnowHowCommentViewSet)
router.register(r"photos/(?P<post_id>\d+)", PhotoCommentViewSet)
router.register(r"videos/(?P<post_id>\d+)", VideoCommentViewSet)


urlpatterns = []

urlpatterns += router.urls
