import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from utils import loadCleanedReducedDimensionalityData, writeModelToFile, visualizeTrainedModel
from config import Topic

def gaussianClustersAreElliptical(X, model, Y_):
    """ MUST BE A 2D MODEL...
    Shows the "circumference" of the ellipsis because GMM creates clusters in shape of an ellipse (unlike kmeans where it is circular)
    Args:
        X - dataset tf-idf and pca
        Y_ - model.labels or model.predict(X): the clusters assigned to each data point!
    """
    from scipy import linalg
    import matplotlib as mpl
    colors = ['violet', 'red', 'blue', 'green', 'purple', 'orange', 'black', 'gold', 'brown', 'magenta', 'dodgerblue', 'olive']
    ax = plt.gca()
    for i, (mean, cov) in enumerate(zip(model.means_, model.covariances_)):
        color = colors[i]
        v, w = linalg.eigh(cov)
        if not np.any(Y_ == i):
            continue
        plt.scatter(X[Y_ == i, 0], X[Y_ == i, 1], s = 30, color=color, label = "Cluster %d" % (i+1))

        # Plot an ellipse to show the Gaussian component
        angle = np.arctan2(w[0][1], w[0][0])
        angle = 180. * angle / np.pi  # convert to degrees
        v = 2. * np.sqrt(2.) * np.sqrt(v)
        ell = mpl.patches.Ellipse(mean, v[0], v[1], 180. + angle, color=color)
        ell.set_clip_box(ax.bbox)
        ell.set_alpha(.5)
        ax.add_artist(ell)

    plt.xticks(())
    plt.yticks(())
    plt.legend()
    plt.title('GMM: Clusters are elliptical')
    plt.show()

topic = int(input("Enter a topic [1 for brexit / 2 for corona]: "))
topicName = Topic(topic).name
num_dimensions = input("How many dimensions should the dataset be? [2/3]: ")
num_dimensions = int(num_dimensions)
X, vectorizer, pca = loadCleanedReducedDimensionalityData(topic, num_dimensions)
# X, vectorizer = getCleanedData(topic)
# X, pca = reduceDimensionality(X, num_dimensions)

# To estimate covariance type and nu of components, 
# plot BIC scores across a range. Choose one with lowest BIC score
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
    print("covariance type= %s" % cv_type)
        
bic = np.array(bic)
len_components = len(n_components_range)

plt.plot(n_components_range, bic[:len_components], color = 'navy', label='spherical')
plt.plot(n_components_range,bic[len_components:2*len_components], color = 'turquoise', label='tied')
plt.plot(n_components_range, bic[len_components*2:len_components*3], color = 'cornflowerblue', label='diag')
plt.plot(n_components_range, bic[len_components*3:], color = 'darkorange', label='full')
plt.xlabel("Number of components")
plt.ylabel("BIC Score")
plt.title("BIC scores across covariance types and number of components", fontsize=12)
plt.legend()
plt.show()

""" NOTE IF BIC SCORE goes on decreasing (like with brexit and corona datasts), 
plot gradient of BIC of the covariance typ ewhihc is the lowest. (usually full)
see where the gradient change reduces.
Comment out the next 7 lines if this is not needed!
"""
# plot the gradient of BIC for this covariance type:
cov_type = input("enter cov type:")
i = cv_types.index(cov_type)
plt.plot(n_components_range, np.gradient(bic[i*len_components:(i+1)*len_components]))
plt.xlabel("Number of components")
plt.ylabel("BIC Score gradient")
plt.title("Gradient of BIC Scores across component ranges for %s covariance" % cov_type)
plt.show()

#  TRAIN MODEL AND PLOT THE GRAPH! 
n_components = int(input("Enter the number of components: "))
model = GaussianMixture(n_components=n_components, covariance_type=cov_type)
model.fit(X)
labels = model.predict(X)

# gaussianClustersAreElliptical(X, model, labels)
visualizeTrainedModel(X,labels,n_components, num_dimensions, 
                "Gaussian Mixtures %s - %d Dimensions, covriance type: %s" 
                    % (topicName, num_dimensions, cov_type))

file_name = input("Enter filename to store data in [WITHOUT .pkl extension]: ")+".pkl"
writeModelToFile(vectorizer, pca, model, n_components, file_name)