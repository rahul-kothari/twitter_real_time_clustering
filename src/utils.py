import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.image as mpimg

from config import *
from data_cleanup import remove_stopwords_and_tfidf

def getCleanedData(topic):
    """
    Gets all tweets from corresponding file. Removes stopwords. Does TFIDF.
    Args:
        topic:  int (1-brexit. 2-corona)
    Returns:
        X, vectorizer:   
    """
    topic=Topic(topic).name
    filename = DATA_FILE[topic]

    tweets = [line.rstrip('\n').lower() for line in open(filename)]
    # 2. remove stopwords, do tfidf
    X, vectorizer = remove_stopwords_and_tfidf(tweets)
    print('done cleaning data')
    return X, vectorizer

def reduceDimensionality(X, num_dimensions):
    """
    Do PCA to reduce dimensions of dataset
    Args:
        X - dataset after TF-IDF vectorization
        num_dimensions - to reduce to
    Returns:
        X - Matrix reduced in dimensions
        pca - pca object fitted for this
    """
    # X is a sparse matrix. Need dense matrix for PCA.
    # If X too large use - Z=linkage(X.todense(),distance='cosine')
    X = X.todense()
    pca = PCA(n_components = num_dimensions) 
    X = pca.fit_transform(X) 
    print("done reducing dimension of data to ", num_dimensions, " dimensions")
    return X, pca

def loadCleanedReducedDimensionalityData(topic, num_dimensions):
    """
    Load the cleaned and reduced dimensinality data.

    Args:
        topic - int (1/2)
        num_dimensions - 2d or 3d model
    
    Returns:
        X, vectorizer, pca
    """

    topic = Topic(topic)
    if topic==Topic.BREXIT and num_dimensions==2:
        file_name = "data/brexit_cleaned_2d"
    elif  topic==Topic.BREXIT and num_dimensions==3:
        file_name = "data/brexit_cleaned_3d"
    elif  topic==Topic.CORONA and num_dimensions==2:
        file_name = "data/corona_cleaned_2d"
    elif  topic==Topic.CORONA and num_dimensions==3:
        file_name = "data/corona_cleaned_3d"

    X, vectorizer, pca = pickle.load(open(file_name, 'rb'))

    return X, vectorizer, pca

def writeModelToFile(vectorizer, pca, model, num_cluster, file_name):
    """
    Write ai model and its vectorizer to filename.

    Args:
        vectorizer - tfidf fitted for this model
        pca - pca fitted for the model. None if not used
        model - AI model
        num_cluster - in this model
        filename - where to store the objects.
    """ 
    with open(file_name, 'wb') as f:
            pickle.dump([vectorizer, pca, model, num_cluster], f)
    print("details saved to ./",file_name)
  

###################### KMEANS HELPERS #############################
def getClusterFeatures(km, n_cluster, vectorizer, isDimensionalityReduced, pca):
    """
    Get cluster centroids feature names
    """
    if isDimensionalityReduced:
        original_space_centroids = pca.inverse_transform(km.cluster_centers_)
        order_centroids = original_space_centroids.argsort()[:, ::-1]
    else:
        order_centroids = km.cluster_centers_.argsort()[:, ::-1]

    terms = vectorizer.get_feature_names()
    for i in range(n_cluster):
        print("Cluster %d:" % (i+1), end='')
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind], end='')
        print()

###################### utitlity across models ###################
def visualizeTrainedModel(X, labels, num_cluster, num_dimensions, title):
    """Get 2d/3d graph of model
    Args:
        X - data after performing TF-IDF and pca 
        labels - model.labels or model.predict(X)
        title - title of the graph
    """
    if num_dimensions == 3:
        colors = ['violet', 'red', 'blue', 'darkgreen', 'purple', 'orange', 'gold', 'brown', 'magenta', 'dodgerblue', 'olive']
        fig = plt.figure()
        ax = Axes3D(fig)
        for i in range(0,num_cluster):
            clusterName = "Cluster" + str(i+1)
            ax.scatter(X[labels==i, 0], X[labels==i, 1], X[labels==i, 2], s=40, marker='o', color=colors[i], label=clusterName)
        ax.legend()
    elif num_dimensions == 2:
        classes = ["Cluster "+str(i) for i in range(1, num_cluster+1)]
        scatter = plt.scatter(X[:,0], X[:,1],c = labels, cmap ='rainbow') 
        plt.legend(handles=scatter.legend_elements()[0], labels=classes)
    plt.title(title)
    plt.show()

############################ FOR STEP 4 ########################
def getStoredModel(filename):
    """
    Give the .pkl file location to retrieves the vectorizer, model and the number of clusters (for Kmeans)
    
    Args:
        filename: where is the .pkl file store

    Returns:
        vectorizer: tfidf vectorier object stored for this.
        pca: None if not done
        model: ai model
        num_cluster: int 
    """
    vectorizer, pca, model, num_cluster = pickle.load(open(filename, 'rb'))
    return vectorizer, pca, model, num_cluster

def getFinalModelForStreaming(topic):
    """Get the details of the final model for streaming. 
    Args:
        topic = int (1 for brexit...)

    :returns:
        filename, vectorizer, pca, model, num_cluster    
    """
    topic = Topic(topic).name
    filename = FINAL_MODEL[topic]  
    vec, pca, model, num_cluster = getStoredModel(filename)
    return filename, vec, pca, model, num_cluster

def createBarGraph(topic, model_name, num_cluster, tweetsPerCluster):
    """
    Draws a histogram of number of tweets per cluster.
    
    :parameters:
        topic = int (1/2)
        model_name = e.g. "KMeans - allD"
        num_cluster : int - number of clusters in the AI model
        tweetsPerCluster: dictionary - 
            keys = cluster number. 
            value = #tweets classified to be in that cluster.
    """
    my_colors = ['brown','pink', 'red', 'limegreen', 'blue', 'cyan',
                'orange', 'dodgerblue','purple', 'turquoise', 'darkorchid', 'gold']
    x = []
    y = []
    for j in range(1, num_cluster+1):
        y.append(tweetsPerCluster[j])
        x.append(j)

    fig=plt.figure()
    fig.subplots_adjust(hspace = 0.5)
    fig.suptitle("STREAMING RESULTS - %s" % Topic(topic).name, fontsize=16)
    ax=plt.subplot(211)

    bars = plt.bar(x, y, align='center', color = my_colors, edgecolor='k', linewidth=2)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x(), yval + 1., str(int(yval)))

    ax.set_xticks(x)
    # ax.set_yticks(np.array(range(0,100,5)))
    plt.title('#tweets per cluster: %s' % model_name)       

    # IF THIS THE FINAL MODEL WAS A 2D OR 3D GRAPH, REPLACE THIS WITH MODEL VISUALIZATION
    # OR ANYTHING ELSE MEANINGFUL
    ax = plt.subplot(212)
    plt.title("Cluster Features for this KMeans Model")
    if topic==1:
        img1 = mpimg.imread('kmeans_brexit_cluster_features.png')
    elif topic==2:
        img1 = mpimg.imread('kmeans_corona_cluster_features.png')
    plt.imshow(img1) 
    ax.set_axis_off()
    plt.show()