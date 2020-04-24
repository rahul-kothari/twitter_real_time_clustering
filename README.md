# Real-time Collective Event Stream Detection from Twitter Streams

The idea of this project was to get tweets related to a topic in real-time and use unsupervised learning techniques to cluster them into various sub-topics to analyse the popular domains with respect to the trend. There were 5 unsupervised learning models used that were trained on the tweets after doing pre-processing, TF-IDF and dimensionality reduction (where necessary). These AI models have to be evaluated too to choose the best one. This part is manual and left for the user to determine.

The AI algorithms were:
* K-Means
* Agglomerative Clustering
* DBSCAN
* BIRCH
* Gaussian Mixture Models

All the above functionality already works for two trends: Brexit and Coronavirus and **can be extended to any number of topics**

* I have included the original dataset for Brexit and Coronavirus to help you get started and experiment. 

* I also included the 18 models I created and experimented with. They are in the `other_models` folder

* For both the trends, K-Means with no dimensionality reduction were the best models. The models are in the parent folder along with their cluster features.

* In the graphs folder, you shall find graphs related to the 4 AI algorithms and graphs produced on streaming. These graphs will be constructed upon running the appropriate scripts.

* As shown below, you need twitter auth tokens only for step 1 (mining) and step 3 (streaming). 

## Contents
- [Setup](#setup)
- [Getting Started](#getting-started)
	- [1. Mining Tweets and Pre-processing](1-mining-tweets-and-pre-processing)
	- [2a. Training AI Model](2a-training-ai-model)
	- [2b. Evaluate best model out of them all](#2b-evaluate-best-ai-model)
	- [3. Streaming and Classifying Tweets live](3-streaming-and-classifying-tweets-live)
- [Porject Convention and Contribution](#conventions-and-contribution)
- [Future Modifications Proposed](#future-modifications-proposed)

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
5. Install libraries (`Tweepy`, `NumPy`, `Scikit-Learn`, `Matplotlib` etc.):
```
$ pip install -r requirements.txt
```

## Getting Started
To add your own topics, just add it to the `enum` `Topic` in `src/config.py` for the script files to work seamlessly.

The next few headings contain instructions and notes about how to run each step. The project is divided into 3 parts
- [1. Mining Tweets for dataset generation and Pre-processing them](1-mining-tweets-and-pre-processing)
- [2a. Training AI Models on the cleaned dataset](2a-training-ai-model)
- [2b. Evaluate best model out of them all](#2b-evaluate-best-ai-model)
- [3. Streaming and Classifying Tweets in real-time](3-streaming-and-classifying-tweets-live)

### 1. Mining Tweets and Pre-processing
[src/step1_step1_twitter_scrapper.py](src/step1_twitter_scrapper.py)

Mining Tweets is not possible without the Twitter auth tokens.

For refereence, I have already added my datasets for Brexit in [data/brexit.txt](data/brexit.txt) and Corona in [data/corona.txt](data/corona.txt)

How the script works:
- User inputs which topic (1 for Brexit / 2 for Coronavirus) to mine tweets on
- The filtering of tweets can be controlled from `src/config.py`'s `MINING_TOPIC` dictionary
- To understand more about how to filter for twitter refer [here](https://developer.twitter.com/en/docs/tweets/rules-and-filtering/guides/using-premium-operators)
- Tweets are "cleaned" i.e. removal of URLS, user mentions, RT characters, numbers, emojis and punctuations. Refer `src/data_cleanup.py`'s `remove_urls_users_punctuations()` method
- After every 250 tweets, they are then written to a file. By default tweets are saved in [data/trial.txt](data/trial.txt). This can be controleld in `src/config.py`'s `DATA_FILE` dictionary.
- By default, 5000 tweets for a topic will be mined (if there are that many tweets).

**NOTE 1: Beware that for very niche topics, twitter might not have enough tweets, and then it would keep printing the same tweets again**
**NOTE 2: Beware of Twitter's rate limits. Using Tweepy, the code makes frequent pauses to prevent reaching rate limuts**

## 2a. Training AI Model
5 AI Algorithms can be trained:
* K-Means - [src/step2_kmeans.py](src/step2_kmeans.py)
* Agglomerative Clustering - [src/step2_agglomerativeClustering.py](src/step2_agglomerativeClustering.py)
* DBSCAN - [src/step2_dbscan.py](step2_dbscan)
* BIRCH - [src/step2_birch.py](src/step2_birch.py)
* GMM or Gaussian Mixture Models - [src/step2_gaussianMixtures.py](src/step2_gaussianMixtures.py)

I have included all models in src/other_models folder. It is a pickle file containing the AI model, the tf-idf vectorizer object, the pca object (for dimension reduction) and the number of clusters.


Each script does the following:
1. Ask user to input a topic number 1 for Brexit / 2 for Coronavirus)
2. Ask user the number of dimensions to reduce the dataset into
**NOTE - Only with K-Means can you perform the AI without dimension reduction. In rest all cases this is not recommended**
3. Perform TF-IDF Vectorization and stop words removal on the cleaned data
4. Perform Dimensionality Reduction (if user chose this option).
5. Plot relevant graphs to estimate paramters
	- for K-Means: elbow method to estimate optimal number of clusters
	- for DBSCAN: to determing eps value (the "knee" of the graph)
	- for BIRCH: 2 graphs - showing the impact of threshold with change in branching_factor and vice-versa.
	- for GMM: Determine the covariance type and the number of clusters.
6. Wait on user input on the parameters 
7. Train model and show relevnt information and graph visualization (e.g. cluster features for K-Means, model visualization etc.)
8. Save model to a pickle file so it can be retrieved later. 

**NOTE on Agglomerative Clustering** - point 6 is skipped. The code automatically determines the right parameters

**NOTE on GMM:** First graph is plotted to show how BIC score changes across clusters and different covariance type. User is asked if BIC goes on reducing (which it does for both Corona and Brexit 2D and 3D dataset). If so then it's gradient is plotted. User has to choose the covariance type with the overall lowerst BIC. This is usually "full".

**NOTE 3:** Certain files have other functionalities too. Like `kmeans.py` can show the circumference of the clusters formed. `agglomerative_clustering.py` can show the Dendrogram/Tree. `gmm.py` can show the ellipsis of the cluster.

Check out the graphs folder to see what graphs these scripts produce!

## 2b. Evaluate best AI Model
- Can use metrics like Silhouette score and BIC but they differ across models with different dimensions on the dataset.

- Best to look at the tweets in each cluster and see what they refer to, if they cover the diversity of the dataset and how much overlap they have.

2 utility scripts have also been added:
- **utilityScript-classifyWholeDatasetWithModel.py** - this requires the .pkl file of the model and the topic number. It then classifies the whole dataset using the model.
- **utilityScript-stream_multiple_models.py** - like step3, streams on twitter but plots sub-graphs showing how different AI models performed on the same tweets.

## 3. Streaming and Classifying Tweets live

[src/step3_event_catcher.py](src/step3_event_catcher.py)

K-Means allDimension dataset (i.e. no dimension reduction) was best for both Corona and Brexit topics. 

I have included the pickle files of these models in the parent directory for benefit of the user.

Once the final model is evaluated, 

You WILL need Twitter Auth tokens to stream.

1. Asks user input for tweet topic
2. Asks user for how many tweets to stream. It is recommended to limit this to 30 for brexit (because there aren't that many tweets) and upto 150 for Corona.
3. The filtering for tweets is controlled in `src/config.py`'s `STREAMING_TRACK` dictionary.
4. The tweets then are preprocessed (removing URLs, user mentions, punctuations, numbers etc.) followed by TF-IDF and dimensionality reduction if necessary.
5. The tweets is fed to the final model. The `.pkl` file for the final model must be mentioned in the `src/config.py`'s `FINAL_MODEL` dictionary
6. After the number of tweets (defined in point 2), a bar chart will be displayed showing what tweets belong to which clusters and the cluster features will be displayed as a subplot.

## Conventions and Contribution
* Please maintain the convention in `config.py`	to add dictionary with the `KEY` as the topic name used in the `Topic` enum.
* Storing .pkl files: the model files should contain the following in this order: vec, pca, model, n_cluster. If pca not done, store `None`.
* AI Model name convention - try to keep it similar to the naming in the `models` folder.

**I would love to see how you use this! Add on your topics, your final models and streaming graphs!**


## FUTURE MODIFICATIONS PROPOSED
* Try cosine distances instead of just euclidean
* try `K-Means MiniBatch` 
* Tokenize certain phrases like "boris johnson", "PM Johnson" as one. 
* remove things like "bbc", "via" etc in tweets.
* try optics instead of dbscan