from rest_framework.routers import DefaultRouter
from .views import KnowHowCommentViewSet, PhotoCommentViewSet, VideoCommentViewSet

router = DefaultRouter()
router.register("knowhows", KnowHowCommentViewSet)
router.register("photos", PhotoCommentViewSet)
router.register("videos", VideoCommentViewSet)


urlpatterns = []

urlpatterns += router.urls
