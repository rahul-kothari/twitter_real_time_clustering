from config import *
from tweepy import API, OAuthHandler, Cursor
import csv
import json

# OAuth process
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = API(auth)

# Create CSV file
csv_file = open('../data/tweets.csv', 'w', encoding="utf8")
csv_writer = csv.writer(csv_file)

# searching for tweets:
search_criteria = TOPIC + " -filer:retweets from:RahulKo96245846"
#search_criteria = "from:RahulKo96245846"
count = 0
for tweet in Cursor(api.search, q=search_criteria, lang="en", tweet_mode='extended').items():
    count += 1
    print(count, tweet.full_text)
    csv_writer.writerow([tweet.full_text])

csv_file.close()

