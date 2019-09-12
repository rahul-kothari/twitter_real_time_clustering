from config import STOPWORDS
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
# 1. Read data from tweets.txt
filename = '../data/tweets.txt'
tweets = [line.rstrip('\n').lower() for line in open(filename)]
# doing file.readLines appends '\n' always.


def remove_stopwords():
    # [word for word in removed_punctuations if word.lower() not in STOPWORDS]
    # removed_stopwords = list()
    # for word in removed_punctuations:
    #     if word.lower() not in STOPWORDS:
    #         removed_stopwords.append(word)
    # print(removed_stopwords)
    vectorizer = TfidfVectorizer(stop_words=STOPWORDS)  # pass my own list of stopwords
    data = vectorizer.fit_transform(tweets)
    return data, vectorizer
"""
2. Clean data -
    a. remove stop words
    b. use TF-IDF across all the tweets.
"""
X, vectorizer = remove_stopwords()
"""
3. Use elbow method to find number of clusters
4. Do KMeans
5. Relevant output.
"""

true_k = 3
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

order_centroids = model.cluster_centers_.argsort()[:, ::-1]
# [:,::-1] -> reverse each array

terms = vectorizer.get_feature_names()
# terms -> all tfidf feature values in sroted order acc to importance.
#
# for i in range(true_k):
#     print("Cluster %d:" % i)
#     for ind in order_centroids[i, :10]:
#         print(' %s' % terms[ind])
