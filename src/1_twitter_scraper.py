from config import *
from tweepy import API, OAuthHandler, Cursor
import re

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
NUM_OF_TWEETS_NEEDED = 100
filename = '../data/tweets.txt'


def data_preprocessing(full_text):
    removed_mentions_urls = re.sub(r"(?:@|https?://|www)\S+|^(RT)\s+", "", full_text)
    removed_punctuations = re.findall(r'\w+', removed_mentions_urls)
    return removed_punctuations


# searching for tweets.
for tweet in Cursor(api.search, q=search_criteria, lang=lang, tweet_mode='extended').items(NUM_OF_TWEETS_NEEDED):
    count += 1
    print(count, tweet.full_text)
    """
    Cleaning Data
    1. Use regex to remove all user mentions, URLs, RT
    "(?:@|https?://|www)\S+|^(RT)\s+" -> 
    words starting with @ or prefixed with ":" OR https OR https:// OR www 
    NOT followed by any whitespaces (\S+)
    OR ^RT\s+ -> starts with RT followed by whitespaces.
    Replace them with "" -> use re.sub()
    
   2. Remove all punctuations i.e. only keep words with [a-1],[A-W],[0-9]
    Remove any other characters within the word.
    ==> re.findall(\w+)
    findall gives list. So join it.
    
    3. remove stop words later using sklearn TF-IDF Vector
    """
    processed_tweet = data_preprocessing(tweet.full_text)

    data.append(" ".join(processed_tweet))

delimiter = "\n"
open(filename, 'a', encoding="utf8")\
    .write(delimiter.join(data))
