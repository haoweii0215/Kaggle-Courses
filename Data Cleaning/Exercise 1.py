# Exercise 1 : Handling Missing Values
from learntools.core import binder
binder.bind(globals())
from learntools.data_cleaning.ex1 import *
import pandas as pd
import numpy as np
print("Setup Complete")

## 1) Take a first look at the data
## Run the next code cell to load in the libraries and dataset you'll use to complete the exercise.
sf_permits = pd.read_csv("../input/building-permit-applications-data/Building_Permits.csv")
np.random.seed(0)

## Answer:
sf_permits.head()

## 2) How many missing data points do we have?
## What percentage of the values in the dataset are missing? Your answer should be a number between 0 and 100. (If 1/4 of the values in the dataset are missing, the answer is 25.)

## Answer:
missing_values_count = sf_permits.isnull().sum()
total_cells = np.product(sf_permits.shape)
total_missing = missing_values_count.sum()
percent_missing = (total_missing/total_cells) * 100

## 4) Drop missing values: rows
## If you removed all of the rows of sf_permits with missing values, how many rows are left?
## Note: Do not change the value of sf_permits when checking this.

## Answer:
sf_permits.dropna()

## 5) Drop missing values: columns
## Now try removing all the columns with empty values.
##    Create a new DataFrame called sf_permits_with_na_dropped that has all of the columns with empty values removed.
##    How many columns were removed from the original sf_permits DataFrame? Use this number to set the value of the dropped_columns variable below.

## Answer:
sf_permits_with_na_dropped = sf_permits.dropna(axis=1)
cols_in_original_dataset = sf_permits.shape[1]
cols_in_na_dropped = sf_permits_with_na_dropped.shape[1]
dropped_columns = cols_in_original_dataset - cols_in_na_dropped

## 6) Fill in missing values automatically
## Try replacing all the NaN's in the sf_permits data with the one that comes directly after it and then replacing any remaining NaN's with 0. Set the result to a new DataFrame sf_permits_with_na_imputed.

## Answer:
sf_permits_with_na_imputed = sf_permits.fillna(method='bfill', axis=0).fillna(0)