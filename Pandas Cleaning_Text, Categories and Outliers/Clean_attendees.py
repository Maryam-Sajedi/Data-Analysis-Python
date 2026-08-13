"""
Goals: Cleaning data — Text, Categories and Outliers:

Project Overview

A conference has exported its attendee list. The names and job titles have inconsistent spacing and casing, the ticket prices are text with currency symbols, and the company sizes are written several different ways.

    Clean attendee_name and company: strip the spaces and apply title case.
    Clean email: strip the spaces and lower-case it.
    Split attendee_name into new first_name and last_name columns.
    Convert ticket_price from text to a number (remove the £ and the thousands comma, then pd.to_numeric). Print the total ticket revenue.
    Tidy company_size: strip and title-case it, then use .replace() with a mapping to collapse Sme, Small, Startup into "Small", and Corp, Enterprise into "Large". Print the value_counts() before and after.
    Convert company_size to an ordered category with the order Small < Medium < Large.
    Band ticket_price with pd.cut() into "Standard" (up to £300), "Business" (up to £800) and "VIP" (above), in a column called ticket_tier.
    Use the 1.5 × IQR rule on ticket_price to find outliers, and print them.
"""

import pandas as pd
import numpy as np
import io

attendee_csv = """attendee_id,attendee_name,company,email,company_size,ticket_price
A01,  jane DOE ,acme ltd,Jane.Doe@ACME.com ,SME,£299.00
A02,JOHN smith,  Globex ,john@globex.com,enterprise,£799.00
A03, sara connor,Initech,SARA@initech.COM ,startup,£299.00
A04,mike ROSS  ,ACME LTD,mike@acme.com,sme,"£1,499.00"
A05,  Nina Patel,Umbrella Corp ,nina@UMBRELLA.com,corp,£799.00
A06,omar hassan ,globex,omar@Globex.COM ,Medium,£450.00
A07,PRIYA sharma  ,initech ,priya@initech.com,SMALL,£299.00
A08, tom baker,Umbrella Corp,TOM@umbrella.com ,Corp,"£3,999.00"
A09,uma green,Acme Ltd ,uma@ACME.com,Medium,£450.00
A10,  victor lee ,GLOBEX,victor@globex.com ,Enterprise,£799.00
A11,wendy adams,Initech,WENDY@Initech.com,Startup,£299.00
A12,xavier moss ,umbrella corp,xavier@umbrella.COM,medium,£450.00"""

attendees = pd.read_csv(io.StringIO(attendee_csv))
print(attendees.head(4))

# 1. Clean attendee_name and company: strip + title case:
print()
attendees['attendee_name'] = attendees['attendee_name'].str.strip().str.title()
attendees['company'] = attendees['company'].str.strip().str.title()
print(f"\n.1 Cleaned names and companies:") 
print(attendees[['attendee_name', 'company']].head(4))

# 2. Clean email: strip + lower case:
attendees['email'] = attendees['email'].str.strip().str.lower()
print("\n.2 Cleaning emails:")
print(attendees[['attendee_name', 'email']].head(4))
print()

# 3. Split attendee_name into first_name and last_name:
attendees[['first_name', 'family_name']] = attendees['attendee_name'].str.split(' ', expand = True)
print("\n.3 Split attendee names:")
print(attendees[['attendee_name', 'first_name', 'family_name']].head(3))
print()

# 4. ticket_price -> number (drop the £ and the comma), then print total revenue:
attendees['ticket_price'] = attendees['ticket_price'].str.replace('£', '', regex = False)
attendees['ticket_price'] = attendees['ticket_price'].str.replace(',', '', regex = False)
attendees['ticket_price'] = pd.to_numeric(attendees['ticket_price'])
print("\n.4 Fixing the ticket prices:")
print(attendees['ticket_price'].dtype)
print(f"Total revenue: {attendees['ticket_price'].sum():,.2f} €")
print()

# 5. Tidy company_size, then collapse the variants with .replace().
#    Print value_counts() before and after:
attendees['company_size'] = attendees['company_size'].str.strip().str.title()
print(f"Company size before cleaning:") 
print(attendees['company_size'].value_counts())
uniformed = {'medium' : 'Medium',
            'sme' : 'Small',
             'Sme': 'Small',
            'SME' : 'Small',
            'small' : 'Small',
            'Corp': 'Large',
            'Enterprise' : 'Large',
            'Startup' : 'Small',
            }
attendees['company_size'] = attendees['company_size'].replace(uniformed)
print("Company size after cleaning:")
print(attendees['company_size'].value_counts())
print()
# 6. Make company_size an ORDERED category: Small < Medium < Large:
attendees['company_size'] = pd.Categorical(attendees['company_size'], 
                                           categories=['Small', 'Medium', 'Large'], 
                                           ordered = True
                                          )
print("After ordering the company sizes:")
print(list(attendees['company_size'].cat.categories))
print(f"Attendees from at least medium companies: {(attendees['company_size'] >= 'Medium').sum()}")
print()
# 7. Band ticket_price into Standard (<=300) / Business (<=800) / VIP (>800):
attendees['ticket_tier'] = pd.cut(attendees['ticket_price'], 
                                  bins=[0, 300, 800, np.inf], 
                                  labels=['Standard', 'Business', 'VIP'],
                                 )
    
print('Type of tickets:')
print(attendees[['attendee_name', 'ticket_price', 'ticket_tier']])
# 8. Find outliers in ticket_price using the 1.5 x IQR rule and print them:
q1 = attendees['ticket_price'].quantile(0.25)
q3 = attendees['ticket_price'].quantile(0.75)
iqr = q3 - q1

lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

normal = attendees['ticket_price'].between(lower, upper)
outliers= attendees.loc[~normal, ['attendee_name', 'company', 'ticket_price']].to_string(index= False)

print("Outliers:")
print(outliers)
print("Mean value of ticket prices without outliers:")
print(f"{attendees.loc[normal, 'ticket_price'].mean():,.2f} €")
