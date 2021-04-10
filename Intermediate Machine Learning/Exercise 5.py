# Exercise 5 : Cross-Validation

## Set up code checking
import os
if not os.path.exists("../input/train.csv"):
    os.symlink("../input/home-data-for-ml-course/train.csv", "../input/train.csv")
    os.symlink("../input/home-data-for-ml-course/test.csv", "../input/test.csv")
from learntools.core import binder
binder.bind(globals())
from learntools.ml_intermediate.ex5 import *
print("Setup Complete")

import pandas as pd
from sklearn.model_selection import train_test_split

## Read the data
train_data = pd.read_csv('../input/train.csv', index_col='Id')
test_data = pd.read_csv('../input/test.csv', index_col='Id')

## Remove rows with missing target, separate target from predictors
train_data.dropna(axis=0, subset=['SalePrice'], inplace=True)
y = train_data.SalePrice
train_data.drop(['SalePrice'], axis=1, inplace=True)

## Select numeric columns only
numeric_cols = [cname for cname in train_data.columns if train_data[cname].dtype in ['int64', 'float64']]
X = train_data[numeric_cols].copy()
X_test = test_data[numeric_cols].copy()

## Step 1: Write a useful function
## In this exercise, you'll use cross-validation to select parameters for a machine learning model.
## Begin by writing a function get_score() that reports the average (over three cross-validation folds) MAE of a machine learning pipeline that uses:
##    the data in X and y to create folds,
##    SimpleImputer() (with all parameters left as default) to replace missing values, and
##    RandomForestRegressor() (with random_state=0) to fit a random forest model.
## The n_estimators parameter supplied to get_score() is used when setting the number of trees in the random forest model.


## Answer:
def get_score(n_estimators):
    my_pipeline = Pipeline(steps=[
        ('preprocessor', SimpleImputer()),
        ('model', RandomForestRegressor(n_estimators, random_state=0))
    ])
    scores = -1 * cross_val_score(my_pipeline, X, y, cv=3, scoring='neg_mean_absolute_error')
    return scores.mean()

## Step 2: Test different parameter values
## Now, you will use the function that you defined in Step 1 to evaluate the model performance corresponding to eight different values for the number of trees in the random forest: 50, 100, 150, ..., 300, 350, 400.
## Store your results in a Python dictionary results, where results[i] is the average MAE returned by get_score(i).

## Answer:
results = {}
for i in range(1,9):
    results[50*i] = get_score(50*i)


## Step 3: Find the best parameter value
## Given the results, which value for n_estimators seems best for the random forest model? Use your answer to set the value of n_estimators_best.

## Answer:
n_estimators_best = min(results, key=results.get)