import re

import tweepy
from tweepy import OAuthHandler

consumer_api_key = ''
consumer_api_secret = ''
access_token = ''
access_token_secret = ''
authorizer = OAuthHandler(consumer_api_key, consumer_api_secret)
authorizer.set_access_token(access_token, access_token_secret)
api = tweepy.API(authorizer, timeout=15, wait_on_rate_limit=True)
all_tweets = []
search_query = 'place:Melbourne'

for tweet in tweepy.Cursor(api.search, q=search_query + " -filter:retweets", lang='en', result_type='recent').items(5):
    all_tweets.append([tweet.text,
                       tweet.created_at, tweet.place])
print(all_tweets)
