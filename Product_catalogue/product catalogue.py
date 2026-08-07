import pandas as pd
import io

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
# 1. First 4 rows and first 3 columns, using .iloc:
print("1. First 4 rows and 3 columns:")
print(f"{products.iloc[0:4, 0:3]}")
print()
# 2. Move product_code into the index -> catalogue:
print("2. product_code becomes index:")
catalogue = products.set_index('product_code')
print(f"{catalogue}")
print()
# 3. The whole row for P004, using .loc:
print("3. The whole row for P004:")
print(catalogue.loc['P004'])
print()
# 4. name and price of every Kitchen product, using a mask inside .loc:
print("4. Name and price pf every kitchen product:")
print(catalogue.loc[catalogue['category'] == 'Kitchen', ['name', 'price']])

# 5. Reduce every Garden price by 20% in a single .loc assignment:
print("5. 20% discount on Garden items:")
catalogue.loc[catalogue['category'] == 'Garden', 'price'] *= 0.80
print(catalogue.loc[catalogue['category'] == 'Garden', ['name', 'price']])
print()

# 6. .query(): costs more than 30 AND more than 20 in stock:
print("6. Costs more than 30, and stocks more than 20")
print(catalogue.query('price >= 30 and stock >= 20')[['name', 'price', 'stock']])
print()

# 7. Count the products in each category:
print("Number of products in each category:")
print(catalogue.value_counts('category'))
print()

# 8. Tidied copy 'report': rename stock -> units_in_stock, drop supplier:
#    Then confirm catalogue still has its supplier column:
report = catalogue.rename(columns={'stock': 'units_in_stock'}).drop(columns=['supplier'])
print("Tidied copy:")
print(report.head(3))
print(list(catalogue.columns))