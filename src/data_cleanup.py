import re
from sklearn.feature_extraction.text import TfidfVectorizer
from config import STOPWORDS


def remove_urls_users_punctuations(full_text):
    """ Create the game, SpaceInvaders. Train or test it.
    Args: 
    full_text : string - a raw tweet

    Returns:
    string - removing punctuations, urls, user mentions, RT, numbers
    """
    """    
    1. Use regex to remove all user mentions, URLs, RT
    "(?:@|https?://|www)\S+|\w*\d\w*|^(RT)\s+" -> 
    words starting with @ or prefixed with ":" OR https OR https:// OR www 
    NOT followed by any whitespaces (\S+)
    OR \w*\d\w* -> remove any words with numbers.
    OR ^RT\s+ -> starts with RT followed by whitespaces.
    Replace them with "" -> use re.sub()

   2. Remove all punctuations i.e. only keep words with [a-1],[A-W],[0-9]
    Remove any other characters within the word.
    ==> re.findall(\w+)
    findall gives list. So join it.
    """
    removed_mentions_urls = re.sub(r"(?:@|https?://|www)\S+|\w*\d\w*|^(RT)\s+", "", full_text)
    removed_punctuations = re.findall(r'\w+', removed_mentions_urls)
    return " ".join(removed_punctuations)


def remove_stopwords_and_tfidf(proecessed_tweets):
    """
    Removes stopwords and assigns importance based on TF-IDF
    Args:
        proecessed_tweets: list of tweets are removing punctuations, urls etc.
    
    Returns:
        _data - removing stop words, and doing tfidf
        _vectorizer - SKLEARN.TFIDF Vectorizer Object
    """
    # remove words with numbers.
    proecessed_tweets = [ re.sub(r'\w*\d\w*', '', tweet).strip() for tweet in proecessed_tweets]
    
    _vectorizer = TfidfVectorizer(stop_words=STOPWORDS)  # pass my own list of stopwords
    _data = _vectorizer.fit_transform(proecessed_tweets)
    return _data, _vectorizer