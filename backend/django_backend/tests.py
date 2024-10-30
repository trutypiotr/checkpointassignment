from django.conf import settings
from rest_framework.test import APITestCase


class MyAPITestCase(APITestCase):
    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + settings.API_TOKEN)
