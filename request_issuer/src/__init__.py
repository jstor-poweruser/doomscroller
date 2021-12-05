import logging


def handler(event, context) -> None:
    # Lambda handler code
    logging.info("Got event:", event)