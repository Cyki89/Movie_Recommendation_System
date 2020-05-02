####################################################################
#                                                       		   #
# 		Simple Movie Recomendation System Console Application 	   #
# (without any complex, unnecessary verification of input data!!!) #
# 		Follow the messages and everything should work fine   	   #
#                                                       		   #
####################################################################

from pyspark.sql import SparkSession
import numpy as np
import pickle
import os
import time
import inspect


####################################################################
####         	  Movie Recomendation System Class            	#### 
####################################################################

class RecommendationSystem():
    '''movie recomendation system'''
    
    def __init__(self, moviePairRdd, movieNameDict, totalRecommendations, singleRecommendation):
        self.moviePairRdd = moviePairRdd
        self.totalRecommendations = totalRecommendations
        self.singleRecommendation = singleRecommendation
        self.movieNameDict = movieNameDict
    
    def makeRecomendation(self, userRatings):
        '''driver function for recommendation'''
        
        # create list of similiraties for all user watched films
        movieSimScores, movieSimTypes, movieCoOccurences,\
        movieNames, movieRecomendedBy = self.createSimLists(userRatings)

        # sort lists by similiry score ratings
        sortedMovieSimScores, sortedMovieSimTypes, sortedMovieCoOccurences,\
        sortedMovieNames, sortedMovieRecomendedBy = self.sortSimLists(movieSimScores, movieSimTypes, 
                                                    movieCoOccurences, movieNames, movieRecomendedBy)
   
        # placeholder to control movie recomendations for user
        recommendations = []

        # iterate over all recomended film
        for name, simScore, simType, coOccurence, recomendedBy in zip(sortedMovieNames, 
                                                                      sortedMovieSimScores, 
                                                                      sortedMovieSimTypes,
                                                                      sortedMovieCoOccurences,
                                                                      sortedMovieRecomendedBy):
            # to avoid duplicates in recommendations
            if name not in recommendations:
                
                # show remomended films
                self.showRecommendation(len(recommendations)+1,
                                        name,
                                        recomendedBy,
                                        simScore,
                                        simType,
                                        coOccurence)
                
                recommendations.append(name)

                if len(recommendations) == self.totalRecommendations:
                    break
                    
                    
    def createSimLists(self, userRatings):
        '''create lists of movie similarities'''
        
        # create empty placeholders
        movieNames = []
        movieSimScores = []
        movieSimTypes = []
        movieCoOccurences =[]
        movieRecomendedBy = []
        
        # iterate over all user's watched film
        for movieId, rating in userRatings.items():
            # filter for movie pair contain user rated movie
            filteredMovies = self.moviePairRdd.filter(lambda x: (x[0][0] == movieId or x[0][1] == movieId) )

            # take only n best recommendation for each user movie
            recomendedMovies = filteredMovies.sortBy(lambda x: x[1][0], ascending = False)\
                                             .take(self.singleRecommendation)

            for recomendedMovie in recomendedMovies:
                
                movieKeys, simScores = recomendedMovie

                if movieId == movieKeys[0]:
                    similarMovieId = movieKeys[1]
                else:
                    similarMovieId = movieKeys[0]

                # don't recomend movies, that the user has already seen
                if similarMovieId not in userRatings.keys():
                    
                    # append similarity score multiple by user's rating for watched movie
                    movieSimScores.append(simScores[0]*rating)
                    # append category similarity
                    movieSimTypes.append(simScores[1])
                    # append movie coocurence
                    movieCoOccurences.append(simScores[2])
                    # append recomended movie name
                    movieNames.append(self.movieNameDict[similarMovieId])
                    # append user movie name thanks to whom this film was recommended
                    movieRecomendedBy.append(self.movieNameDict[movieId])
            
        return movieSimScores, movieSimTypes, movieCoOccurences, movieNames, movieRecomendedBy
        
        
    def sortSimLists(self, movieSimScores, movieSimTypes, movieCoOccurences,
                     movieNames, movieRecomendedBy):
        '''sort lists by similiry score ratings'''
        
        # reverse sort recomended movies by similarity score            
        movieSimScores = np.array(movieSimScores)
        idx = np.argsort(movieSimScores)[::-1]

        # reorder items in placeholders using numpy array properties
        movieSimScores = movieSimScores[idx]     
        movieSimTypes = np.array(movieSimTypes)[idx] 
        movieCoOccurences = np.array(movieCoOccurences)[idx] 
        movieNames = np.array(movieNames)[idx]
        movieRecomendedBy = np.array(movieRecomendedBy)[idx] 
        
        # convert back to lists
        return list(movieSimScores), list(movieSimTypes), list(movieCoOccurences),\
               list(movieNames), list(movieRecomendedBy)

            
    def showRecommendation(self, counter, movieName, recomendedMovieName, 
                           movieSimScore, movieSimType, movieCoOccurence):
        ''' show single movie recomendation'''

        print(f'Recomended Movie #{counter}',
              f'Title: {movieName}',
              f'Similarity Score: {round(movieSimScore,4)}',
              f'Similarity Types: {round(movieSimType,4)}', 
              f'Cooccurence: {movieCoOccurence}',
              f'Recommended by: {recomendedMovieName}',
              '-'*75, sep='\n')


####################################################################
####       Movie Recomendation System Interface Functions       #### 
####################################################################

def mainMenu():
	'''interface management function'''
	while True:
		showMainMenu()
		userInput = input()
		menuFunctions = {
		 '1' : showAvailableMovies,
		 '2' : showRatedMovies,
		 '3' : addMovies,
		 '4' : alterMovieRatings,
		 '5' : removeIndividualRating,
		 '6' : removeAllRatings,
		 '7' : makeRecomendation,
		 '8' : exit
		}
		try:
			menuFunctions[userInput]()
		except KeyError:		
			print('Wrong Key! Please try again', 
				  'Choose a number from 1 to 7 to select the appropriate action',
				  sep='\n')
			return mainMenu()


def showMainMenu():
	'''show main menu'''
	os.system('clear')
	print(f'Welcome to Movie Recommendation System')
	print('-'*75)
	print('Select action:')
	print('1. Show all available movies to rating')
	print('2. Show movies rated so far')
	print('3. Add movie ratings')
	print('4. Alter movie ratings')
	print('5. Remove individual movie ratings')
	print('6. Remove all movie ratings')
	print('7. Show movie recommendations for your preferences')
	print('8. Exit program')
	print('-'*75)


def showAvailableMovies():
	'''print list of available movies to rate'''
	os.system('clear')
	print('All available movies to rating:')
	print('-'*75)
	for movieId, movieName in MOVIE_LIST:
		print(f'Movie_id: {movieId:<8} Title: {movieName}')
	print('-'*75)
	return backToMainMenu(checkpoint=True)


def showRatedMovies():
	'''print list of rated movies so far'''
	os.system('clear')
	if not USER_RATINGS:
		print('Your movie ratings are empty!')
		print('In Main Menu press 3 to add movie ratings')
	else:
		print('Rated movie(s) so far:')
		print('-'*75)
		for movieId, rating in USER_RATINGS.items():
			print(f'Movie Id: {movieId:} Title:{MOVIE_NAME_DICT[movieId]} Rating: {rating} stars')
		print('-'*75)
	if inspect.stack()[1][3] not in ['removeIndividualRating', 'removeAllRatings', 'alterMovieRatings']:
		return backToMainMenu(checkpoint=True)


def addMovies():
	'''add movie ratings'''
	os.system('clear')
	found = False
	userInput = input('Enter the movie name or phase, that you are looking for: ') 
	print('Search Results:')
	print('-'*75)
	for movieId, movieName in MOVIE_LIST:
		if userInput.lower() in movieName.lower():
			found = True
			print(f'Movie_id: {movieId:<8} Title: {movieName}')
	print('-'*75)
	if found:
		userInput = input('Do you want to rate any of these films? [Y/N] ')
		if userInput.lower() == 'y':
			return rateMovies()
		else:
			userInput = input('Do you want to search for the movie(s) again [Y/N] ')
			if userInput.lower() == 'y':
				return addMovies()
		return backToMainMenu()
	else:
		print('No movie found matching the criteria...')
		userInput = input('Do you want to search for the movie(s) again [Y/N] ')
		if userInput.lower() == 'y':
			return addMovies()
		else:
			return backToMainMenu()


def rateMovies():
	'''rate movies'''
	movieId = int(input('Enter a movie ID: '))
	if movieId not in MOVIE_NAME_DICT.keys():
		print('Wrong movie ID, press 1 in main menu to see all available movies to rate')
		return backToMainMenu(checkpoint=True)
	rating = float(input('Enter a rating for this film from 1 to 5: '))
	print(f'You rated movie: {MOVIE_NAME_DICT[int(movieId)]} on {rating} stars')
	userInput1 = input('Do you confirm this rating? Press [Y/N]: ')
	if userInput1.lower() == 'y':
			USER_RATINGS[movieId] = rating
	userInput2 = input('Do you want to rate another movie(s) of this list? [Y/N] ')
	if userInput2.lower() == 'y':
		return rateMovies()
	userInput3 = input('Do you want to search for the movie(s) again [Y/N] ')
	if userInput3.lower() == 'y':
		return addMovies()
	else:
		return backToMainMenu()


def alterMovieRatings():
	'''change movie ratings'''
	os.system('clear')
	if not USER_RATINGS:
		print('Your movie ratings are empty!')
		print('In Main Menu press 3 to add movie ratings')
		return backToMainMenu(checkpoint=True)
	showRatedMovies()
	movieId = int(input('Enter the ID of the movie you want to alter: '))
	if movieId not in USER_RATINGS.keys():
		print('No found movie of entered ID in you ratings, enter correct movie ID')
	else:
		newRating = float(input(f'Enter the new rating for the movie: "{MOVIE_NAME_DICT[movieId]}" '))
		userInput = input( (f'Do you confirm changing rating from {USER_RATINGS[movieId]} '
		 					f'to {newRating} stars for this movie ? [Y/N] ') )
		if userInput.lower() == 'y':
			USER_RATINGS[movieId] = newRating 
			print('The rating has been successfully changed')
	userInput = input('Do you want to change another movie rating? [Y/N] ')
	if userInput.lower() == 'y':
		return alterMovieRatings()
	return backToMainMenu()


def removeIndividualRating():
	'''remove inditidual movie ratings'''
	os.system('clear')
	if not USER_RATINGS:
		print('Your movie ratings are empty!')
		print('In Main Menu press 3 to add movie ratings')
		return backToMainMenu(checkpoint=True)
	showRatedMovies()
	movieId = int(input('Enter the ID of the movie you want to remove: '))
	if movieId not in USER_RATINGS.keys():
		print('No found movie of entered ID in you ratings, enter correct movie ID')
	else:
		userInput = input(f'Do you confirm removing rating for the movie "{MOVIE_NAME_DICT[movieId]}"? [Y/N] ')
		if userInput.lower() == 'y':
			del USER_RATINGS[movieId]
			print('The rating has been successfully removed')
	userInput = input('Do you want to remove another movie rating? [Y/N] ')
	if userInput.lower() == 'y':
		return removeIndividualRating()
	return backToMainMenu()


def removeAllRatings():
	'''remove all movie ratings'''
	os.system('clear')
	if not USER_RATINGS:
		print('Your movie ratings are empty!')
		print('In Main Menu press 3 to add movie ratings')
		return backToMainMenu(checkpoint=True)
	showRatedMovies()
	userInput = input('Do you confirm removing all ratings? [Y/N] ')
	if userInput.lower() == 'y':
		print('Removing all ratings ...')
		time.sleep(1)
		USER_RATINGS.clear()
	return backToMainMenu()


def backToMainMenu(checkpoint=False):
	'''function to reduce the repetitive amount of code '''
	if checkpoint:
		input('Press any key to continue...')
	print('Back to Main Menu ...')
	time.sleep(1)
	return mainMenu()


def makeRecomendation():
	'''make recommendation based on user's preferences'''
	os.system('clear')
	if not USER_RATINGS:
		print('Your movie ratings are empty!')
		print('In Main Menu press 3 to add movie ratings')
		input('Press any button to continue ...')
		return backToMainMenu()
	print('Recommendation Results:')
	print('-'*75)
	RS.makeRecomendation(USER_RATINGS)
	return backToMainMenu(checkpoint=True)


##################################################################
####                      Main Program                        #### 
##################################################################

if __name__ == '__main__':
	
	# start spark session
	spark = SparkSession.builder.appName('my_app').master("local[*]").getOrCreate()

	# list of all available movies to rate (global variable)
	with open('movieList.pickle', 'rb') as f:
		MOVIE_LIST = pickle.load(f)

	# create lookup table for available movie names (global variable)
	MOVIE_NAME_DICT = {int(movieId): movieName for movieId, movieName in MOVIE_LIST}

	# movie pair similarities RDD
	moviePairSimilaritiesRdd = spark.sparkContext.pickleFile('MoviePairSimilarities')

	# dict for user rating (global variable)
	USER_RATINGS = {}

	# instance of movie recommendation system (global instance)
	RS = RecommendationSystem(moviePairSimilaritiesRdd, 
							  MOVIE_NAME_DICT, 
							  totalRecommendations=10, 
							  singleRecommendation=5)

	# run interface management function
	mainMenu()

	# stop spark session
	spark.stop()
