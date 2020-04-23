#  Utility script to save the result after doing TF-IDF, PCA so not keep doing it several times
import pickle

from utils import getCleanedData, reduceDimensionality
from config import Topic


filename = input("Path where this cleaned processed data is stored in: ")
filenames = ["data/brexit_cleaned_2d", "data/brexit_cleaned_3d", 
            "data/corona_cleaned_2d", "data/corona_cleaned_2d"]
i=0
topics = [1,2]
dimensions = [2,3]
for topic in topics:
    for num_dimension in dimensions:
        X, vectorizer = getCleanedData(topic)
        X, pca = reduceDimensionality(X, num_dimensions)
        with open(filenames[i], 'wb') as f:
                pickle.dump([X, vectorizer, pca], f)
        print("data saved to ./",file_name)
        i+=1