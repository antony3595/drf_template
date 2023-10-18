import binascii

from django.utils.translation import ugettext_lazy as _
from knox.auth import TokenAuthentication, compare_digest
from knox.crypto import hash_token
from knox.models import AuthToken
from knox.settings import CONSTANTS, knox_settings
from rest_framework import exceptions


class CustomKnoxTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, token):
        msg = _('Ваша сессия истекла! Пожалуйста, авторизуйтесь заново')
        token = token.decode("utf-8")
        for auth_token in AuthToken.objects.filter(
                token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH]):
            if self._cleanup_token(auth_token):
                continue

            try:
                digest = hash_token(token)
            except (TypeError, binascii.Error):
                raise exceptions.AuthenticationFailed(msg)
            if compare_digest(digest, auth_token.digest):
                if knox_settings.AUTO_REFRESH and auth_token.expiry:
                    self.renew_token(auth_token)
                return self.validate_user(auth_token)
        raise exceptions.AuthenticationFailed(msg)
