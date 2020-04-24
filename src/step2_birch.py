import numpy as np
from sklearn.cluster import Birch
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from utils import *
from config import Topic

topic = int(input("Enter a topic [1 for brexit / 2 for corona]: "))
topicName = Topic(topic).name
num_dimensions = input("How many dimensions should the dataset be? [2/3]: ")
num_dimensions = int(num_dimensions)
# X, vectorizer, pca = loadCleanedReducedDimensionalityData(topic, num_dimensions)
X, vectorizer = getCleanedData(topic)
X, pca = reduceDimensionality(X, num_dimensions)

fig = plt.figure()
fig.subplots_adjust(hspace=0.6, wspace=0.4)
fig.suptitle('BIRCH Clustering %s - %d Dimensions - Threshold = 0.1' % (topicName, num_dimensions))
for i in range(9):
    brfac = 50*(i+1)
    model = Birch(branching_factor=brfac, n_clusters=None, threshold=0.1)
    model.fit(X)
    labels = model.predict(X)
    n_clusters = len(set(labels))
    if num_dimensions == 2: 
        ax = fig.add_subplot(3, 3, i+1)
        ax.scatter(X[:,0], X[:,1], c=labels, cmap='rainbow', s=10)
    elif num_dimensions == 3:
        ax = fig.add_subplot(3, 3, i+1, projection='3d')
        ax.scatter(X[:,0], X[:,1], X[:,2], c=labels, cmap='rainbow', s=10)
    ax.set_title("branching_factor= %d, num_clusters= %d" % (brfac, n_clusters))
plt.show()


fig = plt.figure()
fig.subplots_adjust(hspace=0.6, wspace=0.4)
fig.suptitle('BIRCH Clustering %s - %d Dimensions - Braching factor = 50' % (topicName, num_dimensions))
thresholds = [0.001, 0.01, 0.05, 0.1, 0.5, 1]
for i in range(6):
    model = Birch(branching_factor=50, n_clusters=None, threshold=thresholds[i])
    model.fit(X)
    labels = model.predict(X)
    n_clusters = len(set(labels))
    if num_dimensions == 2: 
        ax = fig.add_subplot(2, 3, i+1)
        ax.scatter(X[:,0], X[:,1], c=labels, cmap='rainbow', s=10)
    elif num_dimensions == 3:
        ax = fig.add_subplot(2,3, i+1, projection='3d')
        ax.scatter(X[:,0], X[:,1], X[:,2], c=labels, cmap='rainbow', s=10)
    ax.set_title("threshold= %0.3f, num_clusters= %d" % (thresholds[i], n_clusters))

plt.show()

brfac = int(input("Enter the branching factor for the BIRCH model: "))
threshold = float(input("Enter the threshold for the BIRCH model: "))
model = Birch(branching_factor=brfac, threshold=threshold, n_clusters=None)
model.fit(X)
labels = model.predict(X)
num_cluster = len(set(labels))

visualizeTrainedModel(X, labels, num_cluster, num_dimensions, 
                    "BIRCH Clustering %s - %d Dimensions, brfac = %d, threshold=%.2f" 
                        % (topicName, num_dimensions, brfac, threshold))
file_name = input("Enter filename to store data in [WITHOUT .pkl extension]: ")+".pkl"
writeModelToFile(vectorizer, pca, model, num_cluster, file_name)


