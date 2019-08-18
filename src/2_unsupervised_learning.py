from config import STOPWORDS
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
# 1. Read data from tweets.txt
filename = '../data/tweets.txt'
tweets = [line.rstrip('\n').lower() for line in open(filename)]
# doing file.readLines appends '\n' always.
"""
2. Clean data -
    a. remove stop words
    b. use TF-IDF across all the tweets.
"""
# [word for word in removed_punctuations if word.lower() not in STOPWORDS]
# removed_stopwords = list()
# for word in removed_punctuations:
#     if word.lower() not in STOPWORDS:
#         removed_stopwords.append(word)
# print(removed_stopwords)
vectorizer = TfidfVectorizer(stop_words=STOPWORDS)  # pass my own list of stopwords
X = vectorizer.fit_transform(tweets)

"""
3. Use elbow method to find number of clusters
4. Do KMeans
5. Relevant output.
"""

true_k = 3
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()

for i in range(true_k):
    print("Cluster %d:" % i)
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind])
