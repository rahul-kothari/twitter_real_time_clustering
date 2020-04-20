import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.image as mpimg
from config import *
from data_cleanup import remove_stopwords_and_tfidf

def saveData():
    """
    For each topic and dimension combo, get X( cleaned data), vectorizer, pca (IN THAT ORDER)
    and save them to data folder. So you don't have to keep computing it.    
    """
    filenames = ["data/brexit_cleaned_2d", "data/brexit_cleaned_3d", 
            "data/corona_cleaned_2d", "data/corona_cleaned_2d"]
    i=0
    topics = [1,2]
    dimensions = [2,3]
    for topic in topics:
        for num_dimension in dimensions:
            X, vectorizer = getCleanedData(topic)
            X, pca = reduceDimensionality(X, num_dimensions)
            with open(filenames[i], 'wb') as f:
                    pickle.dump([X, vectorizer, pca], f)
            print("data saved to ./",file_name)
            i+=1

def reduceDimensionality(X, num_dimensions):
    # X is a sparse matrix. Need dense matrix for PCA.
    # If X too large use - Z=linkage(X.todense(),distance='cosine')
    X = X.todense()
    pca = PCA(n_components = num_dimensions) 
    X = pca.fit_transform(X) 
    print("done reducing dimension of data to ", num_dimensions, " dimensions")
    return X, pca

def getCleanedData(topic):
    """
    Gets all tweets from corresponding file. Removes stopwords. Does TFIDF.
    Paramters:
        topic:  int (1-brexit. 2-corona)
    Returns:
        X, vectorizer:   
    """
    topic=Topic(topic)
    if topic==Topic.BREXIT:
        filename = FILE_PATH_BREXIT
    elif topic==Topic.CORONA:
        filename = FILE_PATH_CORONA

    tweets = [line.rstrip('\n').lower() for line in open(filename)]
    # 2. remove stopwords, do tfidf
    X, vectorizer = remove_stopwords_and_tfidf(tweets)
    print('done cleaning data')
    return X, vectorizer

def loadCleanedReducedDimensionalityData(topic, num_dimensions):
    """
    Load the cleaned and reduced dimensinality data.

    :parameters:
        topic - int (1/2)
        num_dimensions - 2d or 3d model
    
    :returns:
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

def writeModelToFile(vectorizer, pca, model, file_name):
    """
    Write ai model and its vectorizer to filename.
    """    
    if not pca==None:
        with open(file_name, 'wb') as f:
                pickle.dump([vectorizer, pca, model], f)
    else:
        with open(file_name, 'wb') as f:
                pickle.dump([vectorizer, model], f)
    print("model saved to ./",file_name)
  

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
    """Get 2d/3d graph of model"""
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
def getStoredModel(filename, isDimensionalityReduced):
    """
    Finds the file where the ai model for this topic is stored. 
    Then retrieves the vectorizer, model and the number of clusters (for Kmeans)
    Paramters:
        filename:
        isDimnesionalityReduced (was pca done?)  
    Returns:
        vectorizer: 
        pca
        model: ai model
        n_cluster: intn(for kmeans)

    """
    n_cluster = int(filename.split("_")[0])
    pca = None
    if isDimensionalityReduced:
        vectorizer, pca, model = pickle.load(open(filename, 'rb'))
    else:
        vectorizer, model = pickle.load(open(filename, 'rb'))
    return vectorizer, pca, model, n_cluster

def getFinalModelForStreaming(topic):
    """Get the filename (of the final model) and Track for streaming
    :params:
        topic = int (1 for brexit...)"""
    topic = Topic(topic)
    if topic == Topic.BREXIT:
        filename = STORED_MODEL_BREXIT
    elif topic == Topic.CORONA:
        filename = STORED_MODEL_CORONA
    isDimensionalityReduced = False   
    vec, pca, model, num_cluster = getStoredModel(filename, isDimensionalityReduced)
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

    ax = plt.subplot(212)
    plt.title("Cluster Features for this KMeans Model")
    if topic==1:
        img1 = mpimg.imread('kmeans_brexit_cluster_features.png')
    elif topic==2:
        img1 = mpimg.imread('kmeans_corona_cluster_features.png')
    plt.imshow(img1) 
    ax.set_axis_off()
    plt.show()