# Scaling and Normalization
import pandas as pd
import numpy as np
from scipy import stats
from mlxtend.preprocessing import minmax_scaling
import seaborn as sns
import matplotlib.pyplot as plt

### generate 1000 data points randomly drawn from an exponential distribution
original_data = np.random.exponential(size=1000)

### mix-max scale the data between 0 and 1
scaled_data = minmax_scaling(original_data, columns=[0])

### plot both together to compare
fig, ax = plt.subplots(1,2)
sns.distplot(original_data, ax=ax[0])
ax[0].set_title("Original Data")
sns.distplot(scaled_data, ax=ax[1])
ax[1].set_title("Scaled data")

### normalize the exponential data with boxcox
normalized_data = stats.boxcox(original_data)

### plot both together to compare
fig, ax=plt.subplots(1,2)
sns.distplot(original_data, ax=ax[0])
ax[0].set_title("Original Data")
sns.distplot(normalized_data[0], ax=ax[1])
ax[1].set_title("Normalized data")


