# Exercise 2 : Parsing Dates
from learntools.core import binder
binder.bind(globals())
from learntools.data_cleaning.ex3 import *
import pandas as pd
import numpy as np
import seaborn as sns
import datetime
print("Setup Complete")

earthquakes = pd.read_csv("../input/earthquake-database/database.csv")
np.random.seed(0)

## 1) Check the data type of our date column
## You'll be working with the "Date" column from the earthquakes dataframe. Investigate this column now: does it look like it contains dates? What is the dtype of the column?

## Answer:
earthquakes['Date'].head()

## 2) Convert our date columns to datetime
## Most of the entries in the "Date" column follow the same format: "month/day/four-digit year". However, the entry at index 3378 follows a completely different pattern. Run the code cell below to see this.
earthquakes[3378:3383]
date_lengths = earthquakes.Date.str.len()
date_lengths.value_counts()
indices = np.where([date_lengths == 24])[1]
print('Indices with corrupted data:', indices)
earthquakes.loc[indices]

## Answer:
earthquakes.loc[3378, "Date"] = "02/23/1975"
earthquakes.loc[7512, "Date"] = "04/28/1985"
earthquakes.loc[20650, "Date"] = "03/13/2011"
earthquakes['date_parsed'] = pd.to_datetime(earthquakes['Date'], format="%m/%d/%Y")

## 3) Select the day of the month
## Create a Pandas Series day_of_month_earthquakes containing the day of the month from the "date_parsed" column.

## Answer:
day_of_month_earthquakes = earthquakes['date_parsed'].dt.day

## 4) Plot the day of the month to check the date parsing
## Plot the days of the month from your earthquake dataset.

## Answer:
day_of_month_earthquakes = day_of_month_earthquakes.dropna()
sns.distplot(day_of_month_earthquakes, kde=False, bins=31)
