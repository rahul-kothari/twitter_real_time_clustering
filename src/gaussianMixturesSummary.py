import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from utils import loadCleanedReducedDimensionalityData, getStoredModel
from config import Topic


final_cov_type = "full"
# summary[TOPIC_NAME][NUM_DIMENSION] = NUM_COMPONENT for this model
filenames = {
    "BREXIT": {
        2 : "7_cluster_gmm_brexit_2d.pkl",
        3 : "7_cluster_gmm_brexit_3d.pkl"
    },
    "CORONA": {
        2 : "5_cluster_gmm_corona_2d.pkl",
        3 : "6_cluster_gmm_corona_3d.pkl"
    }
}
summary = {"BREXIT": {2:7 , 3:7 }, "CORONA": {2:5 ,3:6}}


topic = int(input("Enter a topic [1 for brexit / 2 for corona]: "))
topicName = Topic(topic).name
num_dimensions = input("How many dimensions should the dataset be? [2/3]: ")
num_dimensions = int(num_dimensions)
X, vectorizer, pca = loadCleanedReducedDimensionalityData(topic, num_dimensions)

bic = []
n_components_range = range(2, 14)
cv_types = ['spherical', 'tied', 'diag', 'full']
for cv_type in cv_types:
    for n_components in n_components_range:
        # Fit a Gaussian mixture with EM
        gmm = GaussianMixture(n_components=n_components,
                                      covariance_type=cv_type)
        gmm.fit(X)
        bic.append(gmm.bic(X))
        
bic = np.array(bic)
len_components = len(n_components_range)

fig = plt.figure()
fig.subplots_adjust(hspace=0.6, wspace=0.3, left=0.1, right = 0.95)
fig.suptitle("Gaussian Mixture %s (%d Dimension) Summary" % (topicName, num_dimensions), fontsize=16)
gs = fig.add_gridspec(2, 2)

ax = fig.add_subplot(gs[0, :])
ax.plot(n_components_range, bic[:len_components], color = 'navy', label='spherical')
ax.plot(n_components_range,bic[len_components:2*len_components], color = 'turquoise', label='tied')
ax.plot(n_components_range, bic[len_components*2:len_components*3], color = 'cornflowerblue', label='diag')
ax.plot(n_components_range, bic[len_components*3:], color = 'darkorange', label='full')
ax.set_xlabel("Number of components")
ax.set_ylabel("BIC Score")
plt.title("BIC scores across covariance types and number of components", fontsize=12)
plt.legend()

ax2 = fig.add_subplot(gs[1, 0]) 
ax2.plot(n_components_range, np.gradient(bic[3*len_components:]))
ax2.set_xlabel("Number of components")
ax2.set_ylabel("BIC Score gradient")
plt.title("Gradient of BIC Scores across component ranges for %s covariance" % final_cov_type)


n_components = summary[topicName][num_dimensions]

filename = filenames[topicName][num_dimensions]
vec, pca, gmm, n_clus = getStoredModel(filename, True)
Y_ = gmm.predict(X)

colors = ['violet', 'red', 'blue', 'darkgreen', 'purple', 'orange', 'gold', 'brown', 'magenta', 'dodgerblue']
classes = ["Cluster "+str(i) for i in range(1, n_components+1)]
if num_dimensions == 3:
    ax = fig.add_subplot(gs[1, 1], projection='3d')
    for i in range(0,n_components):
        ax.scatter(X[Y_==i, 0], X[Y_==i, 1], X[Y_==i, 2], s=30, marker='o', color=colors[i], label=classes[i])
    ax.legend()  
    plt.title("Model Visualization - %d clusters" % n_components)
    
elif num_dimensions == 2:
    ax = fig.add_subplot(gs[1,1])
    scatter = ax.scatter(X[:,0], X[:,1],c = Y_, cmap ='rainbow') 
    ax.legend(handles=scatter.legend_elements()[0], labels=classes, loc='upper right')
    plt.title('Model Visualization - %d clusters' % n_components)
plt.show()
