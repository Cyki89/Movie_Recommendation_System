# Movie_Recommendation_System

## Overview
The goal of this project is to build <i>Movie Recommendation System</i> with <i>Spark</i> using item-based colaborative filtering method.

## Dependencies
* Python 3.7
* PySpark 2.4.5
* Numpy
* Matplotlib
* Seaborn

## Data
Data come from [https://grouplens.org/datasets/movielens/](https://grouplens.org/datasets/movielens/). I used <i>100K</i> movie ratings dataset from <i>2018</i> year.

## Scope of work
* Create RDD of movie similarities
* Set similarity thresholds for movie ratings, category and co occurrence
* Reduce RDD of movie similarities based on similarity thresholds
* Set the rules for the recommendation system
* Create test cases
* Evaluate the recommendation system based on test cases
* Discuss the results
* Create a Movie Recommendation System Console Application 

## Content
* <i>Movie_Recommendation_System_Notebook.ipynb</i> - notebook with calculations and descriptions
* <i>Movie_Recommendation_System_Notebook.py</i> - console application to run in the terminal
* <i>MoviePairSimilarities</i> - folder contains serialized movie pair similarities RDD
* <i>movieNameDict.pickle</i> - serialized lookup table of movie names
* <i>movieList.pickle</i> - serialized list of avaiable movie to rate in console application
* <i>extract_available_movies.py</i> - script to create list of available movies to rate
* <i>ml-latest-small</i> - folder contains datasets

## Example test and results 
<b>User ratings:</b>
- <i>Lord of the Rings: The Two Towers, The (2002)</i> - 5 stars
- <i>Kill Bill: Vol. 1 (2003)</i> - 5 stars
- <i>Harry Potter and the Chamber of Secrets (2002)</i> - 1 stars

<b>Recomendation:</b>
```
Recomended Movie #1
Title: Lord of the Rings: The Fellowship of the Ring, The (2001)
Similarity Score: 4.977
Similarity Types: 1.0
Cooccurence: 166
Recommended by: Lord of the Rings: The Two Towers, The (2002)
----------------------------------------------------------------------------------------------------
Recomended Movie #2
Title: Lord of the Rings: The Return of the King, The (2003)
Similarity Score: 4.9679
Similarity Types: 1.0
Cooccurence: 161
Recommended by: Lord of the Rings: The Two Towers, The (2002)
----------------------------------------------------------------------------------------------------
Recomended Movie #3
Title: Kill Bill: Vol. 2 (2004)
Similarity Score: 4.9676
Similarity Types: 0.6667
Cooccurence: 103
Recommended by: Kill Bill: Vol. 1 (2003)
----------------------------------------------------------------------------------------------------
Recomended Movie #4
Title: Army of Darkness (1993)
Similarity Score: 4.9421
Similarity Types: 0.2
Cooccurence: 23
Recommended by: Kill Bill: Vol. 1 (2003)
----------------------------------------------------------------------------------------------------
Recomended Movie #5
Title: Spirited Away (Sen to Chihiro no kamikakushi) (2001)
Similarity Score: 4.9276
Similarity Types: 0.3333
Cooccurence: 63
Recommended by: Lord of the Rings: The Two Towers, The (2002)
----------------------------------------------------------------------------------------------------
Recomended Movie #6
Title: Pulp Fiction (1994)
Similarity Score: 4.924
Similarity Types: 0.5
Cooccurence: 99
Recommended by: Kill Bill: Vol. 1 (2003)
----------------------------------------------------------------------------------------------------
Recomended Movie #7
Title: Who Framed Roger Rabbit? (1988)
Similarity Score: 4.9211
Similarity Types: 0.1429
Cooccurence: 39
Recommended by: Kill Bill: Vol. 1 (2003)
----------------------------------------------------------------------------------------------------
Recomended Movie #8
Title: Inglourious Basterds (2009)
Similarity Score: 4.9196
Similarity Types: 0.3333
Cooccurence: 56
Recommended by: Kill Bill: Vol. 1 (2003)
----------------------------------------------------------------------------------------------------
Recomended Movie #9
Title: Edward Scissorhands (1990)
Similarity Score: 4.9111
Similarity Types: 0.3333
Cooccurence: 52
Recommended by: Lord of the Rings: The Two Towers, The (2002)
----------------------------------------------------------------------------------------------------
Recomended Movie #10
Title: Toy Story 3 (2010)
Similarity Score: 4.8948
Similarity Types: 1.0
Cooccurence: 44
Recommended by: Lord of the Rings: The Two Towers, The (2002)
----------------------------------------------------------------------------------------------------
```
<b>Discussion of results:</b>
* As expected in recommended movies appear:
  - Movies from <i>the Lord of the Rings</i> saga
  - <i>Kill Bill: Vol. 2</i>
  - No movies from <i>Harry Potter</i> saga
* More <i>Quentin Tarantino</i> (director of <i>Kill Bill</i>) movies like: <i>Pulp Fiction</i> and <i>Inglourious Basterds</i>
* <i>Army of Darkness</i> - I personally do not know this movie but from the sample photos and opinions it results from it has a very similar atmosphere to <i>the Lord of the Rings</i>
* <i>Spirited Away</i> - Japanese anime in the atmosphere of magic and gods, very high marks and good reviews
* <i>Who Framed Roger Rabbit?</i> - anime in the atmosphere of <i>Kill Bill</i>
* <i>Toy Story 3</i> - belongs to the same categories like <i>the Lord of the Rings</i>: Adventure, Fantasy
* <i>Edward Scissorhands</i> - very good movie, but probably should not be on this list

