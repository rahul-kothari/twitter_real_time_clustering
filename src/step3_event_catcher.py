import json
import time

from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
import matplotlib.pyplot as plt

from config import * 
from data_cleanup import remove_urls_users_punctuations
from utils import createBarGraph, getFinalModelForStreaming

# OAuth process
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# listener that handles streaming data
class TwitterListener(StreamListener):

    def __init__(self, topic, numOfTweets):
        """topic of the model"""
        self.topic = topic
        self.topicName = Topic(topic).name
        self.model_name,self.vectorizer, self.pca, self.model, self.n_cluster = getFinalModelForStreaming(topic)
        self._initializeDictionary()
        self.sleep_time = 60 #in seconds 
        self.count=0
        self.NUM_OF_TWEETS_REQUIRED = numOfTweets

    def _initializeDictionary(self):
        """Create 2 dictionaries:
        clusterToTweetsText -> the tweets in each cluster (makes it easy for analysis)
        clusterToNumberOfTweets -> how many tweets classified in this cluster
        (to plot graph)
        """
        self.clusterToTweetsText = dict()
        self.clusterToNumberOfTweets = dict()
        
        for cluster in range(1, self.n_cluster+1):
            self.clusterToNumberOfTweets[cluster]=0
            self.clusterToTweetsText[cluster]=list()
    
    def _prettyPrintClusterToTweets(self):
        for cluster in self.clusterToTweetsText.keys():
            print(cluster, ' :')
            for tweet in self.clusterToTweetsText[cluster]:
                print('\t', tweet)
            print()

    def on_connect(self): 
        print('Stream starting...') 
    
    def on_data(self, data): 
        tweet = json.loads(data)
        #  handle extended tweets too.
        if(tweet["truncated"]):
            text = tweet["extended_tweet"]["full_text"]
        else:
            text = tweet["text"]
            
        #  clean text - removeu urls etc. tfidf vectorization, pca if necessary
        cleaned_text = remove_urls_users_punctuations(text)
        print(cleaned_text)
        X = self.vectorizer.transform([cleaned_text]) 
        if not self.pca == None:
            X = X.todense()
            X = self.pca.transform(X)
        predicted_cluster = int(self.model.predict(X))+1  
        print(predicted_cluster)
        self.clusterToNumberOfTweets[predicted_cluster]+=1
        self.clusterToTweetsText[predicted_cluster].append(cleaned_text)
        self.count+=1

        #EXIT STREAMING TO CREATE BAR GRAPH
        if self.count==self.NUM_OF_TWEETS_REQUIRED:
            self._prettyPrintClusterToTweets()
            createBarGraph(self.topic, self.model_name, self.n_cluster,self.clusterToNumberOfTweets)
            return False

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
    topic=int(input("Which topic (1 for brexit / 2 for corona)?: "))
    _track = STREAMING_TRACK[Topic(topic).name]
    numberOfTweets = int(input("How many tweets to stream?: "))
    twitterStream = Stream(auth, TwitterListener(topic, numberOfTweets))
    twitterStream.filter(languages=["en"], track=_track)