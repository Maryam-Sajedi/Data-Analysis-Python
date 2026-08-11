"""
Project overview:
A gym has exported its membership list, and it is a mess: blank cells, unknown and ?? used as missing markers, two rows imported twice, an age written as a word, and join dates stored as text.

Clean it, in this order:

    1. Read messy_members.csv with read_csv, declaring unknown and ?? as missing markers via na_values.
    2. Print the number of missing values in each column, and the dtype of each column.
    3. Remove exact duplicate rows, printing how many you removed.
    4. Convert age to a number with pd.to_numeric(errors='coerce'), and join_date to a real date with pd.to_datetime().
    5. Drop any row that has no member_id.
    6. Fill missing branch values with the string "Unknown".
    7. Fill missing monthly_fee values with the mean fee for that same membership_type (groupby(...).transform('mean')), and missing age values with the overall median age.
    8. Confirm there are no gaps left, then print the total monthly income (monthly_fee.sum()) formatted to two decimal places.
"""

import pandas as pd

members_csv = """member_id,name,age,membership_type,branch,monthly_fee,join_date
M001,Alice Johnson,34,Premium,Central,49.99,2023-03-14
M002,Bob Smith,unknown,Standard,North,29.99,2023-04-02
M003,Carol White,28,Premium,,49.99,2023-04-19
M004,Dan Brown,45,Standard,North,,2023-05-07
M005,Eve Davis,thirty,Standard,Central,29.99,2023-05-21
M006,Frank Miller,52,Premium,South,54.99,2023-06-11
M006,Frank Miller,52,Premium,South,54.99,2023-06-11
M007,Grace Wilson,23,Student,North,19.99,2023-07-03
M008,Henry Moore,38,Premium,??,,2023-07-28
,Unknown Person,41,Standard,Central,29.99,2023-08-15
M009,Ivy Clark,19,Student,South,19.99,2023-09-01
M010,Jack Lewis,,Standard,Central,32.99,2023-09-30
M010,Jack Lewis,,Standard,Central,32.99,2023-09-30
M011,Kate Ellis,61,Premium,North,49.99,2023-10-12
"""

with open('messy_members.csv', 'w') as f:
    f.write(members_csv)

# 1. Read the file, declaring 'unknown' and '??' as missing markers:
members = pd.read_csv('messy_members.csv', na_values=['unkown', '??'])

# 2. Print the missing-value count per column, and the dtypes:
print(f"Count the missing values: {members.isna().sum().sum()}")
print(f"Data types: {members.dtypes}")
print()

# 3. Remove exact duplicate rows, reporting how many went:
print(f"Before removing duplicates: {len(members)}")
print(f"Duplicate counts:{members.duplicated().sum()}")
members = members.drop_duplicates()
print(f"After dropping duplicates:")
print(len(members))

# 4. Convert age to numeric (coerce) and join_date to datetime:
members['age'] = pd.to_numeric(members['age'], errors= 'coerce')
members['join_date'] = pd.to_datetime(members['join_date'])
print(f"Age is now: {members['age'].dtypes}, and join_date is now: {members['join_date'].dtypes}")
# 5. Drop rows with no member_id:
before = len(members)
members = members.dropna(subset=['member_id'])
after = len(members)
print(f"Droped: {before - after}")

# 6. Fill missing branch values with "Unknown":
members['branch'] = members['branch'].fillna('Unknown')
print(f"\n Branches: {sorted(members['branch'].unique())}")

# 7. Fill missing monthly_fee from the mean fee of the same membership_type,
#    and missing age with the overall median age:
mean_fee= members.groupby('membership_type')['monthly_fee'].transform('mean')
members['monthly_fee'] = members['monthly_fee'].fillna(mean_fee)
median_age = members['age'].median()
members['age'] = members['age'].fillna(median_age)
print(f"Fees filled with mean saleries: {members.groupby('membership_type')['monthly_fee'].mean().round(2)}")

# 8. Confirm no gaps remain, then print the total monthly income:
print(members.isna().sum().sum())
print(len(members))
print(f"Total monthly income: {members['monthly_fee'].sum().round(2)}€")