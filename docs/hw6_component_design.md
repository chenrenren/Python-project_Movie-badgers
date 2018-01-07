# Component Design


## Component list. 
- Get movie revenue and information and combine them
- Conduct missing value imputation, extract features
- Visualize features
- Built regression models, perform analsis and compare models
- Deploy analysis result to WebUI
- ...

## Component specifications. 
### Data collection
- Name: 
  get_revenue(), info_data(), combine()
- What it does: 
  This component is used to send requests to web API to collect the metadata. 
- Inputs: 
  get_revenue: API key of TMDB, Pages go through when movie is sorted by popularity. Info_data: movie_id list, the list contains all the movie with their IMDB id. combine: `.csv` files
- Outputs: 
  get_revenue: `.csv` file contain movie id, corresponding budget and revenue. Info_data: `.csv` file contain the other infomations of the movie collected (Actor, Director, Rating, Votes, Release date, etc.). combine: Combined `.csv` file
- How it works:
  First function in the component calls the API of TMDB to get the movie id, the budget and revenue of the most popular movies for the last decade. Info_data uses the movie id collected to collect the other infomations from OMDB API. combine function joints two dataset using the key column: movie id.

### Conduct Data Cleaning
- Name:
  clean_data() 
- What it does:  
  Clean the initial raw data. Categorize several multilevel variables into a more obvious formation that will work better in the model. Remove or compensate the missing value with average value based on different data types. 
- Inputs:   
  Actors(string|Categorical variable), Country(String|Categorical variable), Director(String|Categorical variable), Genre(String|Categorical variable), Language(Integer|Continuous variable), Production(String|Categorical variable), Released(Integer|Continuous variables)
- Outputs:   
  Dataframe of cleaned data that is ready to build the model and do the data visualization.
- How it works:   
  Extract the month of "Released date" and categorize it into "quarter" variable.   
  Form a new column to decide whether it is the weekdays/weekends based on "Released data".    
  Sort out the famous "Director" and rate it.    
  Categorize "Genre" into 10 main kinds of movies and design an algorithm to sort it.    
  Clean the variable "Production" in case of duplicate factors.     
  Deal with the missing value. If the NA appears in categorical data, remove it. Else, use the average value to compensate it.     

### Build Regression Models
* Functions: model_evaluation,save_model
* What it does:
      Using machine learning methods to build several models, make comparisons and save the models. 
* How it works:
      * Model_evaluation function is to run different types of models, i.e. linear regression, tree model, ridge, lasso model. Using k-fold cross validation to calculate. Compare the error and the accuracy of models between different methods. 
      * Save_model function is to save regression models to local machine as .pkl files.
* Inputs:
      * model_evaluation: model_name (linaer, ridge, lasso), dataset, number of fold for cross validation
      * save_model: model_name, file_name, path
* Outputs:
      * model_evaluation: established prediction model 
      * save_model:"model save complete!"

 
  
### Web UI
- Name:
get_movie_prediciton()
show_analysis()
- What it does:
Taking user inputs and parsing them using Python HTMLParser library and feed into according variables in predictive model.
UI will show static image of the team's analysis of movie trends.
- Inputs:
To call prediciton:
On the html based platform user will input in text or numbers format for:
"Top 3 Actors", "Director", "Genre", "num_languages", "Production", "Release Month", "Release day_of_week", "runtime and year" and "Rating"
To call analysis:
Simply click on "show analysis"
- Outputs:
Predicted voting (popularity) and revnue
Static image of the team's analysis of movie trends.
- How it works:
The UI is a simply web based form that users can input their assumed movie information and get a predicted revenue. The platform will take the information, send to HTMLParser (the team will build this function using this library), and feed intot eh predictive model mentioned above.
UI will show static image of the team's analysis of movie trends.
