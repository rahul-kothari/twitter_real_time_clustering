import json
import time

from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
import matplotlib.pyplot as plt
import numpy as np

from config import *
from data_cleanup import remove_urls_users_punctuations
from utils import getStoredModel

"""
UTILITY SCRIPT
COMPARE HOW SEVERAL DIFFERENT MODELS DO IN STREAMING
Within TwitterListener:
1. JUST ADD THE FILENAME in _getMOdels() -> files
2. And update the subplots in createAllGraphs
"""


class Model:    
    def __init__(self, filename):
        self.name = filename
        self.vectorizer, self.pca, self.model, self.n_cluster = getStoredModel(filename)
        self._initializeDictionary()

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
    
    def prettyPrintClusterToTweets(self):
        print(self.name)
        for cluster in self.clusterToTweetsText.keys():
            print(cluster, ' :')
            for tweet in self.clusterToTweetsText[cluster]:
                print('\t', tweet)
            print()

# listener that handles streaming data
class TwitterListener(StreamListener):

    def __init__(self):
        self.ai_algos = []
        self.count = 0
        self._getModels()

    def _getModels(self):
        """
        Store all the models we want to compare:
        """
        
        files = ["9_cluster_kmeans_corona_allD.pkl", "5_cluster_gmm_corona_2d.pkl"]

        for i in range(len(files)):
            if i==0:
                self.ai_algos.append(Model(files[0], False))
            else:
                self.ai_algos.append(Model(files[i], True))
    
    def on_connect(self): 
        print('Stream starting...') 
    
    def on_data(self, data): 
        tweet = json.loads(data)
        if tweet["truncated"]:
            text = tweet["extended_tweet"]["full_text"]
        else:
            text = tweet["text"]            
        cleaned_text = remove_urls_users_punctuations(text)
        print(cleaned_text)

        for AI in self.ai_algos:
            X = AI.vectorizer.transform([cleaned_text]) 
            if AI.isDimensionalityReduced:
                X = X.todense()
                X = AI.pca.transform(X)
            predicted_cluster = int(AI.model.predict(X))+1  
            AI.clusterToNumberOfTweets[predicted_cluster]+=1
            AI.clusterToTweetsText[predicted_cluster].append(cleaned_text)
        self.count+=1

        #EXIT STREAMING TO CREATE BAR GRAPH
        if self.count==50:
            self.createAllGraphs()
            return False

    def on_error(self, status_code):
        print(status_code)
        return False

    def createAllGraphs(self):
        """
        PLOT SUBPLOTS COMPARING EACH MODEL
        CHANGE ax.fig_add_subplot accordingly
        """
        fig = plt.figure()
        fig.subplots_adjust(hspace=0.8, wspace = 0.5)
        fig.suptitle("CORONA REAL TIME CLASSIFICATION - Comparing models:", fontsize=16)
        my_colors = ['brown','pink', 'red', 'limegreen', 'blue', 'cyan',
            'orange', 'dodgerblue','purple', 'turquoise', 'darkorchid', 'gold']

        for i in range(len(self.ai_algos)):
            AI = self.ai_algos[i]
            AI.prettyPrintClusterToTweets()
            ax = fig.add_subplot(1,2,(i+1))
            x = []
            y = []
            for j in range(1, AI.n_cluster+1):
                y.append(AI.clusterToNumberOfTweets[j])
                x.append(j)

            bars = ax.bar(x, y, align='center', color = my_colors, edgecolor='k', linewidth=2)
            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x(), yval + 1., str(int(yval)))

            ax.set_xticks(x)
            ax.set_yticks(np.array(range(0,50,5)))
            plt.title('#tweets per cluster: %s' % AI.name)   
        plt.show()
            

if __name__ == '__main__' :
    # _track = ["coronavirus nhs", "coronavirus economy", "coronavirus wuhan", "coronavirus usa", "coronavirus trump"]
    topic=Topic(int(input("Which topic (1 for brexit / 2 for corona)?: ")))
    _track = STREAMING_TRACK[topic.name]    # OAuth process
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    twitterStream = Stream(auth, TwitterListener())
    twitterStream.filter(languages=["en"], track=_track)