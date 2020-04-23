# Real-time Collective Event Stream Detection from Twitter Streams
create venv:
.\venv\Scripts\activate
.\venv\Scripts\deactivate



step 1 - frequent pausing to not abuse rate limits. hence only 5000 at a time.
recommended to use trracks with AN OR rather than just geneeral track!


utility script to save data
HIGHLY RECOMMEND LOADING IT IN UTILS/LOADCLEANED...DATA

in step 2 data = tf-idfed and removed stopword, urls, ....

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