from utils import *
from config import *

topic = 2
num_dimensions = 3
# BIRCH: BREXIT : {2D - 7, 3D - 12}, CORONA : {2D - 8, 3D - 10}
# GMM:   BREXIT : {2D - 7, 3D - 7},  CORONA : {2D - 5,  3d - 6}
filename = "6_cluster_gmm_corona_3d.pkl"
# "8_cluster_birch_corona_2d.pkl"
# "7_cluster_gmm_brexit_2d.pkl"
# "5_cluster_gmm_corona_2d.pkl"

X, _, _ = loadCleanedReducedDimensionalityData(topic, num_dimensions)
vec, pca, model, n_clus = getStoredModel(filename, True)
labels = model.predict(X)

outliers = np.where(labels == 5)
outliers = outliers[0]

tweets_data = FILE_PATH_BREXIT if topic == 1 else FILE_PATH_CORONA
tweets = [line.rstrip('\n').lower() for line in open(tweets_data)]
for ind in outliers:
    print(str(labels[ind]+1) + "-> "+ tweets[ind])