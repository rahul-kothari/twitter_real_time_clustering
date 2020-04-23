#  Twitter Consumer API Key
CONSUMER_KEY = "xxx"
CONSUMER_API_SECRET = "xxx"

# Twitter Access Token
ACCESS_TOKEN = "xxx"
ACCESS_TOKEN_SECRET = "xxx"

import enum
# Using enum class create enumerations
class Topic(enum.Enum):
   BREXIT = 1
   CORONA = 2

# file to store tweets (testing or otherwise)
DATA_FILE = {
        "BREXIT" : "data/brexit.txt",
        "CORONA" : "data/corona.txt",
        "TRIAL" : "data/trial.txt" # for testing
}

# Keywords to look out for mining tweets (step 1)
# https://developer.twitter.com/en/docs/tweets/rules-and-filtering/guides/using-premium-operators
MINING_TOPIC = {
        "BREXIT" : "(brexit nhs) OR (brexit eu) -filter:retweets",
        "CORONA" : "(corona stock markets) OR (coronavirus economy) -filter:retweets"
}

# TOPIC (testing or otherwise)
# TOPIC = "brexit OR #brexitShambles OR #stopbrexit OR #remain OR #brexitdeal" + \
#         "OR #hardbrexit OR #antibrexit OR #StopBrexit OR election" + \
#         "OR nodeal OR #nodelabrexit OR british" + \
#         "OR #Tory OR #GetJohnsonOut OR #GetTheToriesOut OR #TacticalVote" +\
#         "OR #ToriesOut" +\
#         "OR #VoteLabour2019 OR #LabourForHope OR #UKLabour" + \
#         "OR #economy OR #stockMarket OR #labour OR #tories OR No-Deal"+\
#         "-filter:retweets"

# keywords to stream for (step 3)
STREAMING_TRACK = {
        "BREXIT" : ["brexit nhs", "brexit tech", "brexit economy", "brexit pound", "brexit jobs", 
                        "brexit eu", "brexit business", "brexit trade", "brexit trump"],
        "CORONA" : ["coronavirus nhs", "coronavirus economy", "coronavirus wuhan", 
                "coronavirus trump", "coronavirus jobs", "coronavirus stock market"]
}

# final model used for streaming (step 3)
FINAL_MODEL = {
        "BREXIT" : "kmeans_brexit_allD_9_clusters.pkl",
        "CORONA" : "kmeans_corona_allD_9_clusters.pkl"
}

# Stop Words
STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]