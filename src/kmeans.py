import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

from utils import *


def doElbowMethod(X):
    Sum_of_squared_distances = []
    K=range(1,15)
    for k in K:
        print("elbow method - doing kmeans for K=",k)
        model = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
        model.fit(X)
        Sum_of_squared_distances.append(model.inertia_)

    plt.plot(K, Sum_of_squared_distances, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum_of_squared_distances')
    plt.title('Elbow Method For Optimal k')
    plt.show()


topic = int(input("Enter a topic [1 for brexit / 2 for corona]: "))
X, vectorizer = getCleanedData(topic)

num_dimensions = 3
X, pca = reduceDimensionality(X, num_dimensions)

doElbowMethod(X)

num_cluster = int(input("Num of clusters: "))
model = KMeans(n_clusters=num_cluster, init='k-means++', max_iter=100, n_init=1)
model.fit(X)
labels = model.labels_

visualizeTrainedModel(X, labels, num_cluster, num_dimensions)

file_name = input("Enter filename to store data in [WITHOUT .pkl extension]: ")+".pkl"
writeModelToFile(vectorizer, pca, model, file_name)

def kmeansClustersAreCircular(X, model):
    from scipy.spatial.distance import cdist
    from matplotlib import pyplot as plt
    
    labels = model.labels_
    centers = model.cluster_centers_
    # plot the input data
    ax = plt.gca()
    ax.axis('equal')
    ax.scatter(X[:, 0], X[:, 1], c=labels, s=40, cmap='rainbow', zorder=2)
    # plot the representation of the KMeans model
    radii = [cdist(X[labels == i], [center]).max()
                for i, center in enumerate(centers)]
    for c, r in zip(centers, radii):
        ax.add_patch(plt.Circle(c, r, fc='#CCCCCC', lw=3, alpha=0.5, zorder=1))
    plt.title("KMeans Corona 2D Model - Clusters are only Circular:")
    plt.show()
	
def getClusterFeatures(dimensionalityReduced, pca=None, km)
	if dimensionalityReduced:
        original_space_centroids = pca.inverse_transform(km.cluster_centers_)
        order_centroids = original_space_centroids.argsort()[:, ::-1]
    else:
        order_centroids = km.cluster_centers_.argsort()[:, ::-1]

    terms = vectorizer.get_feature_names()
    for i in range(true_k):
        print("Cluster %d:" % i, end='')
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind], end='')
        print()
