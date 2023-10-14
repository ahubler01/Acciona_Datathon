# Load GIS data from a CSV file
df_gis = pd.read_csv("setDatos/gis.csv")

# Drop unnecessary columns: oid, service, and parentCode
df_gis = df_gis.drop(['oid', 'service', 'parentCode'], axis=1)

# Expand the 'bissioCode' column into separate 'SECTOR_A', 'SECTOR_B', 'SECTOR_C', and 'SECTOR_D' columns
df_gis[['SECTOR_A', 'SECTOR_B', 'SECTOR_C', 'SECTOR_D']] = df_gis['bissioCode'].str.split('.', expand=True, n=3).fillna('')

# Drop the original 'bissioCode' column
df_gis = df_gis.drop("bissioCode", axis=1)

# Convert empty strings to "NA" to represent missing values
df_gis = df_gis.replace('', "NA")

# Remove duplicates within specific columns
for index, row in df_gis.iterrows():
    for col in ['SECTOR_B', 'SECTOR_C', 'SECTOR_D']:
        if row[col] == row['SECTOR_A']:
            df_gis.at[index, col] = "NA"

# Create a new column 'Number_zone' to store the count of non-missing values in specified columns
df_gis["Number_zone"] = ""
columns_to_check = ['SECTOR_A', 'SECTOR_B', 'SECTOR_C', 'SECTOR_D']

# Initialize an empty list to store the count of missing values per row
missing_values_count_per_row = []

# Iterate through the rows to count non-missing values
for index, row in df_gis.iterrows():
    row_missing_values = 0  # Initialize the count for each row
    for col in columns_to check:
        if row[col] != "NA":  # Check if the value is not "NA"
            row_missing_values += 1
    df_gis.at[index, "Number_zone"] = row_missing_values

# Display the first 16 rows of the DataFrame
df_gis.head(16)
