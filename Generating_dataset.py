import pandas as pd
import numpy as np
from datetime import datetime, timedelta
np.random.seed(42)

num_rows = 1000
start_date = datetime(2024,1,1)
order_ids = [f"CA-2025-{100000+i}" for i in range(num_rows)]
categories = ['Electronics', 'Furniture', 'Office Supplies']
sub_cats={'Electronics': ['Phones', 'Laptops','Accessories'],
          'Furniture': ['Chairs','Tables','Bookcases'],
          'Office Supplies': ['Paper','Art','Binders']}

regions= ['North','East','South','West']
segments=['Consumer','Corporate','Home Office']
data=[]#to store rows

for i in range(num_rows):
    days_to_add = np.random.randint(0, 500)
    order_date = start_date + timedelta(days=days_to_add)
    ship_date = order_date + timedelta(days=np.random.randint(2, 6))
    
    # Product hierarchy
    cat = np.random.choice(categories)
    sub_cat = np.random.choice(sub_cats[cat])
    
    # Financials
    sales = round(float(np.random.exponential(scale=150) + 10), 2)
    qty = int(np.random.randint(1, 10))
    discount = round(float(np.random.choice([0.0, 0.1, 0.2, 0.5], p=[0.6, 0.2, 0.1, 0.1])), 2)
    # Profit is calculated with some randomness
    profit = round((sales * (np.random.uniform(0.1, 0.4))) - (sales * discount), 2)
    
    data.append({
        'Order ID': order_ids[i],
        'Order Date': order_date.strftime('%Y-%m-%d'),
        'Ship Date': ship_date.strftime('%Y-%m-%d'),
        'Segment': np.random.choice(segments),
        'Region': np.random.choice(regions),
        'Category': cat,
        'Sub-Category': sub_cat,
        'Sales': sales,
        'Quantity': qty,
        'Discount': discount,
        'Profit': profit
    })

# Convert to DataFrame
df = pd.DataFrame(data)
# --- Injecting "Messiness" for Cleaning Practice ---
# 1. Add some missing values
df.loc[df.sample(frac=0.03).index, 'Region'] = np.nan
df.loc[df.sample(frac=0.02).index, 'Sales'] = np.nan

# 2. Add some duplicate rows
duplicates = df.sample(n=15, random_state=42)
df = pd.concat([df, duplicates], ignore_index=True)

# 3. Force dates to be text strings to fix later
df['Order Date'] = df['Order Date'].astype(str)

# Save to raw folder
import os
os.makedirs('data/raw', exist_ok=True)
df.to_csv('data/raw/sales_data.csv', index=False)

print(f"Generated a messy dataset with {df.shape[0]} rows!")
print("Saved to: data/raw/sales_data.csv")