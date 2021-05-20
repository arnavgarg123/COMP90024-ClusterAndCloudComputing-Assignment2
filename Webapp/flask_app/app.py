import plotly
from flask import Flask, render_template, send_file, request, url_for, redirect
from matplotlib import pyplot as plt
from io import BytesIO
import plotly.express as px
import json
import plotly.graph_objects as go
from graphs_data import generate_word_cloud, generate_scores, city_comparison, city_tweets, income_sentiment, generate_pie_chart, generate_word_cloud_hashtags
from plotly.subplots import make_subplots


app = Flask(__name__)             # create an app instance

@app.route('/',methods=['GET','POST'])
def my_maps():
  mapbox_access_token = 'pk.eyJ1IjoiZ3Vya2kwOSIsImEiOiJja29iejNiZjkxaWg0MndtdTFiZzdkcXVnIn0.hTqur4keYNgXKLjldLaVEw'
  return render_template('index.html')

@app.route('/wordcloud')
def wordcloud():
    wordcloud = generate_word_cloud()
    fig = plt.figure(figsize=(40, 30))
    plt.imshow(wordcloud)
    # No axis details
    plt.axis("off")
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')

@app.route('/sc2')
def polarityscore():
    data = generate_scores()

    polarity_histogram = px.histogram(data, x="polarity", template='seaborn',  color_discrete_sequence=['indianred'])
    graphJSON = json.dumps(polarity_histogram, cls=plotly.utils.PlotlyJSONEncoder)
    heatMap = px.density_heatmap(data, x="polarity", y="subjectivity", template='seaborn')
    heatMapJSON = json.dumps(heatMap, cls=plotly.utils.PlotlyJSONEncoder)

    final_df = city_comparison()
    fig = go.Figure()
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
    fig.update_layout(legend_title_text='Legend',
                      title_text='Total Tweets vs Covid-related Tweets', template='plotly_dark')
    comboJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('scenario2.html', graphJSON = graphJSON, heatMapJSON = heatMapJSON, comboJSON = comboJSON)
    
@app.route('/wordcloud_hashtags')
def wordcloud_hashtags():
    wordcloud_hashtags = generate_word_cloud_hashtags()
    fig = plt.figure(figsize=(35, 25))
    plt.imshow(wordcloud_hashtags)
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
            name="Population",marker=dict(color="crimson")
            
        ) ,row=1, col=1, secondary_y=False)
    fig.add_trace(
        go.Scatter(
            x=top_df['City'],
            y=top_df['No. of tweets'],
            name="Total Tweets",
        ) ,row=1, col=1, secondary_y=True)
    fig.update_traces(texttemplate='%{text:.2s}')
    fig.update_layout(legend_title_text='Legend',
                    template='plotly_dark')
    
    subJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    fig.add_trace(
        go.Bar(
            x=merge1_df['City'],
            y=merge1_df['Avg. Income AUD'],
            name="Avg. Income",
            
        ) ,row=1, col=2, secondary_y=False)
    fig.add_trace(
        go.Scatter(
            x=merge1_df['City'],
            y=merge1_df['Sentiment'],
            name="Sentiment",
        ) ,row=1, col=2, secondary_y=True)
    #fig.update_traces(hoverinfo='label+percent+name')
    fig.update_layout(legend_title_text='Legend',
                      template='plotly_dark',
                      #margin=dict(r=10, t=25, b=10, l=130),
                      
    )
    fig.update_yaxes(title_text="<b>Population</b>", secondary_y=False, autorange=True, row=1, col=1)
    fig.update_yaxes(title_text="<b>Tweets</b>", secondary_y=True, autorange=True, row=1, col=1)
    fig.update_yaxes(title_text="<b>Avg. Income</b>", secondary_y=False, autorange=True, row=1, col=2)
    fig.update_yaxes(title_text="<b>Sentiment</b>", secondary_y=True, autorange=True, row=1, col=2)
    subJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #labels=['Labor Party', 'Liberal Party']
    #fig.add_trace(
        #go.Pie(labels=labels, values=values, name="liberal vs labour party"),
              #)
    names = ['Labor Party', 'Liberal Party']
    color= ['cyan', 'crimson']
    pie_chart = px.pie(values=values, names=names, title='Sentiment Score of Labor vs Liberal Party', color=names,
                 color_discrete_map={names[0]: color[0], names[1]: color[1]},template='plotly_dark')
    pieJSON = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('scenario1.html', subJSON = subJSON, pieJSON=pieJSON)
    

if __name__ == '__main__':
    app.run(debug=True)


