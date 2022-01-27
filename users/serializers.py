from rest_framework import serializers
from users.models import AppGroup, AppUser


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['url', 'username', 'email', 'groups']


class AppGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppGroup
        fields = ['url', 'name']
