from config import *
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
import csv
import json
# OAuth process
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


# listener that handles streaming data
class TwitterListener(StreamListener):
    def on_connect(self):
        print('Stream starting...')

    def on_data(self, data):
        print(data)
        
    def on_error(self, status):
        print(status)


if __name__ == '__main__' :

    twitterStream = Stream(auth, TwitterListener())
    twitterStream.filter(track=["trump", "donald trump"])