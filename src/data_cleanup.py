import re
from sklearn.feature_extraction.text import TfidfVectorizer
from config import STOPWORDS


def remove_urls_users_punctuations(full_text):
    """ Create the game, SpaceInvaders. Train or test it.
    Parameters
    ------------
    full_text : string
        a raw tweet
    Returns
    -----------
    string - removing punctuations, urls, user mentions, RT
    """
    """    
    1. Use regex to remove all user mentions, URLs, RT
    "(?:@|https?://|www)\S+|^(RT)\s+" -> 
    words starting with @ or prefixed with ":" OR https OR https:// OR www 
    NOT followed by any whitespaces (\S+)
    OR ^RT\s+ -> starts with RT followed by whitespaces.
    Replace them with "" -> use re.sub()

   2. Remove all punctuations i.e. only keep words with [a-1],[A-W],[0-9]
    Remove any other characters within the word.
    ==> re.findall(\w+)
    findall gives list. So join it.
    """
    removed_mentions_urls = re.sub(r"(?:@|https?://|www)\S+|^(RT)\s+", "", full_text)
    removed_punctuations = re.findall(r'\w+', removed_mentions_urls)
    return " ".join(removed_punctuations)


def remove_stopwords_and_tfidf(proecessed_tweets):
    """
    Removes stopwords and assigns importance based on TF-IDF
    :param proecessed_tweets: list of tweets are removing punctuations, urls etc.
    :return: _data - removing stop words, and doing tfidf
            _vectorizer - TFIDF Vectorizer Object
    """
    _vectorizer = TfidfVectorizer(stop_words=STOPWORDS)  # pass my own list of stopwords
    _data = _vectorizer.fit_transform(proecessed_tweets)
    return _data, _vectorizer


# def remove_stopwords(data):
# [word for word in data if word.lower() not in STOPWORDS]
# OR
#     removed_stopwords = list()
#     for word in removed_punctuations:
#         if word.lower() not in STOPWORDS:
#             removed_stopwords.append(word)
#     print(removed_stopwords)
