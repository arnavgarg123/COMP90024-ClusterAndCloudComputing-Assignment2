import pandas as pd
import re
from textblob import TextBlob
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS

df = pd.read_excel('./static/data_files/tweets_couchdb.xlsx',sheet_name='Sheet1')
income_df = pd.read_excel(r'./static/data_files/income.xlsx')
df_city=pd.read_csv(r"./static/data_files/aurin_city_stats.csv")



def generate_word_cloud():
    covid_df = df[df['Text'].str.contains('covid|vaccin', flags=re.IGNORECASE)]
    stop_words = ["https", "will", "co", "amp", "n", "t"] + list(STOPWORDS)
    text = ' '.join(covid_df['Text'])
    text = text.encode("ascii", "ignore").decode('utf-8')
    wordcloud = WordCloud(width=3000, height=2000, random_state=1,
                          background_color='white', colormap='Set1',
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
    wordcloud_hashtags = WordCloud(width=3000, height=2500, random_state=2,
                                   background_color='black', colormap='Set2',
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
