import numpy as np
from sklearn.cluster import DBSCAN 
from sklearn.neighbors import NearestNeighbors
from sklearn import metrics
from utils import * 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from config import Topic

def getBestEpsilon(topicName, num_dimensions, X, min_samples):
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

# if not num_dimensions == "full":
num_dimensions = int(num_dimensions)
isDimensionalityReduced = True
X, vectorizer, pca = loadCleanedReducedDimensionalityData(topic, num_dimensions)
# else:
    # num_dimensions = None
    # isDimensionalityReduced = False
    # X, vectorizer = getCleanedData(topic)
    # pca = None
    # X = X.todense()

min_sample_Values = {"BREXIT": {2: 50, 3:40}, "CORONA": {2:50, 3:50}}
min_samples = min_sample_Values[topicName][num_dimensions]
# min_samples = 2 * num_dimensions
getBestEpsilon(topicName, num_dimensions, X, min_samples)

eps = float(input("Enter the best epsilon val: "))
model = DBSCAN(eps = eps, min_samples = min_samples, metric='cosine')
model.fit(X) 
labels = model.labels_
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
print(n_clusters)
print('done trianing model')

unique_labels = set(labels)
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
    plt.legend()
    plt.show()

elif num_dimensions == 2:
    i=-1
    plt.scatter(X[labels==i, 0], X[labels==i, 1], color='k', label='noise')
    for i in range(0, len(unique_labels)-1): 
        clusterName = "Cluster" + str(i+1)
        plt.scatter(X[labels==i, 0], X[labels==i, 1], color=colors[i], label=clusterName)
    plt.title("DBSCAN %s - %d Dimensions - %d clusters" % (topicName, num_dimensions, n_clusters))
    # plt.legend()
    plt.show()
else: 
    raise Exception("NOT YET IMPLEMENTED")

file_name = input("Enter filename to store data in [WITHOUT .pkl extension]: ")+".pkl"
writeModelToFile(vectorizer, pca, model, file_name)

"""
LINKS
 https://scikit-learn.org/stable/modules/clustering.html#dbscan

OPTIMAL VAL FOR EPS: https://towardsdatascience.com/machine-learning-clustering-dbscan-determine-the-optimal-value-for-epsilon-eps-python-example-3100091cfbc


Schubert, E., Sander, J., Ester, M., Kriegel, H. P., & Xu, X. (2017). DBSCAN revisited, revisited: why and how you should (still) use DBSCAN. ACM Transactions on Database Systems (TODS), 42(3), 19.
    For two-dimensional data: use default value of minPts=4 (Ester et al., 1996)
    For more than 2 dimensions: minPts=2*dim (Sander et al., 1998)

DBSCAN PAPER = https://www.aaai.org/Papers/KDD/1996/KDD96-037.pdf
 """