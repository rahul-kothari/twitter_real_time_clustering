import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN 
from sklearn.neighbors import NearestNeighbors
from utils import *


def getBestEpsilon(X, min_samples):
    #optimal value of eps:
    nbrs = NearestNeighbors(n_neighbors=min_samples, metric='cosine').fit(X)
    distances, indices = nbrs.kneighbors(X)
    distances = distances[:,1]
    distances = np.sort(distances, axis=0)
    plt.plot(distances)
    plt.show()

topic=int(input("Which topic (1 for brexit / 2 for corona)?: "))
X, vectorizer = getCleanedData(topic)

num_dimensions = 3
X, pca = reduceDimensionality(X, num_dimensions)

#optimal value for min_samples:
min_samples = 50 # 2 * num_dimensions #TODO DETERMINE!

getBestEpsilon(x, min_samples)

eps = float(inout("Enter the best epsilon val: "))

model = DBSCAN(eps = epsDict["corona"][num_dimensions], min_samples = min_samples)
model.fit(X) 
labels = model.labels_
print('done trianing model')

colors = ['royalblue', 'maroon', 'forestgreen', 'mediumorchid', 'tan', 'deeppink', 'olive', 'goldenrod', 'lightcyan', 'navy']
color_vectorizer = [colours[label] for label in labels] 

if num_dimensions == 3:
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(X[:,0], X[:,1], X[:,2], c=color_vectorizer)
    plt.show()
elif num_dimensions == 2:
    plt.scatter(X[:,0], X[:,1], c=color_vectorizer)
    plt.show()
else: 
    raise Exception("NOT YET IMPLEMENTED")


"""
LINKS
 https://scikit-learn.org/stable/modules/clustering.html#dbscan

OPTIMAL VAL FOR EPS: https://towardsdatascience.com/machine-learning-clustering-dbscan-determine-the-optimal-value-for-epsilon-eps-python-example-3100091cfbc


Schubert, E., Sander, J., Ester, M., Kriegel, H. P., & Xu, X. (2017). DBSCAN revisited, revisited: why and how you should (still) use DBSCAN. ACM Transactions on Database Systems (TODS), 42(3), 19.
    For two-dimensional data: use default value of minPts=4 (Ester et al., 1996)
    For more than 2 dimensions: minPts=2*dim (Sander et al., 1998)

 """