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


def get_tweets(num_of_tweets=NUM_OF_TWEETS_NEEDED, search_criteria=TOPIC2, lang="en", filename=FILE_PATH3):
	"""
	Get tweets using tweepy api.
	:param num_of_tweets: (int) to be fetched from api
	:param search_criteria: topic, hashtags, keywords etc.
	:param lang: language of tweets to fetch ("en" for english)
	:return: list of cleaned tweets
	"""
	api = create_twitter_object()
	count = 0
	all_tweets = list()
	tweets=[]
	for tweet in Cursor(api.search, q=search_criteria, lang=lang, tweet_mode='extended').items(num_of_tweets):
		try: 			
			count += 1
			print(count, tweet.full_text)
			processed_tweet = remove_urls_users_punctuations(tweet.full_text)
			tweets.append(processed_tweet)
			if(count%250==0):
				# write to file every 250 tweets. 
				open(filename, 'a', encoding="utf8").write("\n".join(tweets))
				all_tweets.extend(tweets)
				tweets = []
		except: #on encountering error, just move on.
			continue
	# if there is left some tweets left:
	open(filename, 'a', encoding="utf8").write("\n".join(tweets))


if __name__ == '__main__' :
	# get tweets and put it in a file
	print("Writing tweets to"+ FILE_PATH3)
	print("Which topic to get tweets about?")
	print("1. Brexit (TOPIC2 in config.py)")
	print("2. Corona (TOPIC_CORONA in config.py)")
	topic=Topic(int(input("Which topic (1/2)?: ")))
	# raises ValueError automatically.
	if(topic==Topic.BREXIT):
		get_tweets(search_criteria=TOPIC2)
	elif(topic==Topic.CORONA):
		get_tweets(search_criteria=TOPIC_CORONA)
