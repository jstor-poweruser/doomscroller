import logging
import os

from tweet_processor import TweetProcessor

def handler(event, context) -> None:
    # Lambda handler code
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Got event:", event)
    tweepy_secrets = {
        'TWITTER_BEARER_TOKEN': os.environ.get('TWITTER_BEARER_TOKEN'),
        'TWITTER_CONSUMER_KEY': os.environ.get('TWITTER_CONSUMER_KEY'),
        'TWITTER_CONSUMER_SECRET': os.environ.get('TWITTER_CONSUMER_SECRET'),
        'TWITTER_ACCESS_TOKEN': os.environ.get('TWITTER_ACCESS_TOKEN'),
        'TWITTER_ACCESS_TOKEN_SECRET': os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
    }
    table_name = os.environ.get('DYNAMO_TABLE_NAME')

    process = TweetProcessor(secrets=tweepy_secrets, table_name=table_name, topic='heehee')
    process.process_tweets()
