import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

from utils import *
from config import Topic

def doElbowMethod(X):
    """Perrforms elbow method to estimate optimum number of clusters"""
    Sum_of_squared_distances = []
    K=range(3,15)
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

def kmeansClustersAreCircular(X, model):
    """
    Shows that KMean clusters are always circular - draws the circumference of each cluster
    Args:
        X - processed cleaned data reduced to 2 dimensions
        model - KMeans model
    """
    from scipy.spatial.distance import cdist
    
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

topic = int(input("Enter a topic [1 for brexit / 2 for corona]: "))
num_dimensions = input("How many dimensions should the dataset be? [2/3/ full]: ")
topicName = Topic(topic).name

if not num_dimensions == "full":
    num_dimensions = None
    isDimensionalityReduced = False
    X, vectorizer = getCleanedData(topic)
    pca = None
else:
    num_dimensions = int(num_dimensions)
    isDimensionalityReduced = True
    X, vectorizer, pca = loadCleanedReducedDimensionalityData(topic, num_dimensions)
    # X, vectorizer = getCleanedData(topic)
    # X, pca = reduceDimensionality(X, num_dimensions)

doElbowMethod(X)

num_cluster = int(input("Num of clusters: "))
model = KMeans(n_clusters=num_cluster, init='k-means++', max_iter=100, n_init=1)
model.fit(X)
labels = model.labels_

print("CLUSTER FEATURES FOR THIS MODEL:\n")
getClusterFeatures(model, num_cluster, vectorizer, isDimensionalityReduced, pca)

if isDimensionalityReduced:
    title = "KMEANS %s - %d Dimensions" % (topicName, num_dimensions)
    # kmeansClustersAreCircular(X, model)
    visualizeTrainedModel(X, labels, num_cluster, num_dimensions, title)

file_name = input("Enter filename to store data in [WITHOUT .pkl extension]: ")+".pkl"
writeModelToFile(vectorizer, pca, model, num_cluster, file_name)


	

