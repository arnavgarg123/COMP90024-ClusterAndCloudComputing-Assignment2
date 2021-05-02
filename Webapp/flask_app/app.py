from flask import Flask
from endpoints.sentiment import overall_sentiment
app=Flask(__name__,template_folder='templates')
app.register_blueprint(overall_sentiment)
@app.route("/")
def home():
    return "hello"


if __name__=='__main__':
    app.run(host='0.0.0.0')