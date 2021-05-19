import plotly
from flask import Flask, render_template, send_file, request, url_for, redirect
from matplotlib import pyplot as plt
from io import BytesIO
import plotly.express as px
import json
import plotly.graph_objects as go
from graphs_data import generate_word_cloud, generate_scores, city_comparison, generate_word_cloud_hashtags, \
    generate_pie_chart


app = Flask(__name__)             # create an app instance

@app.route('/',methods=['GET','POST'])
def my_maps():
  mapbox_access_token = 'pk.eyJ1IjoiZ3Vya2kwOSIsImEiOiJja29iejNiZjkxaWg0MndtdTFiZzdkcXVnIn0.hTqur4keYNgXKLjldLaVEw'
  return render_template('index.html',mapbox_access_token=mapbox_access_token)

@app.route('/sc1', methods=['GET'])
def get_sc1():
    return(render_template('temp.html'))

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

    polarity_histogram = px.histogram(data, x="polarity")
    graphJSON = json.dumps(polarity_histogram, cls=plotly.utils.PlotlyJSONEncoder)

    heatMap = px.density_heatmap(data, x="polarity", y="subjectivity")
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
                      title_text='Total Tweets vs Covid-related Tweets')
    comboJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('scenario2.html', graphJSON = graphJSON, heatMapJSON = heatMapJSON, comboJSON = comboJSON)
    
@app.route('/wordcloud_hashtags')
def wordcloud_hashtags():
    wordcloud_hashtags = generate_word_cloud_hashtags()
    fig = plt.figure(figsize=(40, 30))
    plt.imshow(wordcloud_hashtags)
    plt.axis("off")
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')

@app.route('/scenario1')
def scenario1():
    values = generate_pie_chart()
    names = ['Labor Party', 'Liberal Party']
    colors = ['#F21DA7', '#0FB335']
    pie_chart = px.pie(values=values, names=names, title='Sentiment Score of Labor vs Liberal Party', color=names,
                 color_discrete_map={names[0]: colors[0], names[1]: colors[1]})
    pieJSON = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('scenario1.html', pieJSON = pieJSON)
    

if __name__ == '__main__':
    app.run(debug=True)


