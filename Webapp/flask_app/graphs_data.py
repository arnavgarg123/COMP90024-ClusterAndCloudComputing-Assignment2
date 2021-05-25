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

df = pd.read_excel('./static/data_files/tweets_couchdb.xlsx',sheet_name='Sheet1')
income_df = pd.read_excel(r'./static/data_files/income.xlsx')
df_city=pd.read_csv(r"./static/data_files/aurin_city_stats.csv")
aurin_unemployment_df = pd.read_excel(r'./static/data_files/UnemploymentRate_Cleaned.xlsx', sheet_name='UnemploymentRate')
edu_df=pd.read_excel(r'./static/data_files/data_australia_edu.xlsx')



def generate_word_cloud():
    covid_df = df[df['Text'].str.contains('covid|vaccin', flags=re.IGNORECASE)]
    stop_words = ["https", "will", "co", "amp", "n", "t"] + list(STOPWORDS)
    text = ' '.join(covid_df['Text'])
    text = text.encode("ascii", "ignore").decode('utf-8')
    wordcloud = WordCloud(width=400, height=320, random_state=1,
                          background_color='black', colormap='Set1',
                          collocations=False, stopwords=stop_words).generate(text)
    return wordcloud

def generate_scores():
    covid_df = df[df['Text'].str.contains('covid|vaccin', flags=re.IGNORECASE)]
    covid_df['polarity'] = covid_df['Text'].apply(lambda x: TextBlob(x).sentiment.polarity)
    covid_df['subjectivity'] = covid_df['Text'].apply(lambda x: TextBlob(x).sentiment.subjectivity)

    return covid_df

def city_comparison():    
    covid_df = df[df['Text'].str.contains('covid|vaccin', flags=re.IGNORECASE)]
    tweets_by_city = df[['Text', 'City']].groupby(['City']).count()
    tweets_by_city.rename(columns={'Text': 'No. of tweets'}, inplace=True)
    covid_tweets_by_city = covid_df[['Text', 'City']].groupby(['City']).count()
    covid_tweets_by_city.rename(columns={'Text': 'No. covid tweets'}, inplace=True)
    final_df = tweets_by_city.merge(covid_tweets_by_city, left_index=True, right_index=True)
    final_df = final_df.reset_index()
    final_df = final_df.sort_values(by=["No. covid tweets"], ascending=False)
    final_df=final_df.head(12)

    return final_df
    
def city_tweets():
    tweets_by_city = df[['Text', 'City']].groupby(['City']).count()
    tweets_by_city.rename(columns={'Text': 'No. of tweets'}, inplace=True)
    population_df=df_city[['estmtd_rsdnt_ppltn_smmry_sttstcs_30_jne_prsns_ttl_nm']]
    city_df=df_city[[' lga_name_2019']]
    population_df.rename(columns={'estmtd_rsdnt_ppltn_smmry_sttstcs_30_jne_prsns_ttl_nm': 'Number of people'}, inplace=True)
    city_df.rename(columns={' lga_name_2019': 'City'}, inplace=True)
    new_df =city_df.merge(population_df, left_index=True, right_index=True)
    new_df["City"]=new_df["City"].apply(lambda x: x.strip())
    merge_df=new_df.merge(tweets_by_city.reset_index(), on="City")
    sorted_df = merge_df.sort_values(by=["No. of tweets"], ascending=False)
    top_df=sorted_df.head(13)
    
    return top_df
def income_sentiment():
    sentiment_city=df[['City', 'Sentiment']].groupby(['City']).mean()
    sentiment_city=sentiment_city.reset_index()
    sentiment_city["City"]=sentiment_city["City"].apply(lambda x: x.strip())
    merge1_df=income_df.merge(sentiment_city, on="City")
    return merge1_df

def generate_word_cloud_hashtags():
    text = ' '.join(df['Text'])
    pattern = "\B@\w+"
    result = re.findall(pattern, text)
    result = [hashtag[1:] for hashtag in result]
    result = ' '.join(result)
    wordcloud_hashtags = WordCloud(width=400, height=320, random_state=1,
                                   background_color='black', colormap='Set1',
                                   collocations=False).generate(result)
    return wordcloud_hashtags

def generate_pie_chart():
    labor_party_keywords = "labour party|australian labor party|australian labor|australianlabor|australianlaborparty|Anthony Albanese|Bill Shorten|labourparty"
    liberal_party_keywords = "liberal party|scott morrison|liberal|scottmorrison|liberal party"

    labor_party_df = df[df['Text'].str.contains(labor_party_keywords, flags=re.IGNORECASE)]
    liberal_party_df = df[df['Text'].str.contains(liberal_party_keywords, flags=re.IGNORECASE)]

    labor_party_avg_sentiment = labor_party_df['Sentiment'].mean()
    liberal_party_avg_sentiment = liberal_party_df['Sentiment'].mean()

    labor_party_avg_sentiment_normalised = labor_party_avg_sentiment / (labor_party_avg_sentiment + liberal_party_avg_sentiment)
    liberal_party_avg_sentiment_normalised = liberal_party_avg_sentiment / (labor_party_avg_sentiment + liberal_party_avg_sentiment)

    values = [labor_party_avg_sentiment_normalised, liberal_party_avg_sentiment_normalised]

    return values

def unemployment_polarity():
    work_df = df[df['Text'].str.contains('work|job|unemploy|employ|sack|hire', flags=re.IGNORECASE)]
    work_df['polarity'] = work_df['Text'].apply(lambda x: TextBlob(x).sentiment.polarity)
    work_tweets_by_city = work_df.groupby('City', as_index=False)['polarity'].mean()
    selected_cities = ['Melbourne', 'Sydney', 'Perth (WA)', 'Adelaide', 'Brisbane']
    final_work_tweets_df = work_tweets_by_city.loc[work_tweets_by_city['City'].isin(selected_cities)]

    final_aurin_unemployment_df = aurin_unemployment_df.loc[aurin_unemployment_df['sa4_name'].isin(selected_cities)]

    return final_work_tweets_df, final_aurin_unemployment_df

def generate_wordcloud_work_education():
    work_education_df = df[df['Text'].str.contains('work|job|unemploy|employ|sack|hire|school|educat', flags=re.IGNORECASE)]

    stop_words = ["https", "will", "co", "amp", "n", "t", "nhttps"] + list(STOPWORDS)
    text = ' '.join(work_education_df['Text'])
    text = text.encode("ascii", "ignore").decode('utf-8')
    wordcloud_work_education = WordCloud(width=400, height=320, random_state=1,
                          background_color='black', colormap='Set1',
                          collocations=False, stopwords=stop_words).generate(text)

    return wordcloud_work_education
    
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


def education_unemployment():

    return edu_df
