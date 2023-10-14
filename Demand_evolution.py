import pandas as pd

df_abonado = pd.read_csv("setDatos/abonado.csv")
df_cliente = pd.read_csv("setDatos/cliente.csv")
df_contador = pd.read_csv("setDatos/contador.csv")

#Merge abonado with cliente
df_abonado_cliente = df_abonado.merge(df_cliente, on='COD_SUMINISTRO', how='inner')

#Merge df_abonado_cliente with contador
df_abon_clien_cont = df_abonado_cliente.merge(df_contador, on='COD_CONTADOR_ACT', how='inner')

df_abon_clien_cont.columns

#Remove duplicates
df_abon_clien_cont = df_abon_clien_cont.drop(["cod_concesion_x", "SECTOR_y", "COD_TIPO_SUMINISTRO_y", "cod_concesion_y"], axis = 1)

# Display the first few rows of the DataFrame
print(df_abon_clien_cont.head())

# Get a summary of the data's structure
print(df_abon_clien_cont.info())

# Check basic statistics
print(df_abon_clien_cont.describe())


# Remove dummy variables: NUM_VIVIENDAS
df_abon_clien_cont = df_abon_clien_cont.drop(["NUM_VIVIENDAS", "COD_CONCESION"], axis = 1)

#Every unique COD_TIPO_SUMINISTRO_x
df_abon_clien_cont["COD_TIPO_SUMINISTRO_x"].value_counts()

#Every unique FECHA_ALTA_SUMINISTRO
df_abon_clien_cont["FECHA_ALTA_SUMINISTRO"].value_counts()

# Split the 'SECTOR_x' column into three columns
df_abon_clien_cont[['SECTOR_A', 'SECTOR_B', 'SECTOR_C']] = df_abon_clien_cont['SECTOR_x'].str.split('.', expand=True, n=2).fillna('')

df_abon_clien_cont = df_abon_clien_cont.drop("SECTOR_x", axis = 1)
df_abon_clien_cont = df_abon_clien_cont.drop("COD_SUMINISTRO", axis = 1)
df_abon_clien_cont = df_abon_clien_cont.drop("COD_CONTADOR_ACT", axis = 1)


#Number of new contract

df = pd.DataFrame({
    "New_dates": pd.to_datetime(df_abon_clien_cont["FECHA_ALTA_SUMINISTRO"]),
    "SECTOR_A": df_abon_clien_cont["SECTOR_A"],
    "SECTOR_B": df_abon_clien_cont["SECTOR_B"],
    "SECTOR_C": df_abon_clien_cont["SECTOR_C"]
})
df.set_index("New_dates", inplace=True)

#For zona 0:
df_zone_0 = df[(df['SECTOR_A'] == '0') | (df['SECTOR_B'] == '0') | (df['SECTOR_C'] == '0')]

# Resample by month and count the number of new contracts per month
pivot_df_0 = df_zone_0.resample('M').size().reset_index(name='Frequency')

# Extract the year and month into separate columns
pivot_df_0['Year'] = pivot_df_0['New_dates'].dt.year
pivot_df_0['Months'] = pivot_df_0['New_dates'].dt.month

# Pivot the DataFrame with 'Year' as columns and 'Month' as the values
pivot_df_0 = pivot_df_0.pivot(index='Months', columns='Year', values='Frequency').fillna(0)

#For zona 1:
df_zone_1 = df[(df['SECTOR_A'] == '1') | (df['SECTOR_B'] == '1') | (df['SECTOR_C'] == '1')]

# Resample by month and count the number of new contracts per month
pivot_df_1 = df_zone_1.resample('M').size().reset_index(name='Frequency')

# Extract the year and month into separate columns
pivot_df_1['Year'] = pivot_df_1['New_dates'].dt.year
pivot_df_1['Months'] = pivot_df_1['New_dates'].dt.month

# Pivot the DataFrame with 'Year' as columns and 'Month' as the values
pivot_df_1 = pivot_df_1.pivot(index='Months', columns='Year', values='Frequency').fillna(0)

#For zona 2:
df_zone_2 = df[(df['SECTOR_A'] == '2') | (df['SECTOR_B'] == '2') | (df['SECTOR_C'] == '2')]

# Resample by month and count the number of new contracts per month
pivot_df_2 = df_zone_2.resample('M').size().reset_index(name='Frequency')

# Extract the year and month into separate columns
pivot_df_2['Year'] = pivot_df_2['New_dates'].dt.year
pivot_df_2['Months'] = pivot_df_2['New_dates'].dt.month

# Pivot the DataFrame with 'Year' as columns and 'Month' as the values
pivot_df_2 = pivot_df_2.pivot(index='Months', columns='Year', values='Frequency').fillna(0)

#For zona 3:
df_zone_3 = df[(df['SECTOR_A'] == '3') | (df['SECTOR_B'] == '3') | (df['SECTOR_C'] == '3')]

# Resample by month and count the number of new contracts per month
pivot_df_3 = df_zone_3.resample('M').size().reset_index(name='Frequency')

# Extract the year and month into separate columns
pivot_df_3['Year'] = pivot_df_3['New_dates'].dt.year
pivot_df_3['Months'] = pivot_df_3['New_dates'].dt.month

# Pivot the DataFrame with 'Year' as columns and 'Month' as the values
pivot_df_3 = pivot_df_3.pivot(index='Months', columns='Year', values='Frequency').fillna(0)

#Display
print(pivot_df_0)
print(pivot_df_1)
print(pivot_df_2)
print(pivot_df_3)
