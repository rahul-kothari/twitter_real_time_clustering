# https://scikit-learn.org/stable/modules/clustering.html#birch
# https://towardsdatascience.com/machine-learning-birch-clustering-algorithm-clearly-explained-fb9838cbeed9

import numpy as np
from sklearn.cluster import Birch
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from utils import loadCleanedReducedDimensionalityData, writeModelToFile, getCleanedData, reduceDimensionality


topic = 2
num_dimensions = 3
# X, vectorizer = getCleanedData(topic)
# X, pca = reduceDimensionality(X, num_dimensions)

X, vectorizer, pca = loadCleanedReducedDimensionalityData(topic, num_dimensions)

fig = plt.figure()
fig.subplots_adjust(hspace=0.4, wspace=0.4)
fig.suptitle('BIRCH Clustering - Threshold = 0.1')
for i in range(9):
    ax = fig.add_subplot(3, 3, i+1, projection='3d')
    brfac = 50*(i+1)
    model = Birch(branching_factor=brfac, n_clusters=None, threshold=0.1)
    model.fit(X)
    labels = model.predict(X)
    n_clusters = len(set(labels))
    ax.scatter(X[:,0], X[:,1], X[:,2], c=labels, cmap='rainbow', alpha=0.7, edgecolors='b')
    ax.set_title("branching_factor= %d, num_clusters= %d" % (brfac, n_clusters))
plt.show()


fig = plt.figure()
fig.subplots_adjust(hspace=0.4, wspace=0.4)
fig.suptitle('BIRCH Clustering - Braching factor = 50')
thresholds = [0.1,0.01,0.001,1,1.5]
for i in range(5):
    ax = fig.add_subplot(3, 2, i+1, projection='3d')
    model = Birch(branching_factor=50, n_clusters=None, threshold=thresholds[i])
    model.fit(X)
    labels = model.predict(X)
    n_clusters = len(set(labels))
    ax.scatter(X[:,0], X[:,1], X[:,2], c=labels, cmap='rainbow', alpha=0.7, edgecolors='b')
    ax.set_title("threshold= %0.3f, num_clusters= %d" % (thresholds[i], n_clusters))

plt.show()
