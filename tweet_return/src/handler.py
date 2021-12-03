import logging


def handler(event) -> None:
    # Lambda handler code
    logging.info("Got event:", event)