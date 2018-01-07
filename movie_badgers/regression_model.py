from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_absolute_error, mean_squared_error,\
     r2_score
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.tree import DecisionTreeRegressor
import pandas as pd
import pickle


def model_evaluation(model_name, df, n_fold):
    """evaluate regression model using k-fold cross validation.
    Warning:
    4 models avaliable(linear regression, lasso, ridge, decision tree)
    Input:
    model_name: 4 name avaliable("linear", "lasso", "ridge", "tree")
    df: dataframe
    n_fold: # of folds to split df
    Output:
    base model
    """
    X = df.drop("revenue", axis=1)
    y = df["revenue"]
    if model_name == "linear":
        model = LinearRegression()
    elif model_name == "tree":
        model = DecisionTreeRegressor(max_depth=4)
    elif model_name == "ridge":
        model = Ridge(alpha=0.0001)
    elif model_name == "lasso":
        model = Lasso(alpha=0.0001)
    else:
        raise NameError("Please enter a proper model name")
    print("(Regression Model: ", model_name)
    mae = -cross_val_score(model, X, y, scoring="neg_mean_absolute_error",
                           cv=n_fold)
    mse = -cross_val_score(model, X, y, scoring="neg_mean_squared_error",
                           cv=n_fold)
    rsme = mse ** (1/2)
    r2_score = cross_val_score(model, X, y, scoring="r2", cv=n_fold)
    predictions = cross_val_predict(model, X, y, cv=n_fold)
    print("Average Cross Validation Score (Mean Absolute Error): ", mae.mean())
    print("Average Cross Validation Score (Root Mean Squared Error): ",
          rsme.mean())
    print("Average Cross Validation Score (R^2): ", r2_score.mean())
    model.fit(X, y)
    return model


def save_model(model, file_name, path):
    """save regression model to local machine as .pkl
    Input:
    model: base model, output of model_evaluation()
    new_model: string type, new model name
    path: path the user wants to save the model
    Output:
    "model save complete!"
    """
    with open(path, "wb") as file_name:
        pickle.dump(model, file_name)
    return "model save complete!"
