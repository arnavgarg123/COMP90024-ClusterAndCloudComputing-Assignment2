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
#  * Gurkirat Singh Chohan (Student ID: 1226595)
#
# Location: India, Melbourne, Singapore
#
import re
import time
import gdown
import tweepy
from tweepy import OAuthHandler
import os
from sentiment_analyse import sentiment
from dbconnector import Couch

if not 'model.h5' in os.listdir('./'):
    print('---------------downloading-----------------')
    url = 'https://drive.google.com/u/0/uc?export=download&confirm=2uh4&id=1E8Xg3-gse4EhbqwM-njPJLgShYZOXwso'
    output = 'model.h5'
    gdown.download(url, output, quiet=False)
    url = 'https://drive.google.com/u/0/uc?id=1jyRAKBLM7THKRJg7XSDIe1Jt2YpzWs4o&export=download'
    output = 'tokenizer.pickle'
    gdown.download(url, output, quiet=False)
f=open("ip_addresses.txt", "r")
couchdb_master_ip=f.readline().rstrip()
f.close()
couch=Couch('http://'+couchdb_master_ip+':5984/',['tweet'])
api=couch.getdata('tweet_api')
consumer_api_key = api['Api_Key']
consumer_api_secret = api['Api_Secret_Key']
access_token = api['Access_Token']
access_token_secret = api['Access_Secret_Token']

authorizer = OAuthHandler(consumer_api_key, consumer_api_secret)
authorizer.set_access_token(access_token, access_token_secret)
api = tweepy.API(authorizer, timeout=15, wait_on_rate_limit=True)

senti=sentiment()

while True:
    all_tweets = []
    search_query = ''
    #geo = api.geo_search(query="Sydney", granularity="city")[0].id
    loc=couch.getdata('region')
    geo=loc['code']
    start_time = time.time()

    #for tweet in tweepy.Cursor(api.search, q="place:%s" % geo +" since_id:%s" % '1388256536070262788', lang='en', result_type='recent').items(1000000):
        #all_tweets.append({​"id":str(tweet.id), "uid":str(tweet.user.id), "text":str(tweet.text), "created_at":str(tweet.created_at), "city":str(tweet.place.name), "country":str(tweet.place.country), "box":str(tweet.place.bounding_box.coordinates)}​)

    for tweet in tweepy.Cursor(api.search, q="place:%s" % geo, lang='en', result_type='recent').items(10):
        all_tweets.append({"id":str(tweet.id), "uid":str(tweet.user.id), "text":str(tweet.text), "created_at":str(tweet.created_at), "city":str(tweet.place.name), "country":str(tweet.place.country), "box":str(tweet.place.bounding_box.coordinates), "sentiment":str(senti.sentiment_analysis(tweet.text)[0][1])})
    for i in all_tweets:
        couch.pushdata(i,'tweet')
        print(i)
    del(all_tweets)
    print("--- %s seconds ---" % (time.time() - start_time))
