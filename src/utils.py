import pickle
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from config import *
from data_cleanup import remove_stopwords_and_tfidf

def getCleanedData(topic):
    """
    Gets all tweets from corresponding file. 
    Removes stopwords
    Does TFIDF.
    Paramters:
        topic:  int (1-brexit. 2-corona)
    Returns:
        X, vectorizer:   
    """
    topic=Topic(topic)
    if topic==Topic.BREXIT:
        filename = FILE_PATH
    elif topic==Topic.CORONA:
        filename = FILE_PATH_CORONA

    tweets = [line.rstrip('\n').lower() for line in open(filename)]
    # 2. remove stopwords, do tfidf
    X, vectorizer = remove_stopwords_and_tfidf(tweets)
    print('done cleaning data')
    return X, vectorizer

def reduceDimensionality(X, num_dimensions):

    # X is a sparse matrix. Need dense matrix for PCA.
    # If X too large use - Z=linkage(X.todense(),distance='cosine')
    X = X.todense()
    pca = PCA(n_components = num_dimensions) 
    X = pca.fit_transform(X) 
    print("done reducing dimension of data to ", num_dimensions, " dimensions")
    return X, pca

def visualizeTrainedModel(X, labels, num_cluster, num_dimensions):
    if num_dimensions == 3:
        colors = ['violet', 'red', 'blue', 'green', 'purple', 'orange', 'black', 'yellow']
        fig = plt.figure()
        ax = Axes3D(fig)
        for i in range(0,num_cluster):
            clusterName = "Cluster" + str(i+1)
            ax.scatter(X[labels==i, 0], X[labels==i, 1], X[labels==i, 2], s=50, marker='o', color=colors[i], label=clusterName)
        ax.legend()
        plt.show()
    elif num_dimensions == 2:
        classes = ["Cluster "+str(i) for i in range(1, num_cluster+1)]
        scatter = plt.scatter(X[:,0], X[:,1],c = labels, cmap ='rainbow') 
        plt.legend(handles=scatter.legend_elements()[0], labels=classes)
        plt.show()
    else: 
        raise Exception("NOT YET IMPLEMENTED")

def writeModelToFile(vectorizer, pca, model, file_name):
    """
    Write ai model and its vectorizer to filename.
    """    
    with open(file_name, 'wb') as f:
            pickle.dump([vectorizer, pca, model], f)
    print("model saved to ./",file_name)
  
############################ FOR STEP 3 ########################
def getStoredModelFromTopic(stored_model):
    """
    Finds the file where the ai model for this topic is stored. 
    Then retrieves the vectorizer, model and the number of clusters (for Kmeans)
    Paramters:
        stored_model:  
    Returns:
        vectorizer: 
        pca
        model: ai model
        n_cluster: intn(for kmeans)

    """

    # topic = Topic(topic)
    # if topic==Topic.BREXIT:
    #     stored_model = STORED_MODEL
    # elif topic==Topic.CORONA:
    #     stored_model = STORED_MODEL_CORONA

    n_cluster = int(stored_model.split("_")[0])
    vectorizer, pca model = pickle.load(open(stored_model, 'rb'))

    return vectorizer, model, n_cluster

def getStreamingTrackFromTopic(topic):
    """
    Based on topic, suggests the keywords to look out for while streaming tweets.
    Parameter:
        topic:  int (1-brexit. 2-corona)
    Returns:
        _track: 
    """
    topic = Topic(topic)
    if topic==Topic.BREXIT:
        _track=["brexit"]
    elif topic==Topic.CORONA:
        _track=["corona virus", "corona", "coronavirus"]
    return _track




###### OLD METHODS ##########################

def getModelCentroidsFeatureNames(topic, featuresPerCluster=20):
    """
    Prints first 20 feature of each cluster.
    topic: int
    featuresPerCluster: int - how manhy top features per cluster

    Returns:
    dict = {clusterName : space separated values.}
    """
    vectorizer, model, n_cluster = getStoredModelFromTopic(topic)
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()

    feature_names = dict()
    for i in range(n_cluster):
        names=[]
        for ind in order_centroids[i, :featuresPerCluster]:
            names.append(terms[ind])
        feature_names[(i+1)] = " ".join(names)
    
    return feature_names

# # https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/barchart.html
# # https://stackoverflow.com/questions/28931224/adding-value-labels-on-a-matplotlib-bar-chart
def createBarGraph(topic, n_cluster, tweetsPerCluster):
    """
    Creates a bar graph showing the number of tweets per cluster.
    Paramters:
        topic: int (1-brexit, 2-corona)
        n_cluster: int - 
            number of clusters in the ai model
        tweetsPerCluser: dictionary
            key=cluster number. Value = num of tweets in this cluster
    """

    feature_names = getModelCentroidsFeatureNames(topic,5)

    x=[]; y=[];
    for cluster in tweetsPerCluster.keys():
        x.append(cluster)
        y.append(tweetsPerCluster[cluster])

    fig=plt.figure()
    ax=plt.subplot()

    bars = plt.bar(x, y, align='center', alpha=0.5, color='c', edgecolor='k', linewidth=2)
    plt.xticks(x)
    plt.ylabel('#tweets')
    plt.title('#tweets per cluster')

    annot = ax.annotate("", xy=(0,0), xytext=(-20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="black", ec="b", lw=2),
                    arrowprops=dict(arrowstyle="->"))
    #TODO: Find correct values for (x,y) and xytext.
    annot.set_visible(False)        

    def update_annot(bar):    
        x = bar.get_x()+bar.get_width()/2. #cluster number
        y = bar.get_y()+bar.get_height()/2.
        #.get_x / y -> what value of x,y does the rectangle start at.
        # .get_widht/ height -> kitna mota/lamba it is..
        annot.xy = (x,y) # where to place the annonated text.
        #putting it at the center of the bar.
        text = feature_names[int(x)]
        annot.set_text(text)
        annot.get_bbox_patch().set_alpha(0.4)

    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            for bar in bars:
                cont, ind = bar.contains(event)
                if cont:
                    update_annot(bar)
                    annot.set_visible(True)
                    fig.canvas.draw_idle()
                    return
        if vis:
            annot.set_visible(False)
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)
    plt.show()
    
"""
BESST SO FAR:
Opinion Sinn Fein s election success is important but Boris Johnson is likely to be the architect of Irish unity https
2
Biased blundering and crude the BBC s Brexit Day coverage proved to me it needs reform No The BBC doesn t need Reform it
2
He is part of the metropolitan leftie elite He was also complicit in the betrayal of millions of Northern Labour lea
5
The Tories are launching a million taxpayer funded ad campaign to promote the Union And someone s leaked the cinema ad to
5
Matteo Salvini has warned European Commission President Ursula von der Leyen Italy could be the next country to quit t
2
It was because of Blair and his legacy that we have Brexit Johnson and Corbyn By the end New Labour wasn t offering        
5
So much for saving our green and pleasant land People have been jailed for less of late
7
Brexit going ahead and Trump is going to be president for four more years Nae luck ya wee baldy reptilian slimey cunt Deal 
with it and shut the fuck up you retard
2
I fought for Brexit on social media and I ll fight to get Khan out of London on social media It s my capital cit
2
Concerned food importers have revealed the mountain of paperwork they face under Boris Johnson s hard Brexit making pric   
2
"""