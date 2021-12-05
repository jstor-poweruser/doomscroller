import logging
import boto3
import tweepy

from nltk.tokenize import WordPunctTokenizer
from typing import List, Dict


class TweetProcessor:
    '''Class to poll for tweets from Twitter API, assign sentiment via Amazon Comprehend, and write negative tweets to Dynamo'''
    def __init__(self, secrets: Dict=None, table_name=None, topic=None):
        self.tweepy_client = tweepy.Client(
            bearer_token=secrets['TWITTER_BEARER_TOKEN'],
            consumer_key=secrets['TWITTER_CONSUMER_KEY'],
            consumer_secret=secrets['TWITTER_CONSUMER_SECRET'],
            access_token=secrets['TWITTER_ACCESS_TOKEN'],
            access_token_secret=secrets['TWITTER_ACCESS_TOKEN_SECRET'],
            return_type=dict,
            wait_on_rate_limit=True
        )
        self.topic = topic
        self.dynamo_table = self._get_table(table_name)
        self.comprehend = boto3.client('comprehend')
        self.logger = logging.getLogger(__name__)

    def _get_table(self, table_name) -> Object:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        return table

    def fetch_tweets(self) -> List[Dict]:
        tweets = self.tweepy_client.search_recent_tweets(
            query=f'{self.topic} lang:en -has:media -has:images -is:retweet -has:hashtags -is:reply -is:quote -has:links -has:videos',
            max_results=100,
            tweet_fields=['text', 'created_at', 'id', 'in_reply_to_user_id']
            )['data']
        for tweet in tweets:
            self.clean_tweet(tweet['text'])
        self.logger.info('Fetched and cleaned tweets from TwitterAPI')
        return tweets
        
    def clean_tweet(self, tweet: str) -> str:
        token = WordPunctTokenizer()
        words = token.tokenize(tweet)
        return (' '.join(words)).strip()

    def sentiment_analyzer(self, tweets: List) -> List[Dict]:
        negative_tweets = []
        for tweet in tweets:
            sentiment= self.comprehend.detect_sentiment(Text=tweet['text'], LanguageCode='en')['Sentiment']
            if sentiment == 'NEGATIVE':
                self.logger.info(f'Found negative tweet: {tweet}')
                negative_tweets.append(tweet)
        return negative_tweets

    def write_to_dynamo(tweets) -> None:
        try:
            for tweet in tweets:
                self.dynamo_table.put_item(item = {
                    'tweet_id': tweet['id'],
                    'created_at': tweet['created_at'],
                    'text': tweet['text'],
                    'topic': self.topic
                })
        except Exception as err:
            logger.err(f'Uh oh! Something went wrong when writing to Dynamo: {err}')
        logger.info(f'Successfully wrote {len(tweets)} tweets to DynamoDB')

    def process_tweets(self) -> None:
        tweets = self.fetch_tweets()
        negative_tweets = self.sentiment_analyzer(tweets)
        self.write_to_dynamo(negative_tweets)
