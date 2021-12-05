import logging


def handler(event, context) -> None:
    # Lambda handler code
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Got event:", event)