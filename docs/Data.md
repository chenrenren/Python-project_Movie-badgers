# Description of Data Used #


## Requirements ##

This project aims to predict movie box office. 

Movie Profit data: revenue, budget

Movie Characteristics: genre, release date, rating (R, PG13...), user ratings from IMBD, production company and popularity (number of votes). 

Directors/Actors data: director(s) popularity, actors/actresses popularity


## Sources ##

There are two datasets for this project. **TMDB**includes the budget, revenue and specific imdb id numbers of movies. **OMDB** contains details of movies, including genre, directors, actors, release season, rating, user average ratings and popularity (number of votes).  The two datasets will be linked through **imdb id** which is available on both datasets as unique identifier.

1. [TMDB](https://www.themoviedb.org/?language=en)
2. [OMDB](http://www.omdbapi.com/)

These two datasets can be accessed through API calls. They are free to use, but OMDB API has a constraint of 1,000 limits per day.

## Evaluation ##

|Requirements/Datasets|TMDB|OMDB|
|---|---|---|
|Movie Profit Info|:heavy_check_mark:||
|Basic Movie Info||:heavy_check_mark:|
|Movie Revenue Prediction|:heavy_check_mark:|:heavy_check_mark:|

Basic Movie Info: Contains the basic information of different movies.
e.g. genres, realeasing date etc.

Movie Profit Info: Contains revenue and budget of movies


