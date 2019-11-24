from config import *
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
import csv
import json
import pickle
from data_cleanup import *

# OAuth process
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


# listener that handles streaming data
class TwitterListener(StreamListener):

    self.loaded_model = pickle.load(open(AI_MODEL_FILENAME, 'rb'))
    self.vectorizer


    def on_connect(self):
        print('Stream starting...')

    def on_data(self, data):
        print(data)
        X = vectorizer.transform([remove_urls_users_punctuations(data.full_text)])
        predicted_cluster = self.loaded_model.predict(X)  
        #TODO: build some kind of graph ???
              
    def on_error(self, status):
        print(status)
        #TODO: implement exponential backoff


if __name__ == '__main__' :
    twitterStream = Stream(auth, TwitterListener())
    twitterStream.filter(track=["trump", "donald trump"])