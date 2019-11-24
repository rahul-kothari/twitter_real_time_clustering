from config import FILE_PATH, STATE_VARIABLE_FILENAME 
from data_cleanup import remove_stopwords_and_tfidf
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pickle

def get_cleaned_data():
    """
    get tweets stored on file, remove stopwords and do TFIDF
    :returns: 
        X: Matrix converting sentences to TFIDF values. 
            Size = numOfSentences,numOfUniqueWords)
        vectorizer : TF-IDF Vectorizer.
    """
    # 1. Read data from tweets.txt
    filename = FILE_PATH
    tweets = [line.rstrip('\n').lower() for line in open(filename)]
    # doing file.readLines appends '\n' always.

    # 2. remove stopwords, do tfidf
    X, vectorizer = remove_stopwords_and_tfidf(tweets)
    return X, vectorizer

# 3. do elbow method
def elbow_method(X):
    """
    Carry out the elbow method - do KMeans on several values of number of clusters. 
    And give a plot showing how the error changes.
    """
    Sum_of_squared_distances = []
    K=range(1,15)
    for k in K:
        model = doKMeans(k,X)
        Sum_of_squared_distances.append(model.inertia_)

    plt.plot(K, Sum_of_squared_distances, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum_of_squared_distances')
    plt.title('Elbow Method For Optimal k')
    plt.show()

# 4. Do unsupervised learning
def doKMeans(num_cluster,X):
    """
    Do KMeans on a given number of clusters and data
    :returns:
        model : KMeans learned model
    """
    model = KMeans(n_clusters=num_cluster, init='k-means++', max_iter=100, n_init=1)
    model.fit(X)
    return model

# TODO : EXPERIMENT WITH OTHER UNSUPERVISED LEARING MODELS:


if __name__ == '__main__' :
    X,vectorizer = get_cleaned_data()
    #elbow_method(X)

    n_cluster = 6 # obtained after doing elbow method
    model = doKMeans(n_cluster,X)

    #Save model and vectorizer:
    with open(STATE_VARIABLE_FILENAME, 'wb') as f:
        pickle.dump([vectorizer, model], f)

    # 5. Relevant output
    # TODO
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    # prints keywords in each cluster
    for i in range(n_cluster):
        print("\nCluster %d:" % i)
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind], end='')