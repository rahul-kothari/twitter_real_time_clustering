## TODO: 

1. KMEANS-
	- Can get cluster feature names even after PCA. (https://scikit-learn.org/stable/auto_examples/text/plot_document_clustering.html#sphx-glr-auto-examples-text-plot-document-clustering-py)
	refer code in kmeans.py
	- Do MinIbATCH.
1. Agglomerative 
	- compare different linkage techniques: https://scikit-learn.org/stable/auto_examples/cluster/plot_digits_linkage.html#sphx-glr-auto-examples-cluster-plot-digits-linkage-py
2. DBSCAN
	- you are getting eps based on cosine value. So DBSCAN bhi on cosine distance!
3. birch -
	try on full dimensions.
	graph - remove border of har dot lol
3. GMM - Try with higher cluster numbers.... WHY IS bic so negative?
	https://towardsdatascience.com/gaussian-mixture-model-clusterization-how-to-select-the-number-of-components-clusters-553bef45f6e4
4. all models jaha overlap seems to happen - rotate that graph! overlap shayad kyunki z level sabke same hai! (gmm, birch)

5. Unsupervised learning validation techniques
    * ROC curves, 
    * matrix validation etc.

    - Compare other models in these models.


## THESIS RELATED NOTES/CHANGES/ADDITIONS/THINGS TO TALK ABOUT:

**To write in Thesis**:
* 3 types of anamolies (point, collective, contextual). Yours is collective. Call them topics coz yours is that
* talk about your pipeline, snippets of scripts, graphically represent clusters,..
* UML dg like seqeunce, activity dg shows collection of tweets...
* testing related bs

* doing corona -> I would get utf8 decoding errors coz chinese/arabic/hindi characters would pass through. Had to mannually delete them by identifyig where they came.

* people writing with abbreviations and typos also cause problems.

* annotated bar graphs with top 5 feature names.

* DBSCAN somehow not working. Wanted to use it coz i tought it would automatically label noise valyes that can be seen for corona kmeans 5 cluster 2d model.
* OPTICS - also showing same problem
* DBSCAN, OPTICS - having min_samples very big like 1000 gave all noises. (WHY?). Only small gave variety. But that gave way too much variety. Small min_samples have like 300 clusters lol
* BIRCH - Doing BIRCH on full dimensions gave only 1 cluster. num_cluster is always same despite branching factor. Varying threshold - se nonsense. Problem: clusters overlap.
* Guassian Mixtures - kmeans clusters are only circular (shown in Kmeans Corona 2d pic). GMM can be elliptical! https://jakevdp.github.io/PythonDataScienceHandbook/05.12-gaussian-mixtures.html

* ***take pros and cons of each model from here:https://scikit-learn.org/stable/modules/mixture.html#mixture***

**NOTES = CONFIG.PY ka topic was not giving anything interesting.** SO I started with seearch params like:
"brexit and economy
brexit ADN politics
brexit AND tourism
brexit and tories
brexit and johnson
...
no-deal brexit
brexit and stock market
brexit banking
brexit jobs
brexit tech
brexit sterling

corona virus jobs
corona virus sports
corona virus economy/banks/stock market
corona virus hospitals

### CHANGES:
1. Collected data as above because the general form gave very generic data, and often very slangy/ useless tweets like "brexit." "gone" that are created because we remove all pics, websites, user mentions.
2. Removed numbers in tweets as they messed up clustering
3. removed emojis and other non english characters.

### CHANGES MADE AFTER KMEANS:
4. Added stop wrods like "via", "amp" and other useless words that end up as the top 20 keywords defining my clusters
5. Realization ki words like "boris johnson" should be treated as one instead of 2 separate. Same for phrases.
6. Words like "BBC NEWS" etc. should be ideally ignored.

interestingly, after doing change 4 - elbow method didn't give any good data. SO left it with initial kmeans.

## STEPS:
### ==================0. Create virtual environment==============
.\venv\Scripts\activate
.\venv\Scripts\deactivate

### ===================1. SCRAPPING TWITTER (training)===============
Get statuses, replies,quote tweets with q="brexit". Ignore retweets
[entities - has all urls, hashtags, mentions etc. If truncated==true -> use full text. Warna text?]

NEXT STEP - check which hashtags among thos ein config actually needed,
            doing tf-idf in python

Filter out retweets - they are the same content repeated twice

QUESTIONS: (don't delete - need for documentation)
1. will "brexit" get #brexit, Brexit, #Brexit too?  YES
2. Need replies, quote tweets also                  XXX
3. best encoding for removing "b", unicode chars    DONE
4. does "nodeal" get #NoDeal too?                   YES
5. Need #brexitShambles all tweets with similar # too...
6. need those tweets with "brexity" - i.e. suffix/prefix to "brexit"
7. How to get around 10000 tweets at once? - using "wait_on_rate_limit" -> because if you do try and exception on cursor to catch TweepError - u might get blacklisted...
8. does my way of avoid getting same tweets again?

Store every text (only text) in .txt (new line pe)
For efficiency - first write in a list and do write() only once! doing so many system calls is very slow!

http://docs.tweepy.org/en/latest/cursor_tutorial.html
http://docs.tweepy.org/en/latest/api.html#API.search
https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators
https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/intro-to-tweet-json
ALL HASHTAG SOURCES:
https://ukandeu.ac.uk/how-remain-and-leave-camps-use-hashtags/
https://ritetag.com/best-hashtags-for/brexit

### ===================2. Filter Words======================
Remove user mentions, uris,RT - "(?:@|https?://|www|RT)\S+"
Remove punctuations, spl chaacters, emojis -
Not using nltk.tokenize.word_tokenize
Instead regex - '\w+' only keep chars that are [0-9],[a-z],[A-Z]
REMOVE NUMBERS TOO (\w*\d\w*) as it effects the ai model.
### ====================3. UNSUPERVISED LEARNING==========
Need to further clean data -
remove stop words
Stop words are words that are grammatically essential to structure,
but contribute very little to the context of a sentence.
Got stop words from the nltk pacakge - found it to be most comprehensive. SKlearn's list has several known issues
(https://scikit-learn.org/stable/modules/feature_extraction.html#stop-words)

Now use TF-IDF across all the tweets to extract import words
(COPY DESCRIPTION IN towardsdaatscience website)

Once the data was cleaned up it was now ready for machine learning.

use "elbow method" to find optimal "k"
do k-means

https://towardsdatascience.com/applying-machine-learning-to-classify-an-unsupervised-text-document-e7bb6265f52


### =====================6. Real time classification==========
use code in event_catcher.py to catch tweets in real time and classify model on the fly! (ASYNC MODE!)
http://docs.tweepy.org/en/latest/streaming_how_to.html#a-few-more-pointers
https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters

### ====================7. Graphs========================
Store the results and present graphs or shit.