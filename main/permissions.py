from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions


class AdminModelPermission(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class AdminModelPermissionOrAnonReadonly(DjangoModelPermissions):
    authenticated_users_only = False


class CurrentUserPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return type(obj) == type(user) and obj == user
