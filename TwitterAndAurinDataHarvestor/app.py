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
search_query = ''
geo = api.geo_search(query="Melbourne", granularity="city")[0].id
print(geo)
start_time = time.time()
for tweet in tweepy.Cursor(api.search, q="place:%s" % geo, lang='en').items(2000):
    all_tweets.append([tweet.user.id, tweet.text, tweet.created_at, tweet.place])
j = 0
b=open('sport.json', "a")
for i in all_tweets:
    b.write(str(i)+"\n")
    print(j, i)
    j = j + 1

print("--- %s seconds ---" % (time.time() - start_time))
