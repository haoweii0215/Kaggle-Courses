# Exercise 7 : Data Leakage

## Set up code checking
from learntools.core import binder
binder.bind(globals())
from learntools.ml_intermediate.ex7 import *
print("Setup Complete")

## Step 5: Housing Prices
## You will build a model to predict housing prices. The model will be deployed on an ongoing basis, to predict the price of a new house when a description is added to a website. Here are four features that could be used as predictors.
##    Size of the house (in square meters)
##    Average sales price of homes in the same neighborhood
##    Latitude and longitude of the house
##    Whether the house has a basement
## You have historic data to train and validate the model.
## Which of the features is most likely to be a source of leakage?

## Answer:
potential_leakage_feature = 2