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

# Download Model to container if it is not present
if not 'model.h5' in os.listdir('./'):
    print('---------------downloading-----------------')
    url = 'https://drive.google.com/u/0/uc?export=download&confirm=2uh4&id=1E8Xg3-gse4EhbqwM-njPJLgShYZOXwso'
    output = 'model.h5'
    gdown.download(url, output, quiet=False)
    url = 'https://drive.google.com/u/0/uc?id=1jyRAKBLM7THKRJg7XSDIe1Jt2YpzWs4o&export=download'
    output = 'tokenizer.pickle'
    gdown.download(url, output, quiet=False)

# Read ip for master node
f=open("ip.txt", "r")
couchdb_master_ip=f.readline().rstrip()
f.close()

# Inctance of couchdb connection class
couch=Couch('http://'+couchdb_master_ip+':5984/',['tweet'])

# Fetching tweetapi from db
api=couch.getdata('tweet_api')

# Twitter authentication
consumer_api_key = api['Api_Key']
consumer_api_secret = api['Api_Secret_Key']
access_token = api['Access_Token']
access_token_secret = api['Access_Secret_Token']

authorizer = OAuthHandler(consumer_api_key, consumer_api_secret)
authorizer.set_access_token(access_token, access_token_secret)
api = tweepy.API(authorizer, timeout=15, wait_on_rate_limit=True)

# Inctance of sentiment analysis class
senti=sentiment()

# Fetching tweets
while True:
    # To store tweets
    all_tweets = []
    #search_query = ''

    # Geocode and sinceid fetching from db
    loc=couch.getdata('region')
    geo=loc['code']
    curr_since_id=loc['since_id']
    #start_time = time.time()
    try:
        # First run
        if curr_since_id=="0":
            for tweet in tweepy.Cursor(api.search, q="place:%s" % geo, lang='en', result_type='recent', tweet_mode='extended').items(10000000):
                all_tweets.append({"id":str(tweet.id), "uid":str(tweet.user.id), "text":str(tweet.full_text), "created_at":str(tweet.created_at), "city":str(tweet.place.name), "country":str(tweet.place.country), "box":str(tweet.place.bounding_box.coordinates), "sentiment":str(senti.sentiment_analysis(tweet.full_text)[0][1])})
        # Consecutive runs
        else:
            for tweet in tweepy.Cursor(api.search, q="place:%s" % geo +" since_id:%s" % curr_since_id, lang='en', result_type='recent', tweet_mode='extended').items(10000000):
                all_tweets.append({"id":str(tweet.id), "uid":str(tweet.user.id), "text":str(tweet.full_text), "created_at":str(tweet.created_at), "city":str(tweet.place.name), "country":str(tweet.place.country), "box":str(tweet.place.bounding_box.coordinates), "sentiment":str(senti.sentiment_analysis(tweet.full_text)[0][1])})

        # Pushing tweets to db
        for i in all_tweets:
            couch.pushdata(i,'tweet')
            print(i)
        
        # Updating sinceid
        if all_tweets:
            couch.updatesinceid('code',geo,all_tweets[0]['id'])
    except:
        pass

    # Reset flag in region db
    couch.resetflag('code',geo,'region')
    del(all_tweets)
    #print("--- %s seconds ---" % (time.time() - start_time))
    time.sleep(45)
