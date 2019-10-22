from config import *
from tweepy import API, Cursor, AppAuthHandler
from data_cleanup import remove_urls_users_punctuations


def create_twitter_object():
    # OAuth process
    auth = AppAuthHandler(CONSUMER_KEY, CONSUMER_API_SECRET)
    #auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    # ceate tweepy api object -
    # tell it to wait how much ever needed in case we reached rate limit and notify me too
    api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api


def get_tweets(num_of_tweets, search_criteria=TOPIC, lang="en"):
    """
    Get tweets using tweepy api.
    :param num_of_tweets: (int) to be fetched from api
    :param search_criteria: topic, hashtags, keywords etc.
    :param lang: language of tweets to fetch ("en" for english)
    :return: list of cleaned tweets
    """
    api = create_twitter_object()
    count = 0
    tweets = list()
    for tweet in Cursor(api.search, q=search_criteria, lang=lang, tweet_mode='extended').items(num_of_tweets):
        count += 1
        print(count, tweet.full_text)
        processed_tweet = remove_urls_users_punctuations(tweet.full_text)
        tweets.append(processed_tweet)
    return tweets


if __name__ == '__main__' :
    # get tweets and put it in a file
    data = get_tweets(NUM_OF_TWEETS_NEEDED)
    filename = FILE_PATH
    delimiter = "\n"
    open(filename, 'a', encoding="utf8").write(delimiter.join(data))
