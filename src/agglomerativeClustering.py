import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering 
from sklearn.metrics import silhouette_score
import scipy.cluster.hierarchy as shc

from utils import *

#TODO: TEST WITH SINGLE LINKAGE, MIN, COMLETE, WARD, + cosine distance
def createDendogram(X):
    # Create Dendogram
    plt.title('Visualising the data') 
    Dendrogram = shc.dendrogram((shc.linkage(X, method ='ward'))) 
    plt.show()

def doSilhoutteScoreMethod(X, linkage):
    # Evaluate different models and visualize results:
    K=range(2,15)
    silhouette_scores = [] 
    for k in K:
        print("Silhoute Score method for Agglmoreative Clustering with k = ", k)
        model = AgglomerativeClustering(n_clusters=k, linkage=linkage) 
        silhouette_scores.append(silhouette_score(X, model.fit_predict(X)))
    
    # Plotting a bar graph to compare the results 
    plt.bar(K, silhouette_scores) 
    plt.xlabel('Number of clusters', fontsize = 20) 
    plt.ylabel('S(i)', fontsize = 20) 
    plt.show() 


topic=int(input("Which topic (1 for brexit / 2 for corona)?: "))
X, vectorizer = getCleanedData(topic)

num_dimensions = 3
X, pca = reduceDimensionality(X, num_dimensions)

linkageType = input("LINKAGE TYPE {\"ward\", \"complete\", \"average\", \"single\"}: ")
doSilhoutteScoreMethod(X, linkageType)

num_cluster = int(input("Number of clusters needed: "))

model = AgglomerativeClustering(n_clusters=num_cluster, linkage=linkageType)
model.fit(X)
labels = model.labels_
print('done trianing model')

visualizeTrainedModel(X, labels, num_cluster, num_dimensions)


file_name = input("Enter filename to store data in [WITHOUT .pkl extension]: ")+".pkl"
writeModelToFile(vectorizer, pca, model, file_name)

"""
LINKS:
https://www.geeksforgeeks.org/implementing-agglomerative-clustering-using-sklearn/

https://towardsdatascience.com/machine-learning-algorithms-part-12-hierarchical-agglomerative-clustering-example-in-python-1e18e0075019
"""