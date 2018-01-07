from sklearn import preprocessing
import json
import math
import numpy as np
import pandas as pd
import random
import requests
import os


def get_act_pop_avg():
    """get average poplularity rating for actos by sampling through page numbers
    Warning:
    sampling of page numbers are random with 20 numbers ranges from 1 to 1000
    Input:
    None needed
    Output:
    average actor popularity based on samping
    """

    # Setting up query and list
    query_ave = "https://api.themoviedb.org/3/person/popular?" \
        "api_key=60027f35df522f00e57a79b9d3568423&language=en-US&page=%d"
    rd = random.sample(range(1, 1000), 20)
    rd_pop = []

    # For loop to call api based on page numbers sampled above and return
    # popularity
    for n in rd:
        rq = requests.get(query_ave % n).json()
        for item in rq['results']:
            rd_pop.append(item['popularity'])

    # compute average popularity
    ave_pop = np.mean(rd_pop)
    return ave_pop


def clean_director_actor():
    """add director_actor popularity rating to user generated csv
    Warning:
    This assumes call_data() from get_data module has been ran
    and data_raw_user.csv has been generated
    Input:
    None needed
    Output:
    cleaned data frame ready for user analysis
    """
    # ave_pop is average popularity the dev team got by running get_act_pop_avg
    # dev team assume no need to run again to get new ave_pop
    ave_pop = 2.08979
    TMDB_KEY = '60027f35df522f00e57a79b9d3568423'
    path = os.getcwd()
    df = pd.read_csv(path + '/data/data_raw_user.csv', encoding="latin1")
    Actors_split = []

    # split actor names
    for item in df['Actors']:
        item = str(item).split(",")
        Actors_split.append(item)

    # split director names
    Directors_split = []
    for item in df['Director']:
        item = str(item).split(",")
        Directors_split.append(item)

    # clear whitespace behind the name strings
    for item in Actors_split:
        for i in range(len(item)):
            item[i] = str(item[i]).strip()

    # clear whitespace behind the name strings
    for item in Directors_split:
        for i in range(len(item)):
            item[i] = str(item[i]).strip()

    Actor_Popularity = []
    count = 0
    # API calls to get specific actor popularity
    # by looking through actor names
    url = "https://api.themoviedb.org/3/search/person"
    for item in Actors_split:
        pop_sum = []
        for i in item:
            try:
                payload = {
                    'api_key': TMDB_KEY,
                    'query': i,
                    'language': 'en-US'}
                result = requests.get(url, data=payload).json()
                pop_sum.append(result['results'][0]['popularity'])
            except BaseException:
                pop_sum.append(ave_pop)
        Actor_Popularity.append(np.mean(pop_sum))
        count = count + 1
        print(count)
    df['actor_popularity'] = Actor_Popularity
    Director_Popularity = []
    # API calls to get specific director popularity
    # by looking through director names
    dir_count = 0

    for item in Directors_split:
        pop = []
        for i in item:
            try:
                payload = {
                    'api_key': TMDB_KEY,
                    'query': i,
                    'language': 'en-US'}
                result = requests.get(url, data=payload).json()
                pop.append(result['results'][0]['popularity'])
            except BaseException:
                pop.append(ave_pop)
        Director_Popularity.append(np.mean(pop))
        dir_count = dir_count + 1
        print(dir_count)

    df['director_popularity'] = Director_Popularity

    return df


def clean_regression_data():
    """preparing preloaded data for regression and visualizaiton
    Warning:
    This function directly calls data_clean.csv from data folder
    Do not remove this file!
    Input:
    None needed
    Output:
    Cleaned data frame ready for regression analysis
    and model building
    """

    path = os.getcwd()
    df = pd.read_csv(path + '/data/data_clean.csv', encoding="latin1")
    # drop unnecessary columns
    df = df.drop(["Unnamed: 0", "imdb_id", "Title", "X.x", "X.y", "Country",
                  "Actors", "Director", "Year", "Production"], axis=1)
    # drop_missing values
    mis_val_col = ["Genre", "IMDB.Votes", "Runtime", "IMDB.Rating", "Language"]
    for col in mis_val_col:
        df = df.drop(df[df[col].isnull()].index)
    # budget
    df["budget"] = df["budget"].map(lambda x: math.log10(x))
    # revenue
    df["revenue"] = df["revenue"].map(lambda x: math.log10(x))
    # genre
    df = pd.concat([df, df['Genre'].str.get_dummies(sep=', ')], axis=1)
    df['Thriller'] = df[['Thriller', 'Horror']].sum(axis=1)
    df['Fantasy'] = df[['Fantasy', 'Sci-Fi']].sum(axis=1)
    df['Other_genre'] = df[['Music', 'History', 'Sport', 'War', 'Western',
                            'Musical', 'Documentary', 'News']].sum(axis=1)
    df.drop(['Music', 'History', 'Sport', 'War', 'Western', 'Musical',
             'Documentary', 'News', 'Horror', 'Sci-Fi'], axis=1, inplace=True)
    genre_lst = list(df)[19:32]
    for x in genre_lst:
        df.loc[df['%s' % x] > 1, '%s' % x] = 1
    df = df.drop("Genre", axis=1)
    # IMDB.Votes
    df['IMDB.Votes'] = df['IMDB.Votes'].replace(',', '', regex=True)
    df['IMDB.Votes'] = df['IMDB.Votes'].astype(int)
    df["IMDB.Votes"] = df["IMDB.Votes"].map(lambda x: math.log10(x))
    # language
    df['Language'] = df.Language.str.count(',') + 1
    # rated
    df["Rated"] = df["Rated"].replace(np.nan, "UNRATED")\
        .replace("NOT RATED", "UNRATED")
    df = df.drop(df[(df["Rated"] == "TV-MA") | (df["Rated"] == "TV-PG") |
                    (df["Rated"] == "TV-14")].index)
    df = pd.concat([df, df['Rated'].str.get_dummies(sep=', ')], axis=1)
    # released
    # index of released date col
    index = df.columns.get_loc("Released")
    # change date data to timestamp
    release_dates = pd.to_datetime(df["Released"])
    # released date is weekend of not
    weekend_list = []
    for each in release_dates:
        day_ofweek = each.dayofweek
        if day_ofweek >= 4 and day_ofweek <= 6:
            tag = 1
        else:
            tag = 0
        weekend_list.append(tag)
    # released date is on dump months
    undumpmonth_list = []
    for each in release_dates:
        month = each.month
        if month == 12 or month == 1 or month == 2 or month == 8 or month == 9:

            tag = 0
        else:
            tag = 1
        undumpmonth_list.append(tag)
    df.insert(loc=index + 1, column="released_on_weekend", value=weekend_list)
    df.insert(loc=index + 2, column="released_not_on_dump_month",
              value=undumpmonth_list)
    df.drop("Released", axis=1)
    # runtime
    df["Runtime"] = df["Runtime"].map(lambda x: int(x.strip("min")))
    # normalization
    x1 = df[['IMDB.Rating', 'IMDB.Votes', 'Language', 'Runtime',
             'budget', 'actor_popularity', 'director_popularity']]
    x2 = df[['released_on_weekend',
             'released_not_on_dump_month',
             'Action',
             'Adventure',
             'Animation',
             'Biography',
             'Comedy',
             'Crime',
             'Drama',
             'Family',
             'Fantasy',
             'Mystery',
             'Romance',
             'Thriller',
             'Other_genre',
             'G',
             'NC-17',
             'PG',
             'PG-13',
             'R',
             'UNRATED']]
    y = df['revenue'].reset_index().drop("index", axis=1)
    normalizer = preprocessing.MinMaxScaler()
    x1 = normalizer.fit_transform(x1)
    x1 = pd.DataFrame(
        x1,
        columns=[
            'IMDB.Rating',
            'IMDB.Votes',
            'Language',
            'Runtime',
            'budget',
            'actor_popularity',
            'director_popularity'])
    x2 = x2.reset_index().drop("index", axis=1)
    X = pd.concat([x1, x2], axis=1)
    df_for_model = pd.concat([X, y], axis=1)
    path = os.getcwd()
    df_for_model.to_csv(path + '/data/data_for_lr.csv', encoding="latin1")
    return df_for_model
