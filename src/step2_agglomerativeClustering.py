import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering 
from sklearn.metrics import silhouette_score
import scipy.cluster.hierarchy as shc
import numpy as np

from utils import *
from config import Topic

def createDendogram(X):
    """Another way to find the best number of clusters for agglomerative
    However can only experiment with 1 linkage type at a time
    So NOT USED HERE!
    """
    # Create Dendogram
    plt.title('Visualising the data') 
    Dendrogram = shc.dendrogram((shc.linkage(X, method ='ward'))) 
    plt.show()

topic = int(input("Enter a topic [1 for brexit / 2 for corona]: "))
topicName = Topic(topic).name
num_dimensions = int(input("How many dimensions should the dataset be? [2/3]: "))
# X, vectorizer, pca = loadCleanedReducedDimensionalityData(topic, num_dimensions)
X, vectorizer = getCleanedData(topic)
X, pca = reduceDimensionality(X, num_dimensions)

# Experiemnt with various linkage types and num clusters to find the best parameters
# Choose model with best silhouette score
best_model = None
best_linkage_type = None
max_silhoutte_score = -np.infty
silhouette_scores = []
linkage_types = ['ward', 'complete', 'average', 'single']
num_cluster_range = range(3,11)

# find the model combination (num_cluster and linkage type) 
# with the hhighest silhouette score
for linkage_type in linkage_types:
    for num_cluster in num_cluster_range:
        model = AgglomerativeClustering(n_clusters=num_cluster, linkage=linkage_type)
        model.fit(X)
        silhouette_scores.append(silhouette_score(X, model.labels_))
        if silhouette_scores[-1] > max_silhoutte_score:
            max_silhoutte_score = silhouette_scores[-1]
            best_model = model
            best_linkage_type = linkage_type
    print("Done with linkage_type ", linkage_type)

#plot results in a graph:
silhouette_scores = np.array(silhouette_scores)
bars = []

colors = ['navy', 'turquoise', 'cornflowerblue','darkorange']
fig = plt.figure(figsize=(8, 6))
fig.subplots_adjust(hspace=.35, bottom=.02)

fig.suptitle("Topic %s %d Dimensions" % (topicName, num_dimensions), fontsize=14)
ax = fig.add_subplot(2,1,1)

for i, link_type in enumerate(linkage_types):
    color = colors[i]
    xpos = np.array(num_cluster_range) + .2 * (i - 2)
    bars.append(plt.bar(xpos, silhouette_scores[i * len(num_cluster_range):
                                  (i + 1) * len(num_cluster_range)],
                        width=.2, color=color))
plt.xticks(num_cluster_range)
plt.ylim([silhouette_scores.min() * 1.01 - .01 * silhouette_scores.max(), silhouette_scores.max()])
plt.title('Silhoutte Score per model')
ax.set_xlabel('Number of clusters')
ax.legend([b[0] for b in bars], linkage_types)

# trained model is the one with highest silhouette score.
labels = best_model.labels_
num_cluster = len(set(labels))

# plot model visualization:
if num_dimensions == 3:
    colors = ['violet', 'red', 'blue', 'green', 'purple', 'orange', 'black', 'yellow']
    ax = fig.add_subplot(2, 1, 2, projection='3d')
    for i in range(0,num_cluster):
        clusterName = "Cluster" + str(i+1)
        ax.scatter(X[labels==i, 0], X[labels==i, 1], X[labels==i, 2], s=50, marker='o', color=colors[i], label=clusterName)
    ax.legend()
    plt.title('Agglomerative Clustering: %s linkage, %d clusters' % (best_linkage_type, num_cluster))
elif num_dimensions == 2:
    ax = fig.add_subplot(2,1,2)
    classes = ["Cluster "+str(i) for i in range(1, num_cluster+1)]
    scatter = plt.scatter(X[:,0], X[:,1],c = labels, cmap ='rainbow') 
    plt.legend(handles=scatter.legend_elements()[0], labels=classes)
    plt.title('Agglomerative Clustering: %s linkage, %d clusters' % (best_linkage_type, num_cluster))

plt.show() 
    

file_name = input("Enter filename to store data in [WITHOUT .pkl extension]: ")+".pkl"
writeModelToFile(vectorizer, pca, best_model, num_cluster, file_name)
