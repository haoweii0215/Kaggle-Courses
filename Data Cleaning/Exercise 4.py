# Exercise 4 : Character Encodings
from learntools.core import binder
binder.bind(globals())
from learntools.data_cleaning.ex4 import *
import pandas as pd
import numpy as np
import chardet
np.random.seed(0)
print("Setup Complete")

## 1) What are encodings?
## You're working with a dataset composed of bytes. Run the code cell below to print a sample entry.
sample_entry = b'\xa7A\xa6n'
print(sample_entry)
print('data type:', type(sample_entry))

## Answer:
before = sample_entry.decode("big5-tw")
new_entry = before.encode()

## 2) Reading in files with encoding problems
## Use the code cell below to read in this file at path "../input/fatal-police-shootings-in-the-us/PoliceKillingsUS.csv".
## Figure out what the correct encoding should be and read in the file to a DataFrame police_killings.

## Answer:
police_killings = pd.read_csv("../input/fatal-police-shootings-in-the-us/PoliceKillingsUS.csv", encoding='Windows-1252')

## ) Saving your files with UTF-8 encoding
## Save a version of the police killings dataset to CSV with UTF-8 encoding. Your answer will be marked correct after saving this file.
## Note: When using the to_csv() method, supply only the name of the file (e.g., "my_file.csv"). This saves the file at the filepath "/kaggle/working/my_file.csv".

## Answer:
police_killings.to_csv("my_file.csv")