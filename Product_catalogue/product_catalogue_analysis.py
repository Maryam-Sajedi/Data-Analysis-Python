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
    
Introduction:

Pandas: Selecting Data with .loc and .iloc¶

What you will learn:

    The difference between label-based selection (.loc) and position-based selection (.iloc)
    How to select rows and columns at the same time
    Why .loc slices include the last item but .iloc slices do not
    How to set a meaningful index with set_index() and undo it with reset_index()
    How to change values safely, and what .copy() protects you from
    Three everyday helpers: .query(), .value_counts(), rename() / drop()

io.StringIO(csv_data) wraps a string in memory so it behaves like a file object — it lets you treat a string as if it were a text file, without ever writing anything to disk.

Concretely: things like pandas.read_csv() normally expect a file path or a file-like object (something with .read(), seek, etc.). If you already have your CSV data sitting in a Python string (e.g. you fetched it with requests, or it's a hardcoded string, or you built it programmatically), you can't pass that string straight to pd.read_csv() — you need to wrap it in StringIO first so pandas can "read" from it like a file.
Two ways to point at a row

In lesson 30 you selected columns with df['city'] and rows with a boolean filter. That covers a lot, but it cannot express "give me the fourth row" or "give me rows 2 to 5 and only the name and salary columns".

Pandas gives you two selectors for that, and the difference between them matters:
Selector 	Selects by 	Example
.iloc 	position — where the row sits, counting from 0 	df.iloc[3] is the 4th row
.loc 	label — what the row is called in the index 	df.loc['E004'] is the row labelled E004
    
Project overview:

Here is a product catalogue. Work through the steps using .loc, .iloc and the helpers from this lesson.

products = pd.read_csv(io.StringIO(product_csv))

    Print the first 4 rows and only the first three columns, using .iloc.
    Move product_code into the index with set_index(), storing the result in catalogue.
    Print the whole row for product code P004 using .loc.
    Print the name and price of every product in the Kitchen category, using a boolean mask inside .loc.
    Everything in the Garden category is on sale: reduce its price by 20% with a single .loc assignment.
    Use .query() to find products that cost more than £30 and have more than 20 in stock.
    Print how many products are in each category with .value_counts().
    Make a tidied copy called report with stock renamed to units_in_stock and the supplier column dropped. Confirm catalogue still has its supplier column.  
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
