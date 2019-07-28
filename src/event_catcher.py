from config import *
from tweepy import Stream, OAuthHandler, API,Cursor
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
        # f = csv.writer(open("../data/tweets.csv", "a"))
        csv_file = csv.writer(open('../data/tweets.csv', 'a'))
        for tweet in tweepy.Cursor(api.search, q="#unitedAIRLINES", count=100,
                                   lang="en",
                                   since="2017-04-03").items():
            print(tweet.created_at, tweet.text)
            csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])

    def on_error(self, status):
        print(status)


if __name__ == '__main__' :
    #twitterStream = Stream(auth, TwitterListener())
    #twitterStream.filter(track=["trump", "donald trump"])
    api = API(auth)
    csv_file = csv.writer(open('../data/tweets.csv', 'a'))
    for tweet in Cursor(api.search, q="#trump", count=100,lang="en").items():
        print(tweet.created_at, tweet.text)
        csv_file.writerow([tweet.created_at, tweet.text.encode('utf-8')])

