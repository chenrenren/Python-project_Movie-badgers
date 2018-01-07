<p align="center">
  <img src="http://www.thesoobproductions.co.uk/wp-content/uploads/2012/10/movie-money-film-reel.ju_.09.jpg">
</p>

# Team Movie Badgers - Movie Revenue Prediction

## Collaborators:
Anna Huang, Jingyun Chen, Weichen Xu, Chen Ren, Junmeng Zhu

## Project description

The movie industry is huge income generator in the entertainment industry, there are many variables that contribute to how successful a movie is, but it's hard to understand how these variables work. 

This project aims to **predict movie box-office** based on genre, director(s), actor(s)/actress(es), release date, rating (R, PG13...), average user ratings from IMDB and popularity (number of votes).  

## Data source
There are two datasets used in this project. The first one **TMDB** includes the budget, revenue and specific imdb id numbers of movies. The second one **OMDB** dataset contains all the other information of the movies(such as release date,genre,imdb voting...).The two datasets will be linked through **imdb id** which is available on both datasets as unique identifier.
1. [TMDB](https://www.themoviedb.org/?language=en)
2. [OMDB](http://www.omdbapi.com/)

## Who can use movie badger?
1. Movie fans/ Theater Owner: User can input the features of a specific movie they want to get its future revenue in the user interface, select a regression model. Then the program presents its estimated revenue
2. Researchers: Researchers who are interested in movie revenue prediction can import the submodules for independent analysis, collect their own dataset based on self defined parameters, even select features to build model using visualization tools

## Before you start
To successfully use our program, you may need to have following environments/ libs:
1. Python 3.5
2. bokeh
3. scikit-learn

## User guidance
1. In a terminal(Mac)/cmd window(PC), navigate the the location you want to copy the `movie_badgers` package.
2. Clone the package by typing the following code in terminal:
```
git clone https://github.com/UWSEDS-aut17/uwseds-group-movie-badgers.git
```
3. Inside `uwseds-group-movie-badgers` directory, initiate the setup:
```
python setup.py install
```
4. Lauch the user interface by starting:
```
python ./movie_badgers/user_interface.py
```
5. (Optional) Researcher use: Windows user can open the demo of all the submodules through **user interface**. Mac user can open that **jupyter notebook** in following directory:
```
uwseds-group-movie-badgers/example
```
