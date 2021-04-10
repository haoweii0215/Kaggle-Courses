# Exercise 2 : Scaling and Normalization
from learntools.core import binder
binder.bind(globals())
from learntools.data_cleaning.ex2 import *
import pandas as pd
import numpy as np
from scipy import stats
from mlxtend.preprocessing import minmax_scaling
import seaborn as sns
import matplotlib.pyplot as plt
print("Setup Complete")

kickstarters_2017 = pd.read_csv("../input/kickstarter-projects/ks-projects-201801.csv")
np.random.seed(0)

## 1) Practice scaling
## We just scaled the "usd_goal_real" column. What about the "goal" column?
## Begin by running the code cell below to create a DataFrame original_goal_data containing the "goal" column.
original_goal_data = pd.DataFrame(kickstarters_2017.goal)

## Answer:
scaled_goal_data = minmax_scaling(original_goal_data, columns=['goal'])

## 2) Practice normalization
## Now you'll practice normalization. We begin by normalizing the amount of money pledged to each campaign.
index_of_positive_pledges = kickstarters_2017.usd_pledged_real > 0
positive_pledges = kickstarters_2017.usd_pledged_real.loc[index_of_positive_pledges]
normalized_pledges = pd.Series(stats.boxcox(positive_pledges)[0],
                               name='usd_pledged_real', index=positive_pledges.index)
fig, ax=plt.subplots(1,2,figsize=(15,3))
sns.distplot(positive_pledges, ax=ax[0])
ax[0].set_title("Original Data")
sns.distplot(normalized_pledges, ax=ax[1])
ax[1].set_title("Normalized data")
print('Original data\nPreview:\n', positive_pledges.head())
print('Minimum value:', float(positive_pledges.min()), '\nMaximum value:', float(positive_pledges.max()))
print('_'*30)
print('\nNormalized data\nPreview:\n', normalized_pledges.head())
print('Minimum value:', float(normalized_pledges.min()), '\nMaximum value:', float(normalized_pledges.max()))

## Answer:
index_positive_pledges = kickstarters_2017.pledged > 0
positive_pledges_only = kickstarters_2017.pledged.loc[index_positive_pledges]
normalized_values = pd.Series(stats.boxcox(positive_pledges_only)[0],
                              name='pledged', index=positive_pledges_only.index)
fig, ax = plt.subplots(1,2,figsize=(15,3))
sns.distplot(positive_pledges_only, ax=ax[0])
ax[0].set_title("Original Data")
sns.distplot(normalized_values, ax=ax[1])
ax[1].set_title("Normalized data")

