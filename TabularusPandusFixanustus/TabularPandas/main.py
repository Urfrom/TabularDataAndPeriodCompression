import numpy as np
import pandas as pd

tabular_data = pd.read_csv("tabular_data.csv")

# Unlike any other feature, this one is of string type.
string_feature = "feature_25"

# Let's compare its contents with hased_data.
hashed_data = pd.read_csv("hashed_feature.csv")

local_feature = "feature_50"

# Drop train data.
tabular_data = tabular_data[tabular_data.id < 4084]
hashed_data = hashed_data[hashed_data.id < 4084]

# Here we gather hashes.
tabular_strings = tabular_data[string_feature].drop_duplicates()
hashed_strings = hashed_data[local_feature].drop_duplicates()

# Ad-hoc solution.
match = set(tabular_strings) & set(hashed_strings)

# As we see, no mathces here. They are completely independent.
print(len(match), len(tabular_strings), len(hashed_strings))

# How much data is missing?
print(tabular_data[string_feature].isnull().sum(), hashed_data[local_feature].isnull().sum())
# Did not expect tabular_data to have no missing string_feature.

# Let's do some basic exploration.

missing_values = tabular_data.isnull().sum()

# Do the same, but for the whole data set.
print(missing_values)
# There're 6 features that are not missing at all.

total_missing = missing_values.sum()

# How much is missing?
print(total_missing / np.product(tabular_data.shape))

# How much data is left after deleting rows with missing values.
print(1.0 - len(tabular_data.dropna()) / len(tabular_data))
# Apparently, we need a way to handle such a loss.
