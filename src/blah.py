from utils import *
from config import Topic

X, vec, pca = loadCleanedReducedDimensionalityData(2,3)
X[:12159,:]
filename = "7_cluster_birch_brexit_2d.pkl"
vec, pca, model, n_clus = getStoredModel(filename, True)
visualizeTrainedModel(X, model.labels_, n_clus, 2, "BIRCH Clustering BREXIT - 2 Dimensions, brfac = 50, threshold = 0.10")