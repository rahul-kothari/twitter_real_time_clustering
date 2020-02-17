import pickle
import matplotlib.pyplot as plt
from config import *

def getDataFilenameFromTopic(topic):
    """
    File where all tweets related to this topic is stored.
    Paramters:
        topic:  int (1-brexit. 2-corona)
    Returns:
        filename:   str
    """
    topic=Topic(topic)
    if topic==Topic.BREXIT:
        filename = FILE_PATH
    elif topic==Topic.CORONA:
        filename = FILE_PATH_CORONA
    return filename

def getStoredModelFromTopic(topic):
    """
    Finds the file where the ai model for this topic is stored. 
    Then retrieves the vectorizer, model and the number of clusters (for Kmeans)
    Paramters:
        topic:  int (1-brexit. 2-corona)
    Returns:
        vectorizer: 
        model: ai model
        n_cluster: intn(for kmeans)

    """

    topic = Topic(topic)
    if topic==Topic.BREXIT:
        stored_model = STORED_MODEL
    elif topic==Topic.CORONA:
        stored_model = STORED_MODEL_CORONA

    n_cluster = int(stored_model.split("_")[0])
    vectorizer, model = pickle.load(open(stored_model, 'rb'))

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

def writeModelToFile(model, vectorizer, filename):
    """
    Write ai model and its vectorizer to filename.
    """    
    with open(file_name, 'wb') as f:
            pickle.dump([vectorizer, model], f)
    print("model saved to ./",file_name)

def createBarGraph(n_cluster, tweetsPerCluster):
    """
    Creates a bar graph showing the number of tweets per cluster.
    Paramters:
        n_cluster: int - 
            number of clusters in the ai model
        tweetsPerCluser: dictionary
            key=cluster number. Value = num of tweets in this cluster
    """
    x=[]; y=[];
    for cluster in tweetsPerCluster.keys():
        x.append(cluster)
        y.append(tweetsPerCluster[cluster])

    plt.bar(x, y, align='center', alpha=0.5, color='c', edgecolor='k', linewidth=2)
    plt.xticks(x)
    plt.ylabel('#tweets')
    plt.title('#tweets per cluster')
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