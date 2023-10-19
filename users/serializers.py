from django.contrib.auth.models import Permission
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from knox.serializers import UserSerializer as KnoxUserSerializer
from rest_framework import serializers

from users.models import AppGroup, AppUser


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']


class BaseGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppGroup
        fields = ['id', 'name']


class ExtendedGroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model = AppGroup
        fields = ['id', 'name', "permissions"]


class CreateUpdateGroupSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all())

    def create(self, validated_data):
        permissions = validated_data.pop('permissions')

        group = AppGroup.objects.create(
            name=validated_data['name'],
        )

        for permission in permissions:
            group.permissions.add(permission)

        return group

    def update(self, instance, validated_data):
        permissions = validated_data.pop('permissions')

        instance.name = validated_data['name']

        instance.permissions.clear()
        for permission in permissions:
            instance.permissions.add(permission)
        instance.save()

        return instance

    class Meta:
        model = AppGroup
        fields = ['id', 'name', "permissions"]


class UserSerializer(serializers.ModelSerializer):
    groups = BaseGroupSerializer(many=True)

    class Meta(KnoxUserSerializer.Meta):
        model = AppUser
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "middle_name",
            "last_login",
            "is_active",
            "email",
            "is_staff",
            "is_superuser",
            "groups",
        )


class CurrentUserSerializer(UserSerializer):
    groups = BaseGroupSerializer(many=True)

    class Meta(KnoxUserSerializer.Meta):
        model = AppUser
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "middle_name",
            "last_login",
            "is_active",
            "email",
            "is_staff",
            "is_superuser",
            "groups",
        )


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    last_login = serializers.CharField(read_only=True)
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=AppGroup.objects.all())

    class Meta:
        model = AppUser
        fields = (
            "id",
            'username',
            'password',
            'password2',
            'email',
            'first_name',
            'last_name',
            "middle_name",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'is_active': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password2": _("Пароли не совпадают")})
        return attrs

    def create(self, validated_data):
        groups_data = validated_data.pop('groups')

        user = AppUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            middle_name=validated_data['middle_name'],
            is_active=validated_data['is_active'],
            is_staff=validated_data['is_staff'],
            is_superuser=validated_data['is_superuser'],
        )

        for group_data in groups_data:
            user.groups.add(group_data)

        user.set_password(validated_data['password'])
        user.save()

        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=AppGroup.objects.all())

    class Meta:
        model = AppUser
        fields = (
            "id", 'username', 'first_name', 'last_name', 'middle_name', 'is_active', 'is_staff', 'is_superuser', 'groups',)
        extra_kwargs = {
            'first_name': {'required': True},
            'is_active': {'required': True},
        }

    def update(self, instance, validated_data):
        groups_data = validated_data.pop('groups')

        instance.username = validated_data['username']
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.middle_name = validated_data['middle_name']
        instance.is_active = validated_data['is_active']
        instance.is_staff = validated_data['is_staff']
        instance.is_superuser = validated_data['is_superuser']

        instance.groups.clear()
        for group_data in groups_data:
            instance.groups.add(group_data)
        instance.save()

        return instance


class UpdateCurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ("id", 'first_name', 'last_name', 'middle_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'middle_name': {'required': True},
        }

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.middle_name = validated_data['middle_name']

        instance.save()

        return instance


class CurrentPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"})

    default_error_messages = {
        "invalid_password": _("Пароль неверный")
    }

    def validate_current_password(self, value):
        is_password_valid = self.context["request"].user.check_password(value)
        if is_password_valid:
            return value
        else:
            self.fail("invalid_password")


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={"input_type": "password"})

    def validate(self, attrs):
        try:
            validate_password(attrs["new_password"])
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        return super().validate(attrs)


class PasswordRetypeSerializer(PasswordSerializer):
    re_new_password = serializers.CharField(style={"input_type": "password"})

    default_error_messages = {
        "password_mismatch": _("Пароли не совпадают")
    }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs["new_password"] == attrs["re_new_password"]:
            return attrs
        else:
            self.fail("password_mismatch")


class ResetPasswordSerializer(PasswordRetypeSerializer):
    pass


class ChangePasswordSerializer(PasswordRetypeSerializer, CurrentPasswordSerializer):
    pass


class UserMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ('id', 'username')
