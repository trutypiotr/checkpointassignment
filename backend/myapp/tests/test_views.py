from unittest.mock import patch

from django.urls import reverse
from django_backend.tests import MyAPITestCase
from myapp.models import Pattern, CaughtMessage


class TestPatternViews(MyAPITestCase):
    def setUp(self):
        super().setUp()
        Pattern.objects.create(name="Test Pattern 1", regex="^test1$")
        self.url = reverse("pattern-list")

    def test_get_patterns(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class TestCaughtMessagesViews(MyAPITestCase):
    def setUp(self):
        super().setUp()
        pattern = Pattern.objects.create(name="Test Pattern 1", regex="^test1$")
        self.payload = {
            "channel": "test-channel",
            "ts": "1234567890.123456",
            "pattern": pattern.id,
            "content": "message",
        }
        self.url = reverse("caught-message-create")

    @patch("myapp.views.slack_client.chat_update")
    def test_create_message(self, mock_chat_update):
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CaughtMessage.objects.count(), 1)
        mock_chat_update.assert_called_once_with(
            channel="test-channel",
            ts="1234567890.123456",
            text="Original message has been blocked",
        )
