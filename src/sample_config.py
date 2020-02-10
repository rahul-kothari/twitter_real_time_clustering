# Twitter Consumer API Key
CONSUMER_KEY = "XXX"
CONSUMER_API_SECRET = "XXX""

# Twitter Access Token
ACCESS_TOKEN = "XXX"
ACCESS_TOKEN_SECRET = "XXX"

# NO OF TWEETS NEEDED
NUM_OF_TWEETS_NEEDED = 10000
# file to store tweets (testing or otherwise)
FILE_PATH = "data/brexit.txt"
FILE_PATH_CORONA = "data/corona.txt"
FILE_PATH3 = "data/trial.txt" # for testing

# TOPIC (testing or otherwise)
TOPIC = "brexit OR #brexitShambles OR #stopbrexit OR #remain OR #brexitdeal" + \
        "OR #hardbrexit OR #antibrexit OR #StopBrexit OR election" + \
        "OR nodeal OR #nodelabrexit OR british" + \
        "OR #Tory OR #GetJohnsonOut OR #GetTheToriesOut OR #TacticalVote" +\
        "OR #ToriesOut" +\
        "OR #VoteLabour2019 OR #LabourForHope OR #UKLabour" + \
        "OR #economy OR #stockMarket OR #labour OR #tories OR No-Deal"+\
        "-filter:retweets"
# from:RahulKo96245846

TOPIC2 = "Brexit sterling-filter:retweets"

TOPIC_CORONA = "coronavirus OR corona virus -filter:retweets" 

# Stop Words
STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]