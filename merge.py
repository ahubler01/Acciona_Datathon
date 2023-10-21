import pandas as pd

# Read the datasets
clima_df = pd.read_csv('clima_filtered.csv')
totalizador_df = pd.read_csv('Totalizador_vf.csv')

# Convert date strings to datetime objects
clima_df['datetimeStr'] = pd.to_datetime(clima_df['datetimeStr'], utc=True)
totalizador_df['RowKey'] = pd.to_datetime(totalizador_df['RowKey'], utc=True)

# Merge the datasets on the common date column
merged_df = pd.merge(clima_df, totalizador_df, left_on='datetimeStr', right_on='RowKey', how='inner')

# Drop the unnamed column if it exists
if 'Unnamed: 0' in merged_df.columns:
    merged_df = merged_df.drop('Unnamed: 0', axis=1)

# Save or further process the merged dataframe as needed
merged_df.to_csv('merged_dataset.csv', index=False)
