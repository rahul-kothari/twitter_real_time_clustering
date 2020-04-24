import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from config import *
from utils import *

"""
UTILITY SCRIPT
Simply change the filename and topic number
"""
filename = "kmeans_brexit_allD_9_clusters.pkl"
topic = 1

# X, _ = getCleanedData(topic)
vec, pca, model, num_cluster = getStoredModel(filename)
labels = model.labels_ # or model.predict(X)
tweetsPerCluster = [0] * num_cluster

x = ["Cluster "+str(i) for i in range(1, num_cluster+1)]

for label in labels:
    tweetsPerCluster[label]= tweetsPerCluster[label]+1

my_colors = ['brown','pink', 'red', 'limegreen', 'blue', 'cyan',
    'orange', 'dodgerblue','purple', 'turquoise', 'darkorchid', 'gold']
bars = plt.bar(x, tweetsPerCluster, align='center', color = my_colors, edgecolor='k', linewidth=2)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x(), yval + 50., str(int(yval)))
plt.xticks(x)
# plt.yticks(np.arange(0,4000,500))
plt.title('%s - classifying all tweets in the dataset using %s' % (Topic(topic).name, filename), fontsize=16)  