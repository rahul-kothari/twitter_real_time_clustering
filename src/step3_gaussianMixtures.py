"""
https://scikit-learn.org/stable/modules/mixture.html#mixture
https://scikit-learn.org/stable/auto_examples/mixture/plot_gmm_selection.html
https://www.reddit.com/r/AskStatistics/comments/5ydt2c/if_my_aic_and_bic_are_negative_does_that_mean/
"""
import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.mixture import GaussianMixture
import itertools
from utils import loadCleanedReducedDimensionalityData, writeModelToFile, visualizeTrainedModel
from config import Topic

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

cov_type = input("enter cov type:")
i = cv_types.index(cov_type)
plt.plot(n_components_range, np.gradient(bic[i*len_components:(i+1)*len_components]))
plt.xlabel("Number of components")
plt.ylabel("BIC Score gradient")
plt.title("Gradient of BIC Scores across component ranges for %s covariance" % cov_type)
plt.show()

n_components = int(input("Enter the number of components: "))
model = GaussianMixture(n_components=n_components, covariance_type=cov_type)
model.fit(X)
labels = model.predict(X)

visualizeTrainedModel(X,labels,n_components, num_dimensions, 
                "Gaussian Mixtures %s - %d Dimensions, covriance type: %s" 
                    % (topicName, num_dimensions, cov_type))

file_name = input("Enter filename to store data in [WITHOUT .pkl extension]: ")+".pkl"
writeModelToFile(vectorizer, pca, model, file_name)

def gaussianClustersAreElliptical(X, model):
    """ MUST BE A 2D MODEL..."""
    colors = ['violet', 'red', 'blue', 'green', 'purple', 'orange', 'black', 'gold', 'brown', 'magenta', 'dodgerblue', 'olive']
    ax = plt.gca()
    for i, (mean, cov) in enumerate(zip(model.means_, model.covariances_)):
        color = colors[i]
        v, w = linalg.eigh(cov)
        if not np.any(Y_ == i):
            continue
        plt.scatter(X[Y_ == i, 0], X[Y_ == i, 1], .8, color=color)

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
    plt.title('GMM: 2D - full model, %d components' % num_components)
    plt.show()



"""
# Plot the BIC scores
fig = plt.figure(figsize=(8, 6))
fig.subplots_adjust(hspace=.35, bottom=.02)
bars = []
color_iter = itertools.cycle(['navy', 'turquoise', 'cornflowerblue',
                              'darkorange'])
spl = fig.add_subplot(2, 1, 1)
for i, (cv_type, color) in enumerate(zip(cv_types, color_iter)):
    xpos = np.array(n_components_range) + .2 * (i - 2)
    bars.append(plt.bar(xpos, bic[i * len(n_components_range):
                                  (i + 1) * len(n_components_range)],
                        width=.2, color=color))
plt.xticks(n_components_range)
plt.ylim([bic.min() * 1.01 - .01 * bic.max(), bic.max()])
plt.title('BIC score per model')
xpos = np.mod(bic.argmin(), len(n_components_range)) + .65 +\
    .2 * np.floor(bic.argmin() / len(n_components_range))
plt.text(xpos, bic.min() * 0.97 + .03 * bic.max(), '*', fontsize=14)
spl.set_xlabel('Number of components')
spl.legend([b[0] for b in bars], cv_types)


# Plot the winner
Y_ = clf.predict(X)
colors = ['navy', 'turquoise', 'darkorange', 'violet', 'red', 'green', 'purple', 'aqua', 'black', 'yellow']
num_components = len(set(Y_))

if num_dimensions == 3:
    ax = fig.add_subplot(2, 1, 2, projection='3d')
    for i in range(0,num_components):
        clusterName = "Component" + str(i+1)
        ax.scatter(X[Y_==i, 0], X[Y_==i, 1], X[Y_==i, 2], s=50, marker='o', color=colors[i], label=clusterName)
    ax.legend()    
    plt.title('Selected GMM: full model, %d components' % num_components)
    plt.show()

elif num_dimensions == 2:
    splot = plt.subplot(2, 1, 2)    
    for i, (mean, cov) in enumerate(zip(clf.means_, clf.covariances_)):
        color = colors[i]
        v, w = linalg.eigh(cov)
        if not np.any(Y_ == i):
            continue
        plt.scatter(X[Y_ == i, 0], X[Y_ == i, 1], .8, color=color)

        # Plot an ellipse to show the Gaussian component
        angle = np.arctan2(w[0][1], w[0][0])
        angle = 180. * angle / np.pi  # convert to degrees
        v = 2. * np.sqrt(2.) * np.sqrt(v)
        ell = mpl.patches.Ellipse(mean, v[0], v[1], 180. + angle, color=color)
        ell.set_clip_box(splot.bbox)
        ell.set_alpha(.5)
        splot.add_artist(ell)

    plt.xticks(())
    plt.yticks(())
    plt.title('Selected GMM: full model, %d components' % num_components)
    plt.show()
else: 
    raise Exception("NOT YET IMPLEMENTED")
"""