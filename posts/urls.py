# from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import KnowHowViewSet, PhotoViewSet, VideoViewSet

router = DefaultRouter()
router.register("knowhows", KnowHowViewSet)
router.register("photos", PhotoViewSet)
router.register("videos", VideoViewSet)

urlpatterns = []

urlpatterns += router.urls
