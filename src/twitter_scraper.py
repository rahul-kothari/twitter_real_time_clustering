from config import *
from tweepy import API, OAuthHandler, Cursor, TweepError

# OAuth process
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# ceate tweepy api object -
# tell it to wait how much ever needed in case we used rate limit
# and notify me too
api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# searching for tweets params:
search_criteria = TOPIC
lang = "en"
count = 0
data = list()
NUM_OF_TWEETS_NEEDED = 10

# searching for tweets.
for tweet in Cursor(api.search, q=search_criteria, lang=lang, tweet_mode='extended').items(NUM_OF_TWEETS_NEEDED):
    count += 1
    print(count, tweet.full_text)
    data.append(tweet.full_text)

delimiter = "\n\n-----------\n\n"
open('../data/tweets.txt', 'a', encoding="utf8")\
    .write(delimiter.join(data))
