from rest_framework import permissions
from rest_framework import viewsets

from users.models import AppUser, AppGroup
from users.serializers import AppUserSerializer, AppGroupSerializer


class AppUserViewSet(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'options', 'head']


class AppGroupViewSet(viewsets.ModelViewSet):
    queryset = AppGroup.objects.all()
    serializer_class = AppGroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'options', 'head']


