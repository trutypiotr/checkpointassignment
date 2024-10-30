import asyncio
import json
import os

import aioboto3

from tasks import handle_message


class Manager:
    def __init__(self, queue_name: str, tasks: dict):
        self.loop = asyncio.get_event_loop()
        self.queue = queue_name
        self.tasks = tasks

    async def _get_messages(self):
        self.session = aioboto3.Session()
        async with self.session.client(
            "sqs",
            endpoint_url=os.environ.get("SQS_URL"),
            region_name=os.environ.get("AWS_REGION"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        ) as client:
            response = await client.receive_message(
                QueueUrl=self.queue,
            )
            messages = response.get("Messages", [])
            for message in messages:
                await client.delete_message(
                    QueueUrl=self.queue, ReceiptHandle=message["ReceiptHandle"]
                )
            return messages

    async def main(self):
        while True:
            messages = await self._get_messages()
            for message in messages:
                body = json.loads(message["Body"])

                task_name = body.get("task")
                args = body.get("args", ())
                kwargs = body.get("kwargs", {})

                task = self.tasks.get(task_name)
                asyncio.create_task(task(*args, **kwargs))
            await asyncio.sleep(1)


if __name__ == "__main__":
    tasks = {"check_patterns": handle_message}
    manager = Manager(queue_name=os.environ.get("SQS_QUEUE"), tasks=tasks)
    asyncio.run(manager.main())
