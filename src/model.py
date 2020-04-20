from utils import getStoredModel

class Model:

    def __init__(self, filename, isDimensionalityReduced):
        self.filename = filename
        split = self.filename.split("_")
        self.name = split[2] + " - " + split[-1][:-4]
        self.isDimensionalityReduced = isDimensionalityReduced
        self.vectorizer, self.pca, self.model, self.n_cluster = getStoredModel(filename, isDimensionalityReduced)
        self.clusterToTweetsText = dict()
        self.clusterToNumberOfTweets = dict()
        self._initializeDictionary()

    def _initializeDictionary(self):
        for cluster in range(1, self.n_cluster+1):
            self.clusterToNumberOfTweets[cluster]=0
            self.clusterToTweetsText[cluster]=list()
    
    def prettyPrintClusterToTweets(self):
        print(self.name)
        for cluster in self.clusterToTweetsText.keys():
            print(cluster, ' :')
            for tweet in self.clusterToTweetsText[cluster]:
                print('\t', tweet)
            print()
        
    def __str__(self):
        return self.name
