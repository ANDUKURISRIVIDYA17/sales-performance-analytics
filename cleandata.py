import os
import pandas as pd

# 1. Load the messy data
raw_path = 'data/raw/sales_data.csv'
df = pd.read_csv(raw_path)

print("--- Initial Inspection ---")
print(f"Total rows starting out: {len(df)}")
print("\nMissing values per column:")
print(df.isnull().sum())

# 2. Drop absolute duplicates
initial_count = len(df)
df.drop_duplicates(inplace=True)
print(f"\nRemoved {initial_count - len(df)} duplicate rows.")

# 3. Handle Missing Values
# For 'Region', we can fill it with a placeholder like 'Unknown'
df['Region'] = df['Region'].fillna('Unknown')

# For 'Sales', since it's a critical financial KPI, dropping rows with missing sales is safest
df.dropna(subset=['Sales'], inplace=True)

# 4. Correct Data Types (Convert string dates to actual datetime objects)
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# 5. Feature Engineering (Adding columns to make Power BI modeling easier)
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.strftime('%B')  # Outputs: January, February, etc.
df['Profit Margin'] = df['Profit'] / df['Sales']

print("\n--- Post-Cleaning Inspection ---")
print(f"Total rows remaining: {len(df)}")
print(f"Any missing values left? {df.isnull().sum().sum()}")

# 6. Save the clean data to an Excel file for Power BI
processed_dir = 'data/processed'
os.makedirs(processed_dir, exist_ok=True)
output_path = os.path.join(processed_dir, 'clean_sales_data.csv')

df.to_csv(output_path, index=False)
print(f"\nSuccess! Cleaned data saved to: {output_path}")