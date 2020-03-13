import json
import time

from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener

from config import CONSUMER_API_SECRET,CONSUMER_KEY,ACCESS_TOKEN,ACCESS_TOKEN_SECRET 
from data_cleanup import remove_urls_users_punctuations
from utils import getStreamingTrackFromTopic, getStoredModelFromTopic, createBarGraph

# OAuth process
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# listener that handles streaming data
class TwitterListener(StreamListener):

    def __init__(self, filename):
        """filename of the model"""
        self.sleep_time = 60 #in seconds 
        self.vectorizer, self.pca, self.model, self.n_cluster = getStoredModelFromTopic(filename)
        self.clusterToTweetsText = dict()
        self.clusterToNumberOfTweets = dict()
        self._initializeDictionary()
        self.count=0

    def _initializeDictionary(self):
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
        if(tweet["truncated"]):
            text = tweet["extended_tweet"]["full_text"]
        else:
            text = tweet["text"]
            
        cleaned_text = remove_urls_users_punctuations(text)
        print(cleaned_text)
        X = self.vectorizer.transform([cleaned_text]) 
        X = X.todense()
        X = self.pca.transform(X)
        predicted_cluster = int(self.model.predict(X))+1  
        print(predicted_cluster)
        self.clusterToNumberOfTweets[predicted_cluster]+=1
        self.clusterToTweetsText[predicted_cluster].append(cleaned_text)
        self.count+=1

        #EXIT STREAMING TO CREATE BAR GRAPH
        if self.count==30:
            self._prettyPrintClusterToTweets()
            createBarGraph(self.n_cluster,self.clusterToNumberOfTweets)
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
    filename = "5_cluster_kmeans_corona_2d.pkl"
    _track = getStreamingTrackFromTopic(topic)
    twitterStream = Stream(auth, TwitterListener(filename))
    twitterStream.filter(languages=["en"], track=_track)