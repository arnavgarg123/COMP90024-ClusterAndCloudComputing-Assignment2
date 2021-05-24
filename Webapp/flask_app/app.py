import plotly
from flask import Flask, render_template, send_file, request, url_for, redirect
from matplotlib import pyplot as plt
from io import BytesIO
import plotly.express as px
import json
import plotly.graph_objects as go
from graphs_data import generate_word_cloud, generate_scores, city_comparison, city_tweets, income_sentiment, generate_pie_chart, generate_word_cloud_hashtags,subjectivity_unemployment,education_unemployment,unemployment_polarity,generate_wordcloud_work_education
from plotly.subplots import make_subplots
#from fetch_couchdb_data import save_data,refresh_map_pt


app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index_pg():
  return render_template('index.html')

#@app.route('/refresh',methods=['GET','POST'])
#def refresh_db():
#  save_data()
#  refresh_map_pt()
#  return render_template('index.html')

@app.route('/wordcloud')
def wordcloud():
    wordcloud = generate_word_cloud()
    fig = plt.figure(figsize=(5, 4))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')

@app.route('/sc2')
def polarityscore():
    data = generate_scores()

    polarity_histogram = px.histogram(data, x="polarity", template='plotly_dark' , color_discrete_sequence=['indianred'])
    graphJSON = json.dumps(polarity_histogram, cls=plotly.utils.PlotlyJSONEncoder)
    heatMap = px.density_heatmap(data, x="polarity", y="subjectivity", template='plotly_dark')
    heatMapJSON = json.dumps(heatMap, cls=plotly.utils.PlotlyJSONEncoder)

    final_df = city_comparison()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=final_df['City'],
            y=final_df['No. covid tweets'],
            name="Covid-related Tweets"
        ))
    fig.add_trace(
        go.Bar(
            x=final_df['City'],
            y=final_df['No. of tweets'],
            name="Total Tweets"
        ))

    fig.update_traces(texttemplate='%{text:.2s}')
    fig.update_layout(legend_title_text='Legend', template='plotly_dark')
    fig.update_yaxes(title_text="tweets", autorange=True)
    comboJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('scenario2.html', graphJSON = graphJSON, heatMapJSON = heatMapJSON, comboJSON = comboJSON)
    
@app.route('/wordcloud_hashtags')
def wordcloud_hashtags():
    wordcloud_hashtags = generate_word_cloud_hashtags()
    fig = plt.figure(figsize=(5, 4))
    plt.imshow(wordcloud_hashtags)
    plt.axis("off")
    plt.tight_layout(pad=0)
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')

@app.route('/sc3')
def scenario3():
    final_work_tweets_df, final_aurin_unemployment_df = unemployment_polarity()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(x=final_work_tweets_df['City'],
               y=final_work_tweets_df['polarity'],
               name="Polarity Score", marker=dict(color="#bf00ff")),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=final_aurin_unemployment_df['sa4_name'],
                   y=final_aurin_unemployment_df['unemp_rate'],
                   name="Unemployment Rate", marker=dict(color="white")),
        secondary_y=True,
    )

    fig.update_traces(texttemplate='%{text:.2s}')
    fig.update_layout(legend_title_text='Legend', template='plotly_dark')

    fig.update_yaxes(title_text="<b>Unemployment Rate</b>", secondary_y=True)
    fig.update_yaxes(title_text="<b>Polarity</b>", secondary_y=False)

    comboJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    mergeit_df=subjectivity_unemployment()
    edu_df=education_unemployment()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=mergeit_df['City'],
            y=mergeit_df['subjectivity'],
            name="Subjectivity"
        ) ,secondary_y=False)
    fig.add_trace(
        go.Scatter(
            x=mergeit_df['City'],
            y=mergeit_df['unemp_rate'],
            name="Unemployment Rate"
        ) , secondary_y=True)

    fig.update_traces(texttemplate='%{text:.2s}')
    fig.update_layout(legend_title_text='Legend', template='plotly_dark')
    fig.update_yaxes(title_text="<b>Subjectivity</b>", secondary_y=False, autorange=True)
    fig.update_yaxes(title_text="<b>Unemployment Rate</b>", secondary_y=True, autorange=True)
    subJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=edu_df['Level of education'],
            y=edu_df['Unemployed'],
            name="<b>Unemployment Percentage<b>"
        ))

    fig.update_traces(texttemplate='%{text:.2s}')
    fig.update_layout(legend_title_text='Legend', template='plotly_dark')
    fig.update_yaxes(title_text="<b>Unemployment Percent</b>", autorange=True)
    hubJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('scenario3.html', subJSON=subJSON, hubJSON=hubJSON, comboJSON = comboJSON)

@app.route('/wordcloud_work_education')
def wordcloud_work_education():
    wordcloud = generate_wordcloud_work_education()
    fig = plt.figure(figsize=(5,4))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')

@app.route('/sc1')
def population_tweets():
    top_df=city_tweets()
    merge1_df=income_sentiment()
    values=generate_pie_chart()
    fig = make_subplots(
    rows=1, cols=2,
    specs=[[{"type": "xy", "secondary_y": True}, {"type": "xy", "secondary_y": True}]]
    ,subplot_titles=("Total Tweets Vs Population", "Sentiment Vs Avg. Income")
)
    fig.add_trace(
        go.Bar(
            x=top_df['City'],
            y=top_df['Number of people'],
            name="Population"
        ) ,row=1, col=1, secondary_y=False)
    fig.add_trace(
        go.Scatter(
            x=top_df['City'],
            y=top_df['No. of tweets'],
            name="Total Tweets"
        ) ,row=1, col=1, secondary_y=True)
    fig.update_traces(texttemplate='%{text:.2s}')
    subJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    fig.add_trace(
        go.Bar(
            x=merge1_df['City'],
            y=merge1_df['Avg. Income AUD'],
            name="Avg. Income"
        ) ,row=1, col=2, secondary_y=False)
    fig.add_trace(
        go.Scatter(
            x=merge1_df['City'],
            y=merge1_df['Sentiment'],
            name="Sentiment"
        ) ,row=1, col=2, secondary_y=True)
    fig.update_layout(
                      template='plotly_dark'             
    )
    fig.update_yaxes(title_text="<b>Population</b>", secondary_y=False, autorange=True, row=1, col=1)
    fig.update_yaxes(title_text="<b>Tweets</b>", secondary_y=True, autorange=True, row=1, col=1)
    fig.update_yaxes(title_text="<b>Avg. Income</b>", secondary_y=False, autorange=True, row=1, col=2)
    fig.update_yaxes(title_text="<b>Sentiment</b>", secondary_y=True, autorange=True, row=1, col=2)
    fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.42
))
    subJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    names = ['Labor Party', 'Liberal Party']
    color= ['cyan', 'crimson']
    pie_chart = px.pie(values=values, names=names, color=names,
                 color_discrete_map={names[0]: color[0], names[1]: color[1]},template='plotly_dark')
    pieJSON = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('scenario1.html', subJSON = subJSON, pieJSON=pieJSON)
    

if __name__ == '__main__':
    app.run(debug=True)


