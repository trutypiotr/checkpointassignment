import unittest
from unittest.mock import patch, AsyncMock
from tasks import handle_message


class TestTasks(unittest.IsolatedAsyncioTestCase):

    @patch("tasks.send_caught_message")
    @patch("tasks.fetch_patterns", new_callable=AsyncMock)
    async def test_handle_message(self, fetch_patterns_mock, send_caught_message_mock):
        fetch_patterns_mock.return_value = [
            {"id": 1, "regex": r"^\d{2}-\d{3}$", "name": "code"}
        ]

        await handle_message("12-345", 1231231.12321, "channel_id")

        send_caught_message_mock.assert_called_once_with(
            "12-345", 1, 1231231.12321, "channel_id"
        )

        fetch_patterns_mock.assert_awaited_once()
