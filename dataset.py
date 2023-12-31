# -*- coding: utf-8 -*-
"""dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pVd-kEqI07xd2NZ67ffKoaaW6xgnBpSz
"""

# Commented out IPython magic to ensure Python compatibility.
# Importing Libraries

import numpy as np
import pandas as pd
import scipy.stats as ss
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
# %matplotlib inline

plt.style.use('seaborn-whitegrid')

from IPython.display import HTML
from IPython.display import display, Image



import statsmodels.stats.weightstats as smw
import statsmodels.stats.proportion as smp
# Using the CLT Theorem

from scipy.stats import norm
import pandas as pd
import statsmodels.api as sm

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn')

import scipy.stats as ss

import matplotlib.gridspec as gridspec

#!pip install statsmodels==0.10.0rc2 --pre
import statsmodels.api as sm
from statsmodels.formula.api import ols

from statsmodels.stats.multicomp import MultiComparison
import seaborn as sns

# Step 1 - import the dataset
from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
path="caudales.csv"
data = pd.read_csv(path)

data.shape

print(data)

print(data.columns)

"""# Data Analysis"""

import pandas as pd
from scipy import stats

# Load the dataset
url = "caudales.csv"  # Replace with the link to your CSV file
data = pd.read_csv(url)

# Loop through each numerical column and filter out the outliers
for column in data.select_dtypes(include=['float64', 'int64']).columns:
    z_scores = stats.zscore(data[column])
    outliers = (z_scores < -3) | (z_scores > 3)
    data = data[~outliers]

# Display the cleaned dataset without outliers
print(data.head())

"""# removes the outliers for each numerical value in the dataset"""

# Loop through each numerical column and filter out the outliers
for column in data.select_dtypes(include=['float64', 'int64']).columns:
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    data = data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]

# Display the cleaned dataset without outliers
print(data)

"""Z-score method, identifies outliers based on the Z-scores of numerical columns, one below is for INF Value"""

import pandas as pd
from scipy import stats

# Calculate Z-scores for 'INF_Value' column
z_scores = stats.zscore(data['INF_Value'])

# Get boolean array indicating the presence of outliers
outliers = (z_scores < -3) | (z_scores > 3)

# Display the outliers
outlier_data = data[outliers]
print(outlier_data)

# Compute IQR for the 'INF_Value' column
Q1 = data['INF_Value'].quantile(0.25)
Q3 = data['INF_Value'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filter out the outliers from the 'INF_Value' column
data_cleaned = data[(data['INF_Value'] >= lower_bound) & (data['INF_Value'] <= upper_bound)]

# Display the cleaned dataset without outliers in the 'INF_Value' column
print(data_cleaned)

data_cleaned.to_csv("caudales_filtered_1.csv", index=False)

"""# Canonical"""

name_counts = data['Canonical'].value_counts()
print(name_counts)

"""# Canonical Types Frequency"""

canonical_order = data['Canonical'].value_counts().index
plt.figure(figsize=(12, 6))
ax = sns.countplot(x='Canonical', data=data, order=canonical_order)
plt.title('Distribution of Canonical Types')
plt.xlabel('Canonical')
plt.ylabel('Count')
plt.xticks(rotation=45)

# Calculate and annotate the bars with percentages
total = len(data['Canonical'])
for p in ax.patches:
    percentage = '{:.1f}%'.format(100 * p.get_height() / total)
    x = p.get_x() + p.get_width() / 2
    y = p.get_height() + 5
    ax.annotate(percentage, (x, y), ha='center')

plt.show()

"""# Graph (Canonical Types vs INF Value)"""

import matplotlib.pyplot as plt
import seaborn as sns

# Setting the figure size
plt.figure(figsize=(14, 8))

# Define the bin edges for 10% intervals from 0 to 100
bins = [i for i in range(0, 101, 10)]
labels = [f"{i}-{i+10}%" for i in range(0, 100, 10)]

# Create a new column in the data for binning the 'INF_Value'
data['ValueBin'] = pd.cut(data['INF_Value'], bins=bins, labels=labels, right=False)

# Create a count plot
sns.countplot(data=data, x='Canonical', hue='ValueBin')

# Setting the title and labels
plt.title('Distribution of INF_Value for Each Canonical Type')
plt.xlabel('Canonical')
plt.ylabel('Count')
plt.legend(title='INF_Value (%)', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)

# Displaying the plot
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(14, 8))

# Calculate the average INF_Value for each Canonical type
avg_values = data.groupby('Canonical')['INF_Value'].mean()

# Plotting the bar plot
sns.barplot(x=avg_values.index, y=avg_values.values)

plt.title('Average INF_Value for Each Canonical Type')
plt.xlabel('Canonical')
plt.ylabel('Average INF_Value (%)')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# Define a dictionary to map 'Canonical' values to 'INF_Variable'
canonical_to_inf = {
    'CAUDAL': 'Type A',
    'PRESION_ENTRADA_SECTOR': 'Type B',
    'TOTALIZADOR': 'Type C',
    'DEPOSITO': 'Type D',
    'PRESION_SALIDA_SECTOR': 'Type E',
    'DEPOSITO_CAUDAL_SALIDA': 'Type F',
    'DEPOSITO_METROS': 'Type G',
    'MARCHA_POZO': 'Type H',
    'VOLUMEN_DIARIO': 'Type I',
    'VOLUMEN': 'Type J',
    'DEPOSITO_VOLUMEN_SALIDA': 'Type K'
}

# Assuming you have a DataFrame named 'data', create a new column 'INF_Value'
data['INF_Value'] = data['Canonical'].map(canonical_to_inf)

# Count the occurrences of each combination of 'Canonical' and 'INF_Value'
counts = data.groupby(['Canonical', 'INF_Value']).size().reset_index(name='Count')

# Display the counts for each combination
print(counts)

"""# INF Value"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


summary_stats = data['INF_Value'].describe()

# Distribution plot
plt.figure(figsize=(10, 6))
sns.histplot(data['INF_Value'], kde=True)
plt.title('Distribution of INF_Value')
plt.xlabel('INF_Value')
plt.ylabel('Frequency')
plt.show()

# Import necessary libraries
import pandas as pd

url = "/content/drive/MyDrive/SMUC_Notebooks /caudales.csv"
data = pd.read_csv(url)

print(f"Number of rows before removing missing values: {len(data)}")

data_cleaned = data.dropna()

print(f"Number of rows after removing missing values: {len(data_cleaned)}")

"""# Converted RowKey to a Datetime format"""

print(data.columns)

# Import necessary libraries
import pandas as pd

# Convert 'RowKey' to Datetime Format
data['RowKey'] = pd.to_datetime(data['RowKey'])

# Set the 'RowKey' column as the index
data.set_index('RowKey', inplace=True)

# Resample the data on a weekly basis:
weekly_data = data.resample('W').mean()  # Use mean, sum, or other aggregation methods as appropriate

# Perform linear interpolation on the weekly resampled dataset
weekly_data_interpolated = weekly_data.interpolate(method='linear')

# Display the interpolated weekly data
print(weekly_data_interpolated)

# Save the interpolated weekly data back to a new CSV:
weekly_data_interpolated.reset_index().to_csv('weekly_interpolated_data.csv', index=False)

data_monthly = data.resample('M').mean()

# Display the monthly grouped data
print(data_monthly)

# In the results, it is seen that last three months of 2022 have the lowest INF_Value

sector_neta_counts = data['Sector_Neta'].value_counts()
print(sector_neta_counts)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
data = pd.DataFrame(data)

plt.figure(figsize=(10, 6))
sns.countplot(data=data, x='Sector_Neta', order=data['Sector_Neta'].value_counts().index)
plt.title('Distribution of Sector_Neta')
plt.xlabel('Sector_Neta')
plt.ylabel('Count')
plt.show()

STA_Label_counts = data['STA_Label'].value_counts()
print(STA_Label_counts)

plt.figure(figsize=(10, 6))
sns.countplot(data=data, x='STA_Label', order=data['STA_Label'].value_counts().index)
plt.title('Distribution of STA_Label')
plt.xlabel('STA_Label')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

