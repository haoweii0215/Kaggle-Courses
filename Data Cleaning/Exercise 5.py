# Exercise 5 : police_killings.to_csv("my_file.csv")
from learntools.core import binder
binder.bind(globals())
from learntools.data_cleaning.ex5 import *
import pandas as pd
import numpy as np
import fuzzywuzzy
from fuzzywuzzy import process
import chardet
print("Setup Complete")

## read in all our data
professors = pd.read_csv("../input/pakistan-intellectual-capital/pakistan_intellectual_capital.csv")
np.random.seed(0)

## convert to lower case
professors['Country'] = professors['Country'].str.lower()
## remove trailing white spaces
professors['Country'] = professors['Country'].str.strip()

## get the top 10 closest matches to "south korea"
countries = professors['Country'].unique()
matches = fuzzywuzzy.process.extract("south korea", countries, limit=10, scorer=fuzzywuzzy.fuzz.token_sort_ratio)

def replace_matches_in_column(df, column, string_to_match, min_ratio=47):
    ## get a list of unique strings
    strings = df[column].unique()

    ## get the top 10 closest matches to our input string
    matches = fuzzywuzzy.process.extract(string_to_match, strings,
                                         limit=10, scorer=fuzzywuzzy.fuzz.token_sort_ratio)

    ## only get matches with a ratio > 90
    close_matches = [matches[0] for matches in matches if matches[1] >= min_ratio]

    ## get the rows of all the close matches in our dataframe
    rows_with_matches = df[column].isin(close_matches)

    ## replace all rows with close matches with the input matches
    df.loc[rows_with_matches, column] = string_to_match

    ## let us know the function's done
    print("All done!")

replace_matches_in_column(df=professors, column='Country', string_to_match="south korea")
countries = professors['Country'].unique()

## 1) Examine another column
## Write code below to take a look at all the unique values in the "Graduated from" column.

## Answer:
unis = professors['Graduated from'].unique()

## 2) Do some text pre-processing
## Convert every entry in the "Graduated from" column in the professors DataFrame to remove white spaces at the beginning and end of cells.

## Answer:
professors['Graduated from'] = professors['Graduated from'].str.strip()

## 3) Continue working with countries
## In the tutorial, we focused on cleaning up inconsistencies in the "Country" column. Run the code cell below to view the list of unique values that we ended with.
countries = professors['Country'].unique()
countries.sort()
countries

## Answer:
matches = fuzzywuzzy.process.extract("usa", countries, limit=10, scorer=fuzzywuzzy.fuzz.token_sort_ratio)
replace_matches_in_column(df=professors, column='Country', string_to_match="usa", min_ratio=70)