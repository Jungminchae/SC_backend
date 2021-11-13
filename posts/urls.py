# from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import KnowHowViewSet

router = DefaultRouter()
router.register("", KnowHowViewSet)
urlpatterns = []

urlpatterns += router.urls
