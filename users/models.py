from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import gettext_lazy as _


class AppUser(AbstractUser):
    class Meta:
        ordering = ["id"]
        verbose_name = _('user')
        verbose_name_plural = _('users')


class AppGroup(Group):
    class Meta:
        proxy = True
        verbose_name = _('group')
        verbose_name_plural = _('groups')
