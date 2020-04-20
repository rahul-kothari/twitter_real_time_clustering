from utils import *
import pickle
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from config import Topic

"""
GETS TRAINED BREXIT MODELS FOR ALL D, 2,3 D
Compares graphs, cluster features, silhoutte score, inertia.
"""

topic = int(input("Enter Topic (1 for brexit / 2 for corona): "))
topicName = Topic(topic).name
models = ["all-D", "2D", "3D"]
silhoutte_scores = []
inertias = []

filenames = {
    "BREXIT": {
        "all-D" : "models/9_cluster_kmeans_brexit_allD.pkl",
        "2D" : "models/4_cluster_kmeans_brexit_2d.pkl",
        "3D" : "models/5_cluster_kmeans_brexit_3d.pkl"
    },
    "CORONA": {
        "all-D" : "models/9_cluster_kmeans_corona_allD.pkl",
        "2D" : "models/6_cluster_kmeans_corona_2d.pkl",
        "3D" : "models/4_cluster_kmeans_corona_3d.pkl"
    }
}

# Details about not reduced data
filename = filenames[topicName][models[0]]
X, _ = getCleanedData(topic)
vectorizer, _, model, num_cluster = getStoredModel(filename, False)
silhoutte_scores.append(silhouette_score(X, model.labels_))
inertias.append(model.inertia_)
print("\nCLUSTER FEATURES FOR DATASET without DIMENSIONALITY REDUCTION")
getClusterFeatures(model, num_cluster, vectorizer, False, None)

#kmeans topic 2d
num_dimensions = 2
filename = filenames[topicName][models[1]]
X,_,_ = loadCleanedReducedDimensionalityData(topic, num_dimensions)
if topic==1:
    X = X[:12159, :]
vectorizer, pca, model_2d, num_cluster_2d = getStoredModel(filename, True)
silhoutte_scores.append(silhouette_score(X, model_2d.labels_))
inertias.append(model_2d.inertia_)
print("\nCLUSTER FEATURES FOR DATASET REDUCED TO 2 DIMENSIONS")
getClusterFeatures(model_2d, num_cluster_2d, vectorizer, True, pca)

# kmeans 3d data
num_dimensions = 3
filename = filenames[topicName][models[2]]
X,_,_ = loadCleanedReducedDimensionalityData(topic, num_dimensions)
if topic==1:
    X = X[:12159, :]
vectorizer, pca, model_3d, num_cluster_3d = getStoredModel(filename, True)
silhoutte_scores.append(silhouette_score(X, model_3d.labels_))
inertias.append(model_3d.inertia_)
print("\nCLUSTER FEATURES FOR DATASET REDUCED TO 2 DIMENSIONS")
getClusterFeatures(model_3d, num_cluster_3d, vectorizer, True, pca)


fig = plt.figure()
fig.subplots_adjust(hspace=.3, bottom=.02, wspace=0.4)
fig.suptitle("Comparison across different KMeans Models on %s Dataset" % topicName, fontsize=14)

ax = fig.add_subplot(2,2,1)
x = np.arange(3)
bars = ax.bar(x, silhoutte_scores)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x(), yval + .005, "{:.2f}".format(yval))
plt.xticks(x, np.array(models))
plt.title('Silhoutte Score per model')

ax2 = fig.add_subplot(2,2,2)
bars = ax2.bar(x, inertias)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x(), yval + .005, "{:.2f}".format(yval))
plt.xticks(x, np.array(models))
ax2.set_title('Inertia per model')

ax3 = fig.add_subplot(2,2,3)
labels = model_2d.labels_
classes = ["Cluster "+str(i) for i in range(1, num_cluster_2d+1)]
scatter = ax3.scatter(X[:,0], X[:,1],c = labels, cmap ='rainbow') 
ax3.legend(handles=scatter.legend_elements()[0], labels=classes)
ax3.set_title('KMEANS %s 2D Visualization' % topicName)


ax4 = fig.add_subplot(2, 2, 4, projection='3d')
colors = ['violet', 'red', 'blue', 'green', 'purple', 'orange', 'black', 'yellow']
labels = model_3d.labels_
for i in range(0,num_cluster_3d):
    clusterName = "Cluster" + str(i+1)
    ax4.scatter(X[labels==i, 0], X[labels==i, 1], X[labels==i, 2], s=50, marker='o', color=colors[i], label=clusterName)
ax4.legend()
ax4.set_title('KMEANS %s 3D Visualization' % topicName)
plt.show()

