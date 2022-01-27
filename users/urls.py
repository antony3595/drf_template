from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import AppUserViewSet, AppGroupViewSet


router = DefaultRouter()
router.register(r'users', AppUserViewSet)
router.register(r'groups', AppGroupViewSet)

urlpatterns = [
    path("", include(router.urls))
]
