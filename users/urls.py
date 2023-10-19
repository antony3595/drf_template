from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, GroupViewSet, PermissionsViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'permissions', PermissionsViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include('users.auth.urls')),
]
