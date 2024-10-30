import json
import os

import boto3

sqs_client = boto3.client(
    "sqs",
    endpoint_url=os.getenv("SQS_URL"),
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def send_message(message: dict):
    response = sqs_client.send_message(
        QueueUrl=os.getenv("SQS_QUEUE"), MessageBody=json.dumps(message)
    )
    return response
