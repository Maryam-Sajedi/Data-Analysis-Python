"""
Product Catalogue Analysis with Pandas
=======================================
A small, self-contained example of how to select, filter, edit, and
summarize tabular data using pandas' .iloc, .loc, and .query() tools.

Run this file top to bottom in Thonny (or any plain Python interpreter).
No internet connection or extra setup is needed - the "dataset" is a
small CSV built right into the script using io.StringIO, and the only
dependency is pandas.

    pip install pandas
"""

import pandas as pd
import io

# ---------------------------------------------------------------------
# 0. THE DATA
# ---------------------------------------------------------------------
# A tiny product catalogue for a kitchen & garden shop, written as a
# CSV string. io.StringIO lets pandas read a string as if it were a
# CSV file, so nothing needs to be saved to disk first.
product_csv = """product_code,name,category,price,stock,supplier
P001,Chopping Board,Kitchen,18.99,45,Northwind
P002,Garden Trowel,Garden,9.50,120,Greenfield
P003,Espresso Cups,Kitchen,24.00,18,Northwind
P004,Watering Can,Garden,15.75,60,Greenfield
P005,Chef Knife,Kitchen,52.00,12,BladeCo
P006,Plant Pots,Garden,7.25,200,Greenfield
P007,Mixing Bowls,Kitchen,31.50,33,Northwind
P008,Pruning Shears,Garden,28.00,25,BladeCo"""

products = pd.read_csv(io.StringIO(product_csv))
print(products)
print()

# ---------------------------------------------------------------------
# 1. First 4 rows and first 3 columns, using .iloc (position-based)
# ---------------------------------------------------------------------
print("1. First 4 rows and 3 columns:")
print(f"{products.iloc[0:4, 0:3]}")
print()

# ---------------------------------------------------------------------
# 2. Move product_code into the index -> catalogue
# ---------------------------------------------------------------------
print("2. product_code becomes index:")
catalogue = products.set_index('product_code')
print(f"{catalogue}")
print()

# ---------------------------------------------------------------------
# 3. The whole row for P004, using .loc (label-based)
# ---------------------------------------------------------------------
print("3. The whole row for P004:")
print(catalogue.loc['P004'])
print()

# ---------------------------------------------------------------------
# 4. name and price of every Kitchen product, using a mask inside .loc
# ---------------------------------------------------------------------
print("4. Name and price of every kitchen product:")
print(catalogue.loc[catalogue['category'] == 'Kitchen', ['name', 'price']])
print()

# ---------------------------------------------------------------------
# 5. Reduce every Garden price by 20% in a single .loc assignment
# ---------------------------------------------------------------------
print("5. 20% discount on Garden items:")
catalogue.loc[catalogue['category'] == 'Garden', 'price'] *= 0.80
print(catalogue.loc[catalogue['category'] == 'Garden', ['name', 'price']])
print()

# ---------------------------------------------------------------------
# 6. .query(): costs at least 30 AND has at least 20 in stock
# ---------------------------------------------------------------------
print("6. Costs at least 30, and at least 20 in stock:")
print(catalogue.query('price >= 30 and stock >= 20')[['name', 'price', 'stock']])
print()

# ---------------------------------------------------------------------
# 7. Count the products in each category
# ---------------------------------------------------------------------
print("7. Number of products in each category:")
print(catalogue.value_counts('category'))
print()

# ---------------------------------------------------------------------
# 8. Tidied copy 'report': rename stock -> units_in_stock, drop supplier
#    Then confirm catalogue still has its supplier column (i.e. the
#    original wasn't touched)
# ---------------------------------------------------------------------
report = catalogue.rename(columns={'stock': 'units_in_stock'}).drop(columns=['supplier'])
print("8. Tidied copy ('report'):")
print(report.head(3))
print()
print("catalogue's columns are unchanged:", list(catalogue.columns))
