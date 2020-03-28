import numpy as np
from sklearn.cluster import DBSCAN 
from sklearn.neighbors import NearestNeighbors
from sklearn import metrics
from utils import loadCleanedReducedDimensionalityData, writeModelToFile, getCleanedData, reduceDimensionality
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def getBestEpsilon(X, min_samples):
    #optimal value of eps:
    nbrs = NearestNeighbors(n_neighbors=min_samples, metric='cosine').fit(X)
    distances, indices = nbrs.kneighbors(X)
    distances = distances[:,1]
    distances = np.sort(distances, axis=0)
    plt.plot(distances)
    plt.title("min_samples: %d" % min_samples)
    plt.show()

#topic=int(input("Which topic (1 for brexit / 2 for corona)?: "))
topic = 1
num_dimensions = 3
X, vectorizer, pca = loadCleanedReducedDimensionalityData(topic, num_dimensions)

# #optimal value for min_samples:
min_samples =  3# 2 * num_dimensions #TODO DETERMINE!
#try for varying values!
epsDictCorona3d = {6 : 0.00379008, 9: 0.00323422, 12: 0.00332292, 
    15: 0.00338888, 18: 0.00330463, 50: 0.00359, 10: 0.00374487}
epsDictBrexit3d = {10: 0.00097736, 1000: 0.00125847}

# G = gridspec.GridSpec(4, 4)
# ax1 = plt.subplot(G[0, :])

# for min_samples in range (4, 50, 3):
if not min_samples in epsDictBrexit3d:
    getBestEpsilon(X, min_samples)
    eps = float(input("Enter the best epsilon val: "))
    epsDictBrexit3d[min_samples] = eps
else:
    eps = epsDictBrexit3d[min_samples]
model = DBSCAN(eps = eps, min_samples = min_samples)
model.fit(X) 
labels = model.labels_
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
print(n_clusters)
print(set(labels))
print(min_samples, " - num clusters = ", n_clusters, " Silhoutte Score %0.3f" % metrics.silhouette_score(X, labels))
print('done trianing model')

unique_labels = set(labels)
colors = [plt.cm.gnuplot2(each)
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
    ax.legend()
    plt.show()

elif num_dimensions == 2:
    i=-1
    plt.scatter(X[labels==i, 0], X[labels==i, 1], color='k', label='noise')
    for i in range(0, len(unique_labels)-1): 
        clusterName = "Cluster" + str(i+1)
        plt.scatter(X[labels==i, 0], X[labels==i, 1], color=colors[i], label=clusterName)
    plt.legend()
    plt.show()
else: 
    raise Exception("NOT YET IMPLEMENTED")

# file_name = input("Enter filename to store data in [WITHOUT .pkl extension]: ")+".pkl"
# writeModelToFile(vectorizer, pca, model, file_name)

"""
LINKS
 https://scikit-learn.org/stable/modules/clustering.html#dbscan

OPTIMAL VAL FOR EPS: https://towardsdatascience.com/machine-learning-clustering-dbscan-determine-the-optimal-value-for-epsilon-eps-python-example-3100091cfbc


Schubert, E., Sander, J., Ester, M., Kriegel, H. P., & Xu, X. (2017). DBSCAN revisited, revisited: why and how you should (still) use DBSCAN. ACM Transactions on Database Systems (TODS), 42(3), 19.
    For two-dimensional data: use default value of minPts=4 (Ester et al., 1996)
    For more than 2 dimensions: minPts=2*dim (Sander et al., 1998)

DBSCAN PAPER = https://www.aaai.org/Papers/KDD/1996/KDD96-037.pdf
 """