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
import tensorflow as tf
import nltk
from nltk.corpus import stopwords
import re
import pickle
from tensorflow.keras.layers import Conv1D, Bidirectional, LSTM, Dense, Input, Dropout
from tensorflow.keras.layers import SpatialDropout1D, Embedding, SpatialDropout1D
import numpy as np
import logging
tf.get_logger().setLevel(logging.ERROR)
class sentiment:
    def __init__(self):
        # Downloading stop words
        nltk.download('stopwords')
        # Loading tockenizer
        handle=open('tokenizer.pickle', 'rb')
        self.tokenizer1 = pickle.load(handle)
        self.stop_words_test = stopwords.words('english')

    # Cleaning text for analysis model
    def preprocess_test(self,text):
        # Removing symbols from text
        text = re.sub("@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+", ' ', str(text).lower()).strip()
        cleaned_text = []
        tockens=np.zeros([2,2])
        # Removing stop words
        for token in text.split():
            if token not in self.stop_words_test:
                cleaned_text.append(token)
        # Padding and tockenizing
        tokens=tf.keras.preprocessing.sequence.pad_sequences(self.tokenizer1.texts_to_sequences([" ".join(cleaned_text)],),maxlen = 30)
        return tokens

    # Load created model
    def load_model(self):
        with tf.device('/cpu:0'):
            return tf.keras.models.load_model("model.h5")

    # Sentiment Analysis and putting everything together
    def sentiment_analysis(self,text):
        text=self.preprocess_test(text)
        model=self.load_model()
        # Using cpu for processing
        with tf.device('/cpu:0'):
            output=model.predict(text)
        # Clearing memory
        tf.keras.backend.clear_session()
        return output
