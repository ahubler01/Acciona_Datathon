import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# !pip install statsmodels==0.10.0rc2 --pre
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy import stats
import scipy.stats as ss
from statsmodels.stats.multicomp import MultiComparison



filtered_df_caudales = pd.read_csv("setDatos/caudales_filtered_1.csv")
df_caudales = pd.read_csv("setDatos/caudales.csv")
df_abon_clien_cont = pd.read_csv("setDatos/df_abon_clien_cont.csv")
df_gis = pd.read_csv("setDatos/gis.csv")


# code = df_gis["code"]
# mask = df_caudales['Sector_Neta'].isin(code)
# filtered_df_caudales = df_caudales[mask]
# len(filtered_df_caudales)
# filtered_df_caudales.columns


#Add zones to canonical with the GIS df.

#GIS DF
df_gis = pd.read_csv("setDatos/gis.csv")

df_gis = df_gis.drop(['oid', 'service', 'parentCode'], axis = 1)
#Expand bissioCode
df_gis[['SECTOR_A', 'SECTOR_B', 'SECTOR_C', 'SECTOR_D']] = df_gis['bissioCode'].str.split('.', expand=True, n=3).fillna('')

df_gis = df_gis.drop("bissioCode", axis = 1)

#Convert missing values to NA
df_gis = df_gis.replace('', "NA")

#Remove duplicates
for index, row in df_gis.iterrows():
    for col in ['SECTOR_B', 'SECTOR_C', 'SECTOR_D']:
        if row[col] == row['SECTOR_A']:
            df_gis.at[index, col] = "NA"

#Creates a new column and assign the number of zone supply
df_gis["Number_zone"] = ""
columns_to_check = ['SECTOR_A', 'SECTOR_B', 'SECTOR_C', 'SECTOR_D']
# Initialize an empty list to store the count of missing values per row
missing_values_count_per_row = []
for index, row in df_gis.iterrows():
    row_missing_values = 0  # Initialize count for each row
    for col in columns_to_check:
        if row[col] != "NA":  # Check if the value is NaN
            row_missing_values += 1
    df_gis.at[index, "Number_zone"] = row_missing_values

#Water supply for zone 0:
#Water supply for zone 1:
df_gis_zone_1 = df_gis[(df_gis['SECTOR_A'] == '1') | (df_gis['SECTOR_B'] == '1') | (df_gis['SECTOR_C'] == '1') | (df_gis['SECTOR_D'] == '1')]
df_gis_zone_1 = df_gis_zone_1.drop(['SECTOR_A', 'SECTOR_B', 'SECTOR_C', 'SECTOR_D'], axis = 1)
#Water supply for zone 2:
df_gis_zone_2 = df_gis[(df_gis['SECTOR_A'] == '2') | (df_gis['SECTOR_B'] == '2') | (df_gis['SECTOR_C'] == '2') | (df_gis['SECTOR_D'] == '2')]
df_gis_zone_2 = df_gis_zone_2.drop(['SECTOR_A', 'SECTOR_B', 'SECTOR_C', 'SECTOR_D'], axis = 1)
#Water supply for zone 3:
df_gis_zone_3 = df_gis[(df_gis['SECTOR_A'] == '3') | (df_gis['SECTOR_B'] == '3') | (df_gis['SECTOR_C'] == '3') | (df_gis['SECTOR_D'] == '3')]
df_gis_zone_3 = df_gis_zone_3.drop(['SECTOR_A', 'SECTOR_B', 'SECTOR_C', 'SECTOR_D'], axis = 1)

# print(df_gis_zone_1)
# print(df_gis_zone_2)
# print(df_gis_zone_3)

# df_caudales_test = pd.read_csv("setDatos/caudales.csv")
# zone_1_code = df_gis_zone_1["code"]
# filtered_df = df_caudales_test[df_caudales_test['Sector_Neta'].isin(zone_1_code)]
# print(filtered_df)


#Add corresponding zone to caudales
zone_1_code = df_gis_zone_1["code"]
filtered_df_caudales.loc[filtered_df_caudales['Sector_Neta'].isin(zone_1_code), 'Zone_1'] = True
zone_2_code = df_gis_zone_2["code"]
filtered_df_caudales.loc[filtered_df_caudales['Sector_Neta'].isin(zone_2_code), 'Zone_2'] = True
zone_3_code = df_gis_zone_3["code"]
filtered_df_caudales.loc[filtered_df_caudales['Sector_Neta'].isin(zone_3_code), 'Zone_3'] = True

#Group by canonical
grouped_canocical = filtered_df_caudales.groupby('Canonical')
caudales_by_canonical = []
for name, group in grouped_canocical:
    caudales_by_canonical.append(group)

# Group by zone
caudales_by_canonical_zone = {'Zone_1': [], 'Zone_2': [], 'Zone_3': []}

for df in caudales_by_canonical:
    caudales_by_canonical_zone['Zone_1'].append(df[df['Zone_1'].isin([True])])
    caudales_by_canonical_zone['Zone_2'].append(df[df['Zone_2'].isin([True])])
    caudales_by_canonical_zone['Zone_3'].append(df[df['Zone_3'].isin([True])])
   

#1. Caudal
#2. Presion_entrada_sector
#3. Presion_salida_sector
#4. Totalizador
#5. Volumen_diario



result_dict = {}
# Iterate through unique values in Column1 and collect unique values from Column2
for key in df_caudales['Canonical'].unique():
    unique_values = df_caudales[df_caudales['Canonical'] == key]['INF_Label'].unique()
    result_dict[key] = unique_values.tolist()

#Removing outliers in every subdf:

# Remove outliers in every sublist
caudales_by_canonical_zone_filtered = {'Zone_1': [], 'Zone_2': [], 'Zone_3': []}
for zone in caudales_by_canonical_zone:
    for canonical in zone:
        # Loop through each numerical column and filter out the outliers
        for column in canonical.select_dtypes(include=['float64', 'int64']).columns:
            z_scores = stats.zscore(canonical[column])
            outliers = (z_scores < -3) | (z_scores > 3)
            canonical = canonical[~outliers]

        # Calculate IQR for each numerical column and filter out the outliers
        for column in canonical.select_dtypes(include=['float64', 'int64']).columns:
            Q1 = canonical[column].quantile(0.25)
            Q3 = canonical[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            canonical = canonical[(canonical[column] >= lower_bound) & (canonical[column] <= upper_bound)]

        # Calculate Z-scores for 'INF_Value' column
        z_scores = stats.zscore(canonical['INF_Value'])
        # Get boolean array indicating the presence of outliers
        outliers = (z_scores < -3) | (z_scores > 3)
        # Display the outliers
        outlier_data = canonical[outliers]
        print(outlier_data)

        # Compute IQR for the 'INF_Value' column
        Q1 = canonical['INF_Value'].quantile(0.25)
        Q3 = canonical['INF_Value'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Filter out the outliers from the 'INF_Value' column
        data_cleaned = canonical[(canonical['INF_Value'] >= lower_bound) & (canonical['INF_Value'] <= upper_bound)]


        # caudales_by_canonical_zone_filtered['Zone_1'].append(data_cleaned[data_cleaned['Zone_1'].isin([True])])
        # caudales_by_canonical_zone_filtered['Zone_2'].append(data_cleaned[data_cleaned['Zone_2'].isin([True])])
        # caudales_by_canonical_zone_filtered['Zone_3'].append(data_cleaned[data_cleaned['Zone_3'].isin([True])])
        # caudales_by_canonical_zone_filtered['Zone_4'].append(data_cleaned[data_cleaned['Zone_4'].isin([True])])




#
#
# len(df_caudales['Canonical'].unique())
# len(filtered_df_caudales['Canonical'].unique())
#
#
#
# #Frequency
# # Convert the 'datetime_column' to a datetime data type
# filtered_df_caudales['RowKey'] = pd.to_datetime(filtered_df_caudales['RowKey'])
#
# # Sort the DataFrame by the 'type' and 'datetime_column' for accurate time difference calculations
# filtered_df_caudales = filtered_df_caudales.sort_values(by=['Canonical', 'RowKey'])
#
# # Calculate the time difference for each group (type)
# filtered_df_caudales['time_difference'] = filtered_df_caudales.groupby('Canonical')['RowKey'].diff()
#
# # Fill NaT with a default value (e.g., 0 or a specific time delta)
# filtered_df_caudales['time_difference'].fillna(pd.Timedelta(seconds=0), inplace=True)
#
# # Find the most common time_difference for each type
# most_common = filtered_df_caudales.groupby('Canonical')['time_difference'].agg(lambda x: x.mode().iat[0])
#
# # Create a new DataFrame with the most common time_difference for each type
# most_common_df = most_common.reset_index()
# most_common_df.rename(columns={'time_difference': 'most_common_time_difference'}, inplace=True)
#
# print(most_common_df)





