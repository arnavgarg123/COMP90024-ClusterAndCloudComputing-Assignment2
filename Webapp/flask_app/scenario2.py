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
import pandas as pd
import re
from textblob import TextBlob
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS
import couchdb
import xlsxwriter

# Loading Covid tweets
def covid_save_data():
    a=open('./ip.txt')
    a=a.readline()
    a=a.strip()
    a='http://'+a+':5984/'
    couchserver=couchdb.Server(url=a)
    couchserver.resource.credentials=('admin','admin')
    c=[]
    b=couchserver['tweet']
    for i in b.view('all_doc/covid'):
        c=c+[i.key]
    workbook = xlsxwriter.Workbook('./static/data_files/covidtweets_couchdb.xlsx')
    worksheet = workbook.add_worksheet()
    row=0
    col=0
    li=['ID','UID','Text','Created_At','City','Country','Co-ordinates','Sentiment']
    for j in li:
        worksheet.write(row, col, j)
        col=col+1
    row=row+1
    for i in c:
        col=0
        for j in i:
            worksheet.write(row, col, j)
            col=col+1
        row=row+1
    workbook.close()
covid_save_data()
# Loading Data
df = pd.read_excel('./static/data_files/covidtweets_couchdb.xlsx',sheet_name='Sheet1', engine='openpyxl')
dft = pd.read_excel('./static/data_files/tweets_couchdb.xlsx',sheet_name='Sheet1', engine='openpyxl')

# Generating Word Cloud
def generate_word_cloud():
    covid_df = df[df['Text'].str.contains('covid|vaccin', flags=re.IGNORECASE)]
    stop_words = ["https", "will", "co", "amp", "n", "t"] + list(STOPWORDS)
    text = ' '.join(covid_df['Text'])
    text = text.encode("ascii", "ignore").decode('utf-8')
    wordcloud = WordCloud(width=400, height=320, random_state=1,
                          background_color='black', colormap='Set1',
                          collocations=False, stopwords=stop_words).generate(text)
    return wordcloud

# Polarity and subjectivy score calculator
def generate_scores():
    covid_df = df[df['Text'].str.contains('covid|vaccin', flags=re.IGNORECASE)]
    covid_df['polarity'] = covid_df['Text'].apply(lambda x: TextBlob(x).sentiment.polarity)
    covid_df['subjectivity'] = covid_df['Text'].apply(lambda x: TextBlob(x).sentiment.subjectivity)

    return covid_df

# Graph comparing total number of tweets to number of covid tweets based on city
def city_comparison():    
    covid_df = df[df['Text'].str.contains('covid|vaccin', flags=re.IGNORECASE)]
    tweets_by_city = dft[['Text', 'City']].groupby(['City']).count()
    tweets_by_city.rename(columns={'Text': 'No. of tweets'}, inplace=True)
    covid_tweets_by_city = covid_df[['Text', 'City']].groupby(['City']).count()
    covid_tweets_by_city.rename(columns={'Text': 'No. covid tweets'}, inplace=True)
    final_df = tweets_by_city.merge(covid_tweets_by_city, left_index=True, right_index=True)
    final_df = final_df.reset_index()
    final_df = final_df.sort_values(by=["No. covid tweets"], ascending=False)
    final_df=final_df.head(12)

    return final_df