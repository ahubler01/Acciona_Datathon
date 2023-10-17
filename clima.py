import numpy as np
import pandas as pd

df = pd.read_csv("clima.csv")

# List of columns to drop
columns_to_drop = ['mint', 'maxt', 'wspd', 'wgust', 'wdir', 'info', 'snow', 'sealevelpressure', 'snowdepth', 'heatindex', 'weathertype', 'conditions']

# Drop the specified columns
df = df.drop(columns=columns_to_drop)

# Columns to fill missing values for
columns_to_fill = ['cloudcover', 'temp', 'visibility', 'solarenergy', 'datetime', 'precip', 'solarradiation', 'dew', 'humidity', 'precipcover', 'windchill']

# Iterate through rows and fill missing values in the specified columns
for index, row in df.iterrows():
    for column_to_fill in columns_to_fill:
        if pd.isnull(row[column_to_fill]):
            # Search for the nearest non-missing values in the row
            before_index = index - 1
            after_index = index + 1
            
            while before_index >= 0 and pd.isnull(df.at[before_index, column_to_fill]):
                before_index -= 1
            
            while after_index < len(df) and pd.isnull(df.at[after_index, column_to_fill]):
                after_index += 1
            
            # Calculate the average of the nearest non-missing values
            if before_index >= 0 and after_index < len(df):
                df.at[index, column_to_fill] = (df.at[before_index, column_to_fill] + df.at[after_index, column_to_fill]) / 2
            elif before_index >= 0:
                df.at[index, column_to_fill] = df.at[before_index, column_to_fill]
            elif after_index < len(df):
                df.at[index, column_to_fill] = df.at[after_index, column_to_fill]
                
# Set Coordinates range
lat1 = 39.234068
lat2 = 39.210825
lon1 = -3.625906
lon2 = -3.587290

# Extract latitude and longitude columns from the 'locations' column
df[['latitude', 'longitude']] = df['locations'].str.split(',', expand=True).astype(float)

# Filter rows based on the coordinate range
df_filtered = df[
    (df['latitude'] <= lat1) & (df['latitude'] >= lat2) &
    (df['longitude'] >= lon1) & (df['longitude'] <= lon2)
]

# Drop the temporary latitude and longitude columns
df_filtered = df_filtered.drop(['latitude', 'longitude'], axis=1)

df_filtered.to_csv('clima_clean.csv')