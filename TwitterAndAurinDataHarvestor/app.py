# Assignment 2 - COMP90024 Course at The University of Melbourne
#
# Cluster and Cloud Computing - Team 48
#
# Authors:
#
#  * Arnav Garg (Student ID: 1248298)
#  * Piyush Bhandula (Student ID: 1163716)
#  * Jay Dave (Student ID: 1175625)
#  * Vishnu Priya G (Student ID: 1230719)
#  * Gurkirat Singh Chohan 1226595
#
# Location: India, Melbourne, Singapore
#
import re
import sys
import time
import gdown
import tweepy
from tweepy import OAuthHandler
import os
from sentiment_analyse import sentiment

file = sys.argv[1]
a = open(file, encoding="utf8")

if not 'model.h5' in os.listdir('./'):
    print('---------------downloading-----------------')
    url = 'https://drive.google.com/u/0/uc?export=download&confirm=2uh4&id=1E8Xg3-gse4EhbqwM-njPJLgShYZOXwso'
    output = 'model.h5'
    gdown.download(url, output, quiet=False)
    url = 'https://drive.google.com/u/0/uc?id=1jyRAKBLM7THKRJg7XSDIe1Jt2YpzWs4o&export=download'
    output = 'tokenizer.pickle'
    gdown.download(url, output, quiet=False)

consumer_api_key = a.readline()[:-1].split(":")[1]
consumer_api_secret = a.readline()[:-1].split(":")[1]
access_token = a.readline()[:-1].split(":")[1]
access_token_secret = a.readline()[:-1].split(":")[1]

authorizer = OAuthHandler(consumer_api_key, consumer_api_secret)
authorizer.set_access_token(access_token, access_token_secret)
api = tweepy.API(authorizer, timeout=15, wait_on_rate_limit=True)

senti=sentiment()

while True:
    all_tweets = []
    search_query = ''
    #geo = api.geo_search(query="Sydney", granularity="city")[0].id
    geo='0073b76548e5984f'
    print(geo)
    start_time = time.time()

    

    for tweet in tweepy.Cursor(api.search, q="place:%s" % geo, lang='en', result_type='recent').items(10):
        all_tweets.append([tweet.user.id, tweet.text, tweet.created_at, tweet.place, senti.sentiment_analysis(tweet.text)[0][1]])

    for i in all_tweets:
        print(i[-1],i[1])
    del(all_tweets)
    print("--- %s seconds ---" % (time.time() - start_time))
