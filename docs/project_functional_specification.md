# Functional specification

## Problem Statements
The project is designed to predict revenue of movies for two types of users for theirs specific purposes. The users can be a movie-lover or those people who could be theater owner to set the screens in advance and professionals in media field who want to find some business insights from movies. 

## User profile
The computational environments the user should be familiar with are listed as:
* iPython Notebook
* GUI

User's knowledge of usage
* For movie-lovers/theater owners: The users are assumed to have less knowledge of the algorithm to use the GUI app.
* For researchers: Users should understand the models used in the prediction process and packages that used in the data visualization. 

## Elements of the problem statement
* How to access movie information data from websites through OMDB API and TMDB API.
* How to joint two databases of movies' information.
* How to categorize and clean the raw data with multi-attributes.
* How to conduct data analysis and visualization with Bokeh packages.
* How to predict a movie's revenue via different models(regression models/tree models) and compare the prediction results with real boxoffice.
* How to construct a graphic user interface.

## Use Case
* First section of GUI shows all the functions in the our packages, which includes data retrieval, data visualization and model prediction. Point-and-Click GUI on an app, go to the jupyter notebook. Get the data through API calls, clean the data and choose the scatterplot or boxplot see the correlation and distribution between two variables.   
* In second section, user can provide the attritubes of the movie(genre, director, releasing date etc.), using different models(regression/trees) to predict the boxoffice of a new movie based on the training dataset.


