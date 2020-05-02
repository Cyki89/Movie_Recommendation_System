####################################################################
####  Helper script to create list of available movies to rate  #### 
####################################################################

from pyspark.sql import SparkSession
import numpy as np
import pickle

if __name__ == '__main__':
	spark = SparkSession.builder.appName('my_app').master("local[*]").getOrCreate()

	# load previously saved movie name dict
	with open('movieNameDict.pickle', 'rb') as f:
		movieNameDict = pickle.load(f)

	# load final movie pair similarities RDD
	moviePairSimilaritiesRdd = spark.sparkContext.pickleFile('MoviePairSimilarities')

	# extract movies id from RDD
	moviesId = moviePairSimilaritiesRdd.map(lambda x: x[0]).collect()

	# add movies id to the set
	moviesIdSet = set()
	for movie1, movie2 in moviesId:
		moviesIdSet.add(movie1)
		moviesIdSet.add(movie2)
	
	# create sorted list of tuple (movie id, movie name)
	movieList = sorted([(movieId, movieNameDict[movieId]) for movieId in moviesIdSet])

	# save movieList for future use
	with open('movieList.pickle', 'wb') as f:
	# pickle the 'models'using the highest protocol available.
		pickle.dump(movieList, f, pickle.HIGHEST_PROTOCOL)

	spark.stop()


