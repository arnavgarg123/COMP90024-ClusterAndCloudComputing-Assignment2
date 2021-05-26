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

# Loading Data
df = pd.read_excel('./static/data_files/tweets_couchdb.xlsx',sheet_name='Sheet1')
aurin_unemployment_df = pd.read_excel(r'./static/data_files/UnemploymentRate_Cleaned.xlsx', sheet_name='UnemploymentRate')
edu_df=pd.read_excel(r'./static/data_files/data_australia_edu.xlsx')

# Graph showing sentiment vs unemployment of different cities
def unemployment_polarity():
    work_df = df[df['Text'].str.contains('work|job|unemploy|employ|sack|hire|school|educat', flags=re.IGNORECASE)]
    work_df['polarity'] = work_df['Text'].apply(lambda x: TextBlob(x).sentiment.polarity)
    work_tweets_by_city = work_df.groupby('City', as_index=False)['polarity'].mean()
    selected_cities = ['Melbourne', 'Sydney', 'Perth (WA)', 'Adelaide', 'Brisbane']
    final_work_tweets_df = work_tweets_by_city.loc[work_tweets_by_city['City'].isin(selected_cities)]

    final_aurin_unemployment_df = aurin_unemployment_df.loc[aurin_unemployment_df['sa4_name'].isin(selected_cities)]

    return final_work_tweets_df, final_aurin_unemployment_df

# Creating word cloud
def generate_wordcloud_work_education():
    work_education_df = df[df['Text'].str.contains('work|job|unemploy|employ|sack|hire|school|educat', flags=re.IGNORECASE)]

    stop_words = ["https", "will", "co", "amp", "n", "t", "nhttps"] + list(STOPWORDS)
    text = ' '.join(work_education_df['Text'])
    text = text.encode("ascii", "ignore").decode('utf-8')
    wordcloud_work_education = WordCloud(width=400, height=320, random_state=1,
                          background_color='black', colormap='Set1',
                          collocations=False, stopwords=stop_words).generate(text)

    return wordcloud_work_education

# Graph comparing subjectivity of tweets relating to unemployment on city level
def subjectivity_unemployment():
    unemp_df=pd.read_excel(r'./static/data_files/UnemploymentRate_Cleaned.xlsx')
    cities_df = df[df['City'].str.contains('Melbourne|Perth|Brisbane|Sydney|Adelaide', flags=re.IGNORECASE)]
    cities_df['subjectivity'] = cities_df['Text'].apply(lambda x: TextBlob(x).sentiment.subjectivity)
    subjectivity_city=cities_df[['City', 'subjectivity']].groupby(['City']).mean()
    city_sub = subjectivity_city.loc[["Melbourne","Adelaide","Brisbane","Sydney","Perth (WA)"]]
    city_sub=city_sub.reset_index()
    unemp_df["sa4_name"]=unemp_df["sa4_name"].apply(lambda x: x.strip())
    unemp_df=unemp_df.set_index('sa4_name')
    unemp_df1 = unemp_df.loc[["Melbourne","Adelaide","Brisbane","Sydney","Perth (WA)"]]
    unemp_df1=unemp_df1.reset_index()
    unemp_df2=unemp_df1[['sa4_name','unemp_rate']]
    unemp_df2.rename(columns={'sa4_name': 'City'}, inplace=True)
    mergeit_df=city_sub.merge(unemp_df2, on="City")

    return mergeit_df

# Graph showing education in comparission to unemployment
def education_unemployment():

    return edu_df
