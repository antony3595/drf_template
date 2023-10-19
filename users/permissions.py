from rest_framework.permissions import DjangoModelPermissions

from main.permissions import AdminModelPermission


class UserBlockPermission(DjangoModelPermissions):
    perms_map = {
        **AdminModelPermission.perms_map,
        'POST': ['%(app_label)s.delete_%(model_name)s'],
    }
