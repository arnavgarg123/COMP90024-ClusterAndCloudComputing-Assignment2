import re
import sys
import tweepy
from tweepy import OAuthHandler

file = sys.argv[1]
a = open(file, encoding="utf8")

consumer_api_key = a.readline()[:-1].split(":")[1]
consumer_api_secret = a.readline()[:-1].split(":")[1]
access_token = a.readline()[:-1].split(":")[1]
access_token_secret = a.readline()[:-1].split(":")[1]

authorizer = OAuthHandler(consumer_api_key, consumer_api_secret)
authorizer.set_access_token(access_token, access_token_secret)
api = tweepy.API(authorizer, timeout=15, wait_on_rate_limit=True)

all_tweets = []
search_query = 'place:Melbourne'

for tweet in tweepy.Cursor(api.search, q=search_query + " -filter:retweets", lang='en', result_type='recent').items(5):
    all_tweets.append([tweet.text, tweet.created_at, tweet.place])

print(all_tweets)
