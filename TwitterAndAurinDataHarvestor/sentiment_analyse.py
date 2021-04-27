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
        nltk.download('stopwords')
        handle=open('tokenizer.pickle', 'rb')
        self.tokenizer1 = pickle.load(handle)
        self.stop_words_test = stopwords.words('english')
    def preprocess_test(self,text):
        text = re.sub("@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+", ' ', str(text).lower()).strip()
        cleaned_text = []
        tockens=np.zeros([2,2])
        for token in text.split():
            if token not in self.stop_words_test:
                cleaned_text.append(token)
        tokens=tf.keras.preprocessing.sequence.pad_sequences(self.tokenizer1.texts_to_sequences([" ".join(cleaned_text)],),maxlen = 30)
        return tokens
    def load_model(self):
        with tf.device('/cpu:0'):
            return tf.keras.models.load_model("model.h5")
    def sentiment_analysis(self,text):
        text=self.preprocess_test(text)
        model=self.load_model()
        with tf.device('/cpu:0'):
            output=model.predict(text)
        tf.keras.backend.clear_session()
        return output

