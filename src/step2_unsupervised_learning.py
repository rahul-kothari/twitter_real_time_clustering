from config import FILE_PATH
from data_cleanup import remove_stopwords_and_tfidf
from sklearn.cluster import KMeans

# 1. Read data from tweets.txt
filename = FILE_PATH
tweets = [line.rstrip('\n').lower() for line in open(filename)]
# doing file.readLines appends '\n' always.

# 2. remove stopwords, do tfidf
X, vectorizer = remove_stopwords_and_tfidf(tweets)

# 3. use elbow method to find number of clusters
# TODO

# 4. Do KMeans
n_cluster = 5
model = KMeans(n_clusters=n_cluster, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

# 5. Relevant output
# TODO
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
# prints keywords in each cluster
for i in range(n_cluster):
    print("\nCluster %d:" % i)
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind], end='')

# PREDICT
from step1_twitter_scrapper import get_tweets

data = get_tweets(10)
print(data)
X_test = vectorizer.transform(data)
predicted = model.predict(X_test)
print(predicted)



