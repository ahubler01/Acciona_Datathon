import pandas as pd

# Load your datasets
clima_clean = pd.read_csv('clima_filtered.csv')
Totalizador_zone_1 = pd.read_csv('Totalizador_zone_1.csv')
Totalizador_zone_2 = pd.read_csv('Totalizador_zone_2.csv')
Totalizador_zone_3 = pd.read_csv('Totalizador_zone_1.csv')

# Convert datetime columns to a consistent format in other datasets
Totalizador_zone_1['RowKey'] = pd.to_datetime(Totalizador_zone_1['RowKey'], format='%Y-%m-%dT%H:%M:%S.%fZ')
Totalizador_zone_2['RowKey'] = pd.to_datetime(Totalizador_zone_2['RowKey'], format='%Y-%m-%dT%H:%M:%S.%fZ')
Totalizador_zone_3['RowKey'] = pd.to_datetime(Totalizador_zone_3['RowKey'], format='%Y-%m-%dT%H:%M:%S.%fZ')

# Merge clima_clean with each of the other datasets separately
merged_data1 = pd.merge(clima_clean, Totalizador_zone_1, left_on='datetimeStr', right_on='RowKey', how='inner')
merged_data2 = pd.merge(clima_clean, Totalizador_zone_2, left_on='datetimeStr', right_on='RowKey', how='inner')
merged_data3 = pd.merge(clima_clean, Totalizador_zone_3, left_on='datetimeStr', right_on='RowKey', how='inner')

# Save the merged datasets to separate CSV files
merged_data1.to_csv('merged_dataset1.csv', index=False)
merged_data2.to_csv('merged_dataset2.csv', index=False)
merged_data3.to_csv('merged_dataset3.csv', index=False)
