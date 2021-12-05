import logging
import boto3
import os

AWS_REGION = os.environ.get('AWS_REGION')
SQS_URL = os.environ.get('SQS_URL')

def handler(event, context) -> None:
    # Lambda handler code
    logging.getLogger().setLevel(logging.INFO)
    queue = get_queue()
    response = queue.send_message(MessageBody="triggered lul")
    logging.info("Message response", response)


def get_queue():
    sqs = boto3.resource('sqs')
    queue = sqs.Queue(url=SQS_URL)
    return queue