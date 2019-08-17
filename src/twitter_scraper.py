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
NUM_OF_TWEETS_NEEDED = 10

# searching for tweets.
for tweet in Cursor(api.search, q=search_criteria, lang=lang, tweet_mode='extended').items(NUM_OF_TWEETS_NEEDED):
    count += 1
    print(count, tweet.full_text)
    # CLEAN THE DATA ->
    """
    1. Use regex to remove all user mentions, URLs.
    "?:@|https?://|www)\S+" -> 
    words starting with @ or prefixed with ":" OR https OR https:// OR www 
    followed with 1 or more whitespaces (\S+)
    Replace them with "" -> use re.sub()
    
   2. Remove all punctuations i.e. only keep words with [a-1],[A-W],[0-9]
    Remove any other characters within the word.
    ==> re.findall(\w+)
    findall gives list
    
    3. Now filter all stopwords from this list.
    """
    removed_mentions_urls = re.sub(r"(?:@|https?://|www)\S+", "", tweet.full_text)
    removed_punctuations = re.findall(r'\w+', removed_mentions_urls)
    # [word for word in removed_punctuations if word not in STOPWORDS]
    removed_stopwords = list()
    for word in removed_punctuations:
        if word.lower() not in STOPWORDS:
            removed_stopwords.append(word)
    print(removed_stopwords)

    data.append(str(removed_stopwords))

delimiter = "\n\n-----------\n\n"
open('../data/tweets.txt', 'a', encoding="utf8")\
    .write(delimiter.join(data))
