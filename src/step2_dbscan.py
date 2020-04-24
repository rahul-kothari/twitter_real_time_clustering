import numpy as np
from sklearn.cluster import DBSCAN 
from sklearn.neighbors import NearestNeighbors
from sklearn import metrics
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from utils import * 
from config import Topic

def getBestEpsilon(topicName, num_dimensions, X, min_samples):
    """To find the right value of eps, Create K-Nearest Neighbour model.
    Get distances of the 2nd Nearest Ngbr. Sort and plot it. 
    The knee is the best value of eps
    https://towardsdatascience.com/machine-learning-clustering-dbscan-determine-the-optimal-value-for-epsilon-eps-python-example-3100091cfbc
    """
    #optimal value of eps:
    nbrs = NearestNeighbors(n_neighbors=min_samples, metric='cosine').fit(X)
    distances, indices = nbrs.kneighbors(X)
    distances = distances[:,1]
    distances = np.sort(distances, axis=0)
    plt.plot(distances)
    plt.title("%s - %d dimensions - min_samples: %d" % (topicName, num_dimensions, min_samples))
    plt.show()


topic = int(input("Enter a topic [1 for brexit / 2 for corona]: "))
topicName = Topic(topic).name
num_dimensions = input("How many dimensions should the dataset be? [2/3]: ")
num_dimensions = int(num_dimensions)
# X, vectorizer, pca = loadCleanedReducedDimensionalityData(topic, num_dimensions)
X, vectorizer = getCleanedData(topic)
X, pca = reduceDimensionality(X, num_dimensions)

# min_samples = 2 * num_dimensions acc to  (Schubert, Sander et al, 2017
min_samples = 2 * num_dimensions 
getBestEpsilon(topicName, num_dimensions, X, min_samples)

# TRAIN MODEL AND PLOT 
eps = float(input("Enter the best epsilon val: "))
model = DBSCAN(eps = eps, min_samples = min_samples, metric='cosine')
model.fit(X) 
labels = model.labels_
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
print(n_clusters)
print('done trianing model')

unique_labels = set(labels)
#  Plot graphs this way because usually n_clusters is very high - Brexit 2d had 193!
#  this plots a range of colours!
colors = [plt.cm.nipy_spectral(each)
          for each in np.linspace(0, 3, len(unique_labels))]
# https://matplotlib.org/3.2.0/tutorials/colors/colormaps.html - for colourmaps!
if num_dimensions == 3:
    fig = plt.figure()
    ax = Axes3D(fig)
    i=-1
    ax.scatter(X[labels==i, 0], X[labels==i, 1], X[labels==i, 2], color='k', label='noise')
    for i in range(0, len(unique_labels)-1): 
        clusterName = "Cluster" + str(i+1)
        ax.scatter(X[labels==i, 0], X[labels==i, 1], X[labels==i, 2], color=colors[i], label=clusterName)
    plt.title("DBSCAN %s - %d Dimensions - %d clusters" % (topicName, num_dimensions, n_clusters))
    if n_clusters < 12: # show legend only if it fits in the image
        plt.legend()
    plt.show()

elif num_dimensions == 2:
    i=-1
    plt.scatter(X[labels==i, 0], X[labels==i, 1], color='k', label='noise')
    for i in range(0, len(unique_labels)-1): 
        clusterName = "Cluster" + str(i+1)
        plt.scatter(X[labels==i, 0], X[labels==i, 1], color=colors[i], label=clusterName)
    plt.title("DBSCAN %s - %d Dimensions - %d clusters" % (topicName, num_dimensions, n_clusters))
    if n_clusters < 12:  # show legend only if it fits int he image.
        plt.legend()
    plt.show()

file_name = input("Enter filename to store data in [WITHOUT .pkl extension]: ")+".pkl"
writeModelToFile(vectorizer, pca, model, file_name)