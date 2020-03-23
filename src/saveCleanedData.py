from utils import saveData

topic = 1
num_dimensions = 2
file_name = "data/brexit_cleaned_2d"
saveData(topic, num_dimensions, file_name)

topic = 1
num_dimensions = 3
file_name = "data/brexit_cleaned_3d"
saveData(topic, num_dimensions, file_name)

topic = 2
num_dimensions = 2
file_name = "data/corona_cleaned_2d"
saveData(topic, num_dimensions, file_name)

topic = 2
num_dimensions = 3
file_name = "data/corona_cleaned_3d"
saveData(topic, num_dimensions, file_name)
