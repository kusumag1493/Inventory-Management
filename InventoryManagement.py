import pandas as pd
import zipfile

# Load the CSV file from the zip archive
file_path = 'SalesKaggle3.csv.zip'
with zipfile.ZipFile(file_path, 'r') as zip_ref:
    zip_ref.extractall('data')
    
# Load the CSV file into a pandas dataframe
df = pd.read_csv('data/SalesKaggle3.csv')

# Rename the relevant columns for ABC analysis
df = df.rename(columns={
    'SKU_number': 'Item_ID',
    'SoldCount': 'Annual_Usage',
    'PriceReg': 'Cost_Per_Unit'
})

# Step 1: Calculate total value (Annual Usage * Cost per Unit)
df['Total_Value'] = df['Annual_Usage'] * df['Cost_Per_Unit']

# Step 2: Sort items by total value in descending order
df_sorted = df.sort_values(by='Total_Value', ascending=False).reset_index(drop=True)

# Step 3: Calculate cumulative value percentage
df_sorted['Cumulative_Value'] = df_sorted['Total_Value'].cumsum()
df_sorted['Cumulative_Percentage'] = 100 * df_sorted['Cumulative_Value'] / df_sorted['Total_Value'].sum()

# Step 4: Classify items into A, B, C categories based on cumulative percentage thresholds
df_sorted['ABC_Category'] = pd.cut(
    df_sorted['Cumulative_Percentage'],
    bins=[0, 70, 90, 100],
    labels=['A', 'B', 'C']
)

# Show the top 10 rows of the result
print(df_sorted[['Item_ID', 'Annual_Usage', 'Cost_Per_Unit', 'Total_Value', 'Cumulative_Percentage', 'ABC_Category']].head(10))

# Save the result to a new CSV file
new_output_file_path = 'ABC_Analysis_New_Result.csv'
df_sorted[['Item_ID', 'Annual_Usage', 'Cost_Per_Unit', 'Total_Value', 'Cumulative_Percentage', 'ABC_Category']].to_csv(new_output_file_path, index=False)

print(f'ABC Analysis result has been saved to {new_output_file_path}')
