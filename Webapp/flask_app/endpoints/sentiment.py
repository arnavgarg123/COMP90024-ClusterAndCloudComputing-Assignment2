from flask import Blueprint

s="sentiment"

overall_sentiment=Blueprint('overall_sentiment',__name__)
@overall_sentiment.route('/senti')
def senti():
    return s