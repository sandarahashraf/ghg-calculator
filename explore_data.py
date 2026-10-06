# Import pandas library
import pandas as pd

# Read the Excel file and select specific sheet
df_egrid = pd.read_excel(r"data\egrid2023_data_rev2.xlsx", sheet_name="SRL23", header=1)

# Assign the selected columns to a new DataFrame and calculate CO2e factor
target_columns = df_egrid[['SUBRGN', 'SRNAME', 'SRCO2RTA']].copy()

# Convert lb CO2e MWh into metric tons CO2e KWh and assign it to a new column
target_columns ['CO2e_factor'] = target_columns['SRCO2RTA'] * 0.00000045359
target_columns = target_columns.dropna()

# Display the selected columns and their CO2e factors without truncation
print(target_columns[['SUBRGN','SRNAME', 'CO2e_factor']].to_string())

# Print the total number of rows, cleanest and dirtiest grid regions, and average CO2e factor
print("Total number of rows:", len(target_columns))
print(f"Cleanest grid region: {target_columns.loc[target_columns['CO2e_factor'].idxmin()]['SUBRGN']} with CO2e factor: {target_columns['CO2e_factor'].min()}")
print(f"Dirtiest grid region: {target_columns.loc[target_columns['CO2e_factor'].idxmax()]['SUBRGN']} with CO2e factor: {target_columns['CO2e_factor'].max()}")
print(f"Average factor: {target_columns['CO2e_factor'].mean():.6f}") 