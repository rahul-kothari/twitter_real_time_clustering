import pickle
model = pickle.load(open('kmeans_classifier.pkl','rb'))
from step1_twitter_scrapper import get_tweets
from step2_unsupervised_learning import vectorizer
# PREDICT
# data = get_tweets(10)
# X_test = vectorizer.transform(data)
# predicted = model.predict(X_test)
# print(predicted)


data =["Look to see if you know any of the members and if they're Republican or Democrat. Arizona Superintendent of Public Instruction Kathy Hoffman today announced the members of the Arizona Department of Education’s School Safety Task Force. https://t.co/za4TLPJ3BW","Whiskey Riff New Music Friday Playlist (9/13/19) https://t.co/mJPEzhGzHd","This is sooooo v 80’s https://t.co/ScJJCmeMgG","Ken Burns takes a deep dive into 'Country Music' for his latest documentary https://t.co/RvrofqyTmo","Why the man Trump once called 'my African American' is leaving the GOP https://t.co/YVDISosdjl","Another thing about Reignited's Dynamic Music, is that if you stick around for a bit, the music will go all bassy. https://t.co/hWWUAxIsLX","Lana Del Rey - Blue Jeans (Official Music Video) https://t.co/eL2MDXOVe4 via @YouTube","Even the telegraph is starting to see sense. https://t.co/20NcKAcg2V","The backround music that plays during #kidvice reminds me of spongebob squrepants #Freshon947"]
from data_cleanup import remove_urls_users_punctuations
cleaned = [remove_urls_users_punctuations(tweet) for tweet in data]
X_test = vectorizer.transform(cleaned)
predicted = model.predict(X_test)
print(predicted)
