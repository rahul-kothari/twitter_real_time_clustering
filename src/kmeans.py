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
