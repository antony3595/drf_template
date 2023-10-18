from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import AppUser, AppGroup
from users.serializers import CreateUserSerializer, UpdateUserSerializer, CurrentUserSerializer, \
    UpdateCurrentUserSerializer, ResetPasswordSerializer, ChangePasswordSerializer, UserMinSerializer, UserSerializer, BaseGroupSerializer, \
    CreateUpdateGroupSerializer, ExtendedGroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    ordering_fields = ['id', 'username', 'email', 'first_name', "last_name", 'role']
    ordering = "-id"

    filter_fields = ['is_active', 'is_superuser', 'is_staff', 'groups']
    search_fields = ['=id', 'username', 'email', "last_name", 'first_name', 'middle_name']

    http_method_names = ['get', 'put', 'options', 'head', 'post']

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return UserSerializer
        elif self.action == "create":
            return CreateUserSerializer
        elif self.action == "update":
            return UpdateUserSerializer
        elif self.action == "me" and self.request.method == "GET":
            return CurrentUserSerializer
        elif self.action == "me" and self.request.method == "PUT":
            return UpdateCurrentUserSerializer
        elif self.action == "reset_password":
            return ResetPasswordSerializer
        elif self.action == "change_password":
            return ChangePasswordSerializer
        elif self.action == "get_users_min":
            return UserMinSerializer
        return UserMinSerializer

    def get_instance(self):
        user = self.request.user
        self.check_object_permissions(self.request, user)
        return user

    @action(["get", "put"], detail=False, pagination_class=None)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)

    @action(["post"], detail=True)
    def reset_password(self, request, pk=None, *args, **kwargs):
        user = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['re_new_password'])
        user.save()
        return Response(status=200, data={})

    @action(["post"], url_path='me/change_password', detail=False)
    def change_password(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        user = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['re_new_password'])
        user.save()
        return Response(status=200, data={})

    @action(["post"], url_path='block', detail=True)
    def block_user(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response(status=200, data={})

    @action(["post"], url_path='unblock', detail=True)
    def unblock_user(self, request, pk=None, *args, **kwargs):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response(status=200, data={})

    @action(['get'], url_path='min', detail=False, pagination_class=None, ordering="username", permission_classes=[IsAuthenticated])
    def get_users_min(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = AppGroup.objects.all()
    serializer_class = BaseGroupSerializer
    http_method_names = ['get', 'post', 'put', 'delete', 'options', 'head']
    search_fields = ['=id', 'name']
    ordering_fields = ["id", "name"]
    ordering = "-id"

    def get_serializer_class(self):
        if self.action == "all":
            return BaseGroupSerializer
        elif self.action in ["create", "update"]:
            return CreateUpdateGroupSerializer
        return ExtendedGroupSerializer

    @action(['get'], url_path='all', detail=False, pagination_class=None)
    def all(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)
