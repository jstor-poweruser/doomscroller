import logging
import os
import boto3
import tweepy

from typing import List
from datetime import datetime

def handler(event, context) -> None:
    # Lambda handler code
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Got event:", event)

def fetch_tweets(topic: str) -> List:
    twitter_bearer_token = os.environ.get('TWITTER_BEARER_TOKEN')
    twitter_consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
    twitter_consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
    twitter_access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
    twitter_access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

    tweepy_client = tweepy.Client(
        bearer_token=twitter_bearer_token,
        consumer_key=twitter_consumer_key,
        consumer_secret=twitter_consumer_secret,
        access_token=twitter_access_token,
        access_token_secret=twitter_access_token_secret,
        wait_on_rate_limit=True
        )

    today = datetime.today().strftime('%Y-%m-%d')

    tweets = tweepy.