import csv
import json
import pickle
import time

from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener

from config import *
from data_cleanup import remove_urls_users_punctuations

# OAuth process
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# listener that handles streaming data
class TwitterListener(StreamListener):

    def __init__(self):
        self.vectorizer, self.model = pickle.load(open(STATE_VARIABLE_FILENAME, 'rb'))
        self.sleep_time = 60 #in seconds 
    
    def on_connect(self): 
        print('Stream starting...') 
    
    def on_data(self, data): 
        # print(data) 
        tweet = json.loads(data)

        if(tweet["truncated"]):
            text = tweet["extended_tweet"]["full_text"]
        else:
            text = tweet["text"]
        cleaned_text = remove_urls_users_punctuations(text)
        print(cleaned_text)
        X = self.vectorizer.transform([cleaned_text]) 
        predicted_cluster = self.model.predict(X)  
        # TODO: build some kind of graph ???
        print(predicted_cluster)

    def on_error(self, status_code):
        print(status_code)
        # switch(status_code):
        if(status_code==420):   # exponential backoff
            time.sleep(self.sleep_time)
            self.sleep_time= self.sleep_time * 2                  
        elif (status_code == 404):
            print("no resource here/ URL doesn't exist");
            return False; 
        elif (status_code == 406):
            print('atleast one of the params is invalid');
            return False; 
        elif (status_code == 413):
            print("parameter list is too long");
            return False; 
        else:
            print("Refer Best Practises guide at https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/connecting"); 
            return False; 
            

if __name__ == '__main__' :
    twitterStream = Stream(auth, TwitterListener())
    twitterStream.filter(track=["brexit"])