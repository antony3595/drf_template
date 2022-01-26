from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import gettext_lazy as _


class AppUser(AbstractUser):
    pass


class AppGroup(Group):
    class Meta:
        proxy = True
        verbose_name = _('group')
        verbose_name_plural = _('groups')
