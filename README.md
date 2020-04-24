# Real-time Collective Event Stream Detection from Twitter Streams

The idea of this project was to get tweets related to a topic in real-time and use unsupervised learning techniques to cluster them into various sub-topics to analyse the popular domains with respect to the trend. 

The code already works for two such trends: Brexit and Coronavirus.

I have included the original dataset for Brexit and Coronavirus. So even without Twitter auth tokens, you can create the AI models!

I also included the 18 models I created and experimented with. They are in the `other_models` folder

In the graphs folder, you shall find graphs related to the 4 AI algorithms and graphs produced on streaming. 

All of these graphs can be easily reproduced! 

As shown below, you need twitter auth tokens only for step 1 (mining) and step 3 (streaming)

The best models for both topics were K-Means all Dimensions (with no dimensionality reduction). The models are in the parent folder along with their cluster features.

## Contents
	- [Setup](#setup)
	- [1. Mining Tweets and Pre-processing](1-mining-tweets-and-pre-processing)
	- [2. Training AI Model](2-training-ai-model)
	- [3. Streaming and Classifying Tweets live](3-streaming-and-classifying-tweets-live)

## Setup
1. Create `src/config.py` and copy in it all the content of [src/sample_config.py](src/sample_config.py) 
2. Get Twitter Developer Account related auth tokens and replace it in `config.py`

**NOTE** Without these, you can't mine or stream tweets!

3. Ensure you have `python 3.6.5` and `pip3`	
4. Create Virtual environment:
```
$ python -m venv venv
$ .\venv\Scripts\activate
```
5. Install libraries:
```
$ pip install -r requirements.txt
```

## 1. Mining Tweets and Pre-processing
Mining Tweets is not possible without the Twitter auth tokens.

For benefit of the checker, I have already added my datasets for Brexit in [data/brexit.txt](data/brexit.txt) and Corona in [data/corona.txt](data/corona.txt)

Should you like to test the functionality head to [src/step1_step1_twitter_scrapper.py](src/step1_twitter_scrapper.py)
- User inputs which topic (1 for Brexit / 2 for Coronavirus) to mine tweets on
- The filtering of tweets can be controlled from `src/config.py`'s `MINING_TOPIC` dictionary
- To understand more about how to filter for twitter refer [here](https://developer.twitter.com/en/docs/tweets/rules-and-filtering/guides/using-premium-operators)
- Tweets are "cleaned" i.e. removal of URLS, user mentions, RT characters, numbers, emojis and punctuations.
- Tweets are then written to a file. By default tweets are saved in [data/trial.txt](data/trial.txt)
- By default, 250 tweets for a topic will be mined.

**NOTE 1: Beware that for very niche topics, twitter might not have enough tweets, and then it would keep printing the same tweets again**

**NOTE 2: Beware of Twitter's rate limits. Using Tweepy, the code makes frequent pauses to prevent reaching rate limuts**

## 2. Training AI Model
4 AI Algorithms can be trained:
* K-Means - [src/step2_kmeans.py](src/step2_kmeans.py)
* Agglomerative Clustering - [src/step2_agglomerativeClustering.py](src/step2_agglomerativeClustering.py)
* DBSCAN - [src/step2_dbscan.py](step2_dbscan)
* Gaussian Mixture Models - [src/step2_gaussianMixtures.py](src/step2_gaussianMixtures.py)

I have included all models in src/other_models folder. It is a pickle file containing the AI model, the tf-idf vectorizer object, the pca object (for dimension reduction) and the number of clusters.


Each script does the following:
1. Ask user to input a topic number 1 for Brexit / 2 for Coronavirus)
2. Ask user the number of dimensions to reduce the dataset into
**NOTE - Only with K-Means can you perform the AI without dimension reduction. The reason is explaiend in my Thesis**
3. Perform TF-IDF Vectorization on the cleaned data
4. Perform Dimensionality Reduction (if user chose this option).
5. Plot relevant graphs to estimate paramters
	- for K-Means: elbow method to estimate optimal number of clusters
	- for DBSCAN: to determing eps value (the "knee" of the graph)
	- for GMM: Determine the covariance type and the number of clusters.
6. Wait on user input on the parameters
7. Train model and show relevnt information (e.g. cluster features for K-Means, model visualization etc.)
8. Save model to a pickle file so it can be retrieved later. 

**NOTE on Agglomerative Clustering** - Here no estimation is necessary. The code automatically determines the right parameters

**NOTE ON GMM:** First graph is plotted to show how BIC score changes across clusters and different covariance type. 

If BIC goes on reducing (which it does for both Corona and Brexit 2D and 3D dataset), then it's gradient is plotted. 

User has to choose the covariance type with the overall lowerst BIC. This is usually "full"

## 3. Streaming and Classifying Tweets live

[src/step3_event_catcher.py](src/step3_event_catcher.py)

As explained in my thesis, K-Means allDimension dataset (i.e. no dimension reduction) was best for both Corona and Brexit topics.

I have included the pickle files of these models in the parent directory for benefit of the user.

The files are also mentioned in the `src/config.py`'s `FINAL_MODEL` dictionary

You WILL need Twitter Auth tokens to stream.

1. Asks user input for tweet topic
2. Asks user for how many tweets to stream. It is recommended to limit this to 30 for brexit (because there aren't that many tweets) and upto 150 for Corona.

The filtering for tweets is controlled in `src/config.py`'s `STREAMING_TRACK` dictionary.

After the number of tweets (defined in prev step), a bar chart will be displayed showing what tweets belong to which clusters and the cluster features will be displayed as a subplot.



utility script to save data
HIGHLY RECOMMEND LOADING IT IN UTILS/LOADCLEANED...DATA


CONFIG.PY CONVENTION


FILENAME CONVENTION

Store .pkl file in this order: vec, pca, model, n_cluster. Even if pca not done, store NONE.


### FUTURE STUFF
* Try cosine distances
* try other dimension reduction methods / kitne dimensions
* try miniBatch
* phrases like boris and johnson should be treated as one.
* remove things like "bbc", "via" etc....
* try optics instead of dbscan