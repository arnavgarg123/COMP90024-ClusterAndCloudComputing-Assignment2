import flask
from flask import request, url_for, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from dominate.tags import img

logo = img(src='./static/img/logo.png', height="50", width="50", style="margin-top:-15px")
#here we define our menu items
topbar = Navbar(logo,
                View('Home', 'my_maps'),
                View('Scenario 1', 'get_sc1'),
                View('Scenario 2', 'get_sc2'),
                View('Scenario 3', 'get_sc3')
                )

nav = Nav()
nav.register_element('left', topbar)

app = flask.Flask(__name__)
Bootstrap(app)

@app.route('/',methods=['GET','POST'])
def my_maps():

  mapbox_access_token = 'pk.eyJ1IjoiZ3Vya2kwOSIsImEiOiJja29iejNiZjkxaWg0MndtdTFiZzdkcXVnIn0.hTqur4keYNgXKLjldLaVEw'

  return render_template('index.html',
        mapbox_access_token=mapbox_access_token)

@app.route('/sc1', methods=['GET'])
def get_sc1():
    return(render_template('temp.html'))
    
@app.route('/sc2', methods=['GET'])
def get_sc2():
    return(render_template('temp.html'))
    
@app.route('/sc3', methods=['GET'])
def get_sc3():
    return(render_template('temp.html'))

nav.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)

