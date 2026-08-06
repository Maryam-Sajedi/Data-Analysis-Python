"""
# Project Overview

Data analysis for a small retail company:
sales dataset covering 12 months across four product categories.

Goals:
- Writing a sample dataset to a CSV file.
- Reading it back and inspecting it.
- Adding a revenue column (units sold multiplied by price per unit).
- Grouping by product category and plotting total revenue as a bar chart.
- Applying NumPy to identify the peak sales month.

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -- Step 1: Write the sample CSV --
csv_content = """date,product_category,units,price_per_unit
2024-01-01,Electronics,120,299.99
2024-01-01,Clothing,340,45.00
2024-01-01,Food,890,8.50
2024-01-01,Books,210,14.99
2024-02-01,Electronics,95,299.99
2024-02-01,Clothing,280,45.00
2024-02-01,Food,760,8.50
2024-02-01,Books,180,14.99
2024-03-01,Electronics,140,299.99
2024-03-01,Clothing,410,45.00
2024-03-01,Food,1050,8.50
2024-03-01,Books,260,14.99
2024-04-01,Electronics,130,299.99
2024-04-01,Clothing,370,45.00
2024-04-01,Food,920,8.50
2024-04-01,Books,230,14.99
2024-05-01,Electronics,160,299.99
2024-05-01,Clothing,450,45.00
2024-05-01,Food,980,8.50
2024-05-01,Books,275,14.99
2024-06-01,Electronics,175,299.99
2024-06-01,Clothing,500,45.00
2024-06-01,Food,1100,8.50
2024-06-01,Books,290,14.99
2024-07-01,Electronics,200,299.99
2024-07-01,Clothing,530,45.00
2024-07-01,Food,1200,8.50
2024-07-01,Books,310,14.99
2024-08-01,Electronics,185,299.99
2024-08-01,Clothing,510,45.00
2024-08-01,Food,1150,8.50
2024-08-01,Books,295,14.99
2024-09-01,Electronics,155,299.99
2024-09-01,Clothing,420,45.00
2024-09-01,Food,970,8.50
2024-09-01,Books,255,14.99
2024-10-01,Electronics,145,299.99
2024-10-01,Clothing,390,45.00
2024-10-01,Food,900,8.50
2024-10-01,Books,240,14.99
2024-11-01,Electronics,220,299.99
2024-11-01,Clothing,580,45.00
2024-11-01,Food,1300,8.50
2024-11-01,Books,330,14.99
2024-12-01,Electronics,310,299.99
2024-12-01,Clothing,700,45.00
2024-12-01,Food,1500,8.50
2024-12-01,Books,400,14.99
"""

with open('sales_data.csv', 'w') as f:
    f.write(csv_content)

print("sales_data.csv written successfully.")

# -- Step 2: Read the CSV and inspect it --
df = pd.read_csv('sales_data.csv', parse_dates=['date'])

print("Shape:", df.shape) # (number of rows, and columns)
print()
print(df.head(8))
print()
df.info()


# -- Step 3: Add a revenue column --
df['revenue'] = df['units'] * df['price_per_unit']

print("Preview with revenue column:")
print(df[['date', 'product_category', 'units', 'price_per_unit', 'revenue']].head(8))
print()
print(f"Total revenue across all categories: £{df['revenue'].sum():,.2f}")

# -- Step 4: Groupby product category and plot total revenue --
category_revenue = df.groupby('product_category')['revenue'].sum().sort_values(ascending = False)
print(f"Total revenue: {category_revenue}")

plt.bar(category_revenue.index, category_revenue.values, color=["steelblue", "darkorange", "green", "violet"])
plt.xlabel('product category')
plt.ylabel('Total revenue (€)')
plt.title('Total revenue by product category (2026)')
plt.tight_layout()
plt.show()

print()
print("Total revenue by category:")
for cat, rev in category_revenue.items():
    print(f"  {cat}: £{rev:,.2f}")

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(category_revenue.index, category_revenue.values, color=['steelblue', '#dd8452', '#55a868', '#c44e52'])
ax.set_xlabel('Product Category')
ax.set_ylabel('Total Revenue (£)')
ax.set_title('Total Revenue by Product Category (2024)')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'£{x:,.0f}'))
plt.tight_layout()
plt.show()

# -- Step 5: Use NumPy to find the peak sales month --:
monthly_units = df.groupby('date')['units'].sum()

print(monthly_units.max())
print(monthly_units.idxmax().date())
print()

units_array = np.array(monthly_units.values)
months = monthly_units.index

peak_index = np.argmax(units_array)
peak_month = months[peak_index]
peak_units = units_array[peak_index]

print(f"Peak sales month: {peak_month.strftime('%B %Y')}")
print(f"Total units sold that month: {peak_units:,}")
print()

# Sum all units sold per month across all categories:
print("Monthly totals (all categories combined):")
for month, units in zip(months, units_array):
    print(f"  {month.strftime('%b %Y')}: {units:,} units")
    
# Step 1: Add a 'profit' column (30% of revenue):
df['profit'] = df['revenue'] * 0.3

# Step 2: Group by product_category and sum profit:
sum_profit = df.groupby('product_category')['profit'].sum().sort_values(ascending = False)
for cat, profit in sum_profit.items():
    print(f"{cat}, {profit:,.2f}€")
# Step 3: Plot a bar chart:
plt.bar(sum_profit.index, sum_profit.values, color=["steelblue", "darkorange", "green", "violet"])
plt.title('Total profit per category')
plt.xlabel('Product category')
plt.ylabel('Total profit (€)')
plt.tight_layout()
plt.show()

# Step 4: Print the category with the highest profit:
peak_profit = sum_profit.max()
print(f"Highest profit: {peak_profit:,.2f}€")
top_category = sum_profit.idxmax()
print(f"Top profit category: {top_category}")