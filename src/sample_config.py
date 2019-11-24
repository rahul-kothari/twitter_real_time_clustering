# Twitter Consumer API Key
CONSUMER_KEY = "XXX"
CONSUMER_API_SECRET = "XXX""

# Twitter Access Token
ACCESS_TOKEN = "XXX"
ACCESS_TOKEN_SECRET = "XXX"

# NO OF TWEETS NEEDED
NUM_OF_TWEETS_NEEDED = 10000
# file to store tweets (testing or otherwise)
FILE_PATH = "data/tweets.txt"
FILE_PATH2 = "data/trial.txt" # for testing

# store vectorizer, ai model
STATE_VARIABLE_FILENAME = "state_variables.pkl"

# TOPIC (testing or otherwise)
TOPIC2 = "music OR sports OR blockchain OR politics OR education -filter:retweets"
TOPIC = "brexit OR #stopbrexit OR #brexitshambles OR #remain OR #brexitdeal" + \
        "OR #referendum OR #hardbrexit OR #antibrexit OR #StopBrexit" + \
        "OR nodeal OR #nodelabrexit OR #probrexit OR #2ndreferendum" + \
        "OR #Tory OR #GetJohnsonOut OR #GetTheToriesOut OR #TacticalVote" +\
        "OR #ToriesOut OR #PeoplesVote OR #UKelection2019 OR #voteleave" +\
        "OR #VoteLabour2019 #LabourForHope #UKLabour #brexitchaos" + \
        "OR #economy" +\
        "-filter:retweets"
        

STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]