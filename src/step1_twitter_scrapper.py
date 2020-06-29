from tweepy import API, Cursor, AppAuthHandler

from config import *
from data_cleanup import remove_urls_users_punctuations, lemmatize


def create_twitter_object():
	# OAuth process
	auth = AppAuthHandler(CONSUMER_KEY, CONSUMER_API_SECRET)
	#auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	# ceate tweepy api object -
	# tell it to wait how much ever needed in case we reached rate limit and notify me too
	api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
	return api


def get_tweets(search_criteria, filename, lang="en"):
	"""
	Get upto 5000 tweets using tweepy api, remove URLS, user mentions, numbers and store in file.
	Args:
		search_criteria: topic, hashtags, keywords etc.
		filename - string where tweets are stored
		lang: language of tweets to fetch ("en" for english)
	"""
	api = create_twitter_object()
	count = 0
	all_tweets = list()
	tweets=[]
	for tweet in Cursor(api.search, q=search_criteria, lang=lang, tweet_mode='extended').items(5000):
		try: 			
			count += 1
			print(count, tweet.full_text)
			lemmatized_tweet = lemmatize(tweet.full_text)
			processed_tweet = remove_urls_users_punctuations(lemmatized_tweet)
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
	print("Which topic to get tweets about?")
	print("1. Brexit (refer MINING_TOPIC[BREXIT] in config.py)")
	print("2. Corona (MINIG_TOPIC[CORONA] in config.py)")
	print("Tweets are put in "+ DATA_FILE["TRIAL"])
	topic=Topic(int(input("Which topic (1/2)?: ")))
	topicName = topic.name
	# raises ValueError automatically.
	get_tweets(search_criteria=MINING_TOPIC[topic.name], filename = DATA_FILE["TRIAL"])
	