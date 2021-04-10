# Exercise 3 : Categorical Variables

## Set up code checking
import os
if not os.path.exists("../input/train.csv"):
    os.symlink("../input/home-data-for-ml-course/train.csv", "../input/train.csv")
    os.symlink("../input/home-data-for-ml-course/test.csv", "../input/test.csv")
from learntools.core import binder
binder.bind(globals())
from learntools.ml_intermediate.ex3 import *
print("Setup Complete")

import pandas as pd
from sklearn.model_selection import train_test_split

## Read the data
X = pd.read_csv('../input/train.csv', index_col='Id')
X_test = pd.read_csv('../input/test.csv', index_col='Id')

## Remove rows with missing target, separate target from predictors
X.dropna(axis=0, subset=['SalePrice'], inplace=True)
y = X.SalePrice
X.drop(['SalePrice'], axis=1, inplace=True)

## To keep things simple, we'll drop columns with missing values
cols_with_missing = [col for col in X.columns if X[col].isnull().any()]
X.drop(cols_with_missing, axis=1, inplace=True)
X_test.drop(cols_with_missing, axis=1, inplace=True)

## Break off validation set from training data
X_train, X_valid, y_train, y_valid = train_test_split(X, y,
                                                      train_size=0.8, test_size=0.2,
                                                      random_state=0)

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

## function for comparing different approaches
def score_dataset(X_train, X_valid, y_train, y_valid):
    model = RandomForestRegressor(n_estimators=100, random_state=0)
    model.fit(X_train, y_train)
    preds = model.predict(X_valid)
    return mean_absolute_error(y_valid, preds)

## Step 1: Drop columns with categorical data
## You'll get started with the most straightforward approach. Use the code cell below to preprocess the data in X_train and X_valid to remove columns with categorical data. Set the preprocessed DataFrames to drop_X_train and drop_X_valid, respectively.

## Answer:
drop_X_train = X_train.select_dtypes(exclude=['object'])
drop_X_valid = X_valid.select_dtypes(exclude=['object'])

## Step 2: Label encoding
## Part B :
## Use the next code cell to label encode the data in X_train and X_valid. Set the preprocessed DataFrames to label_X_train and label_X_valid, respectively.
##    We have provided code below to drop the categorical columns in bad_label_cols from the dataset.
##    You should label encode the categorical columns in good_label_cols.

## Answer:
label_encoder = LabelEncoder()
for col in set(good_label_cols):
    label_X_train[col] = label_encoder.fit_transform(X_train[col])
    label_X_valid[col] = label_encoder.transform(X_valid[col])

## Step 3: Investigating cardinality
## Part A :
## The output above shows, for each column with categorical data, the number of unique values in the column. For instance, the 'Street' column in the training data has two unique values: 'Grvl' and 'Pave', corresponding to a gravel road and a paved road, respectively.
## We refer to the number of unique entries of a categorical variable as the cardinality of that categorical variable. For instance, the 'Street' variable has cardinality 2.
## Use the output above to answer the questions below.

## Answer:
high_cardinality_numcols = 3
num_cols_neighborhood = 25

## Part B :
## For large datasets with many rows, one-hot encoding can greatly expand the size of the dataset. For this reason, we typically will only one-hot encode columns with relatively low cardinality. Then, high cardinality columns can either be dropped from the dataset, or we can use label encoding.
## As an example, consider a dataset with 10,000 rows, and containing one categorical column with 100 unique entries.
##    If this column is replaced with the corresponding one-hot encoding, how many entries are added to the dataset?
##    If we instead replace the column with the label encoding, how many entries are added?
## Use your answers to fill in the lines below.

## Answer:
OH_entries_added = 1e4*100 - 1e4
label_entries_added = 0

## Step 4: One-hot encoding
## Use the next code cell to one-hot encode the data in X_train and X_valid. Set the preprocessed DataFrames to OH_X_train and OH_X_valid, respectively.
##    The full list of categorical columns in the dataset can be found in the Python list object_cols.
##    You should only one-hot encode the categorical columns in low_cardinality_cols. All other categorical columns should be dropped from the dataset.

## Answer:
from sklearn.preprocessing import OneHotEncoder
OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
OH_cols_train = pd.DataFrame(OH_encoder.fit_transform(X_train[low_cardinality_cols]))
OH_cols_valid = pd.DataFrame(OH_encoder.transform(X_valid[low_cardinality_cols]))

OH_cols_train.index = X_train.index
OH_cols_valid.index = X_valid.index

num_X_train = X_train.drop(object_cols, axis=1)
num_X_valid = X_valid.drop(object_cols, axis=1)

OH_X_train = pd.concat([num_X_train, OH_cols_train], axis=1)
OH_X_valid = pd.concat([num_X_valid, OH_cols_valid], axis=1)
