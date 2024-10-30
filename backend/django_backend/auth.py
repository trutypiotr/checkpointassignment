from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication


class MyTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        if key != settings.API_TOKEN:
            raise exceptions.AuthenticationFailed()
        return AnonymousUser, None
