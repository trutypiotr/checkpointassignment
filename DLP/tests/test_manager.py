import json
import unittest
from unittest.mock import patch, AsyncMock

from main import Manager


class TestManager(unittest.IsolatedAsyncioTestCase):
    @patch("main.aioboto3.Session")
    def setUp(self, MockSession):
        self.queue_name = "test_queue"
        self.tasks = {"check_patterns": AsyncMock()}
        self.manager = Manager(queue_name=self.queue_name, tasks=self.tasks)

    @patch("main.aioboto3.Session")
    async def test_get_messages(self, MockSession):
        mock_client = (
            MockSession.return_value.client.return_value.__aenter__.return_value
        )
        mock_client.receive_message = AsyncMock(
            return_value={
                "Messages": [
                    {
                        "Body": json.dumps(
                            {"task": "check_patterns", "args": [1], "kwargs": {}}
                        ),
                        "ReceiptHandle": "mock_receipt_handle",
                    }
                ]
            }
        )
        mock_client.delete_message = AsyncMock()

        messages = await self.manager._get_messages()
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            json.loads(messages[0]["Body"]),
            {"task": "check_patterns", "args": [1], "kwargs": {}},
        )
        mock_client.delete_message.assert_called_once_with(
            QueueUrl=self.queue_name, ReceiptHandle="mock_receipt_handle"
        )
