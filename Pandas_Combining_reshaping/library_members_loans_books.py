"""
Pandas: Combining and Reshaping:
================================
In this project you will learn:

    How to stack tables on top of each other with pd.concat()
    How to join two tables on a shared key with pd.merge(), and what how= changes
    How to spot rows whose key did not match, using indicator=True
    How to summarise several columns at once with groupby().agg() and named aggregations
    How to build a cross-tab with pivot_table(), and how to unpivot with melt()


Project overview:
================================
A library has three tables: loans, members and books. Some loans refer to a member who is no longer on file, and one member has never borrowed anything.

    1. Stack loans_q1 and loans_q2 into a single loans table with pd.concat(), using ignore_index=True. Print how many rows you ended up with.
    2. Left-join loans onto members on member_id, keeping every loan. Print how many loans ended up with no member name.
    3. Repeat the join with how='outer' and indicator=True, and print which member has never borrowed a book.
    4. Merge the result of step 2 with books on book_id so every loan also carries its title and genre.
    5. With groupby().agg() and named aggregations, build a per-genre summary containing: the number of loans (count of loan_id), the number of distinct members (nunique of member_id), and the average days_kept. Sort it by loan count, highest first.
    6. Build a pivot_table() of the number of loans, with genre down the side and branch across the top, filling gaps with 0.
    7. Melt the wide monthly_visits table into long form with columns branch, month and visits, then print total visits per month.
"""

import pandas as pd

members = pd.DataFrame({
    'member_id': ['M1', 'M2', 'M3', 'M4', 'M5'],
    'member_name': ['Alice Johnson', 'Bob Smith', 'Carol White', 'Dan Brown', 'Eve Davis'],
    'branch': ['Central', 'North', 'Central', 'South', 'North'],
})

books = pd.DataFrame({
    'book_id': ['B1', 'B2', 'B3', 'B4', 'B5'],
    'title': ['Dune', 'Wolf Hall', 'Sapiens', 'The Hobbit', 'Bad Blood'],
    'genre': ['Sci-Fi', 'Historical', 'Non-Fiction', 'Fantasy', 'Non-Fiction'],
})

loans_q1 = pd.DataFrame({
    'loan_id': ['L1', 'L2', 'L3', 'L4'],
    'member_id': ['M1', 'M2', 'M1', 'M3'],
    'book_id': ['B1', 'B3', 'B4', 'B2'],
    'days_kept': [14, 21, 7, 28],
})

loans_q2 = pd.DataFrame({
    'loan_id': ['L5', 'L6', 'L7', 'L8'],
    'member_id': ['M4', 'M9', 'M2', 'M3'],
    'book_id': ['B5', 'B1', 'B3', 'B5'],
    'days_kept': [10, 35, 18, 12],
})

monthly_visits = pd.DataFrame({
    'branch': ['Central', 'North', 'South'],
    'Jan': [820, 610, 430],
    'Feb': [790, 655, 470],
    'Mar': [910, 700, 505],
})

# 1. Stack loans_q1 and loans_q2 into `loans`:
loans = pd.concat([loans_q1, loans_q2], ignore_index=True)
print(loans)
print(f"\n.1 Combined loans: {len(loans)}")
print()

# 2. Left-join loans onto members on member_id; count loans with no member name:
join_loans = pd.merge(loans, members, on='member_id', how='left')
print(f"Number of loans without member: {join_loans['member_name'].isna().sum()}")
print(f"\n.2 Loans with no member: {join_loans[join_loans['member_name'].isna()]}")
print()

# 3. Outer join with indicator=True; which member has never borrowed?
outer_join = pd.merge(loans, members, on='member_id', how='outer', indicator=True)
print(f"Members who never borrowed: {outer_join['loan_id'].isna().sum()}")
print(outer_join['_merge'].value_counts)
print(f"\n.3 Member who never borrowed:")
print(outer_join.loc[outer_join['_merge']== 'right_only'])
print()

# 4. Merge in `books` on book_id so every loan carries title and genre:
full = pd.merge(join_loans, books, on='book_id', how='left')
print("\n.4 Merged books with title and genre:")
print(full[['loan_id', 'member_name', 'book_id', 'title', 'genre', 'days_kept']].head(6))
print()

# 5. Per-genre summary: loan count, distinct members, average days_kept.
#    Sort by loan count, highest first:
pre_genre_summary = full.groupby('genre').agg(loan_count=('loan_id', 'count'), 
                                              distinct_members=('member_id', 'nunique'), 
                                              avrerage_days_kept= ('days_kept','mean')).round(2).sort_values('loan_count', ascending=False)
print(f"Pre-genre summary:")
print(pre_genre_summary)
print()

# 6. pivot_table: number of loans, genre down the side, branch across the top:
grid=pd.pivot_table(full, values='loan_id', index='genre', columns='branch', aggfunc='count', 
                    fill_value=0, margins=True, margins_name='Total')
print("\n.6 Pivot table:")
print(grid)
print()
# 7. Melt monthly_visits to long form, then total the visits per month:

long_visits = monthly_visits.melt(id_vars='branch', var_name='months', value_name='visits')
print("Visits per month long list:")
print(long_visits)
print("\n.7 Total visits per month:")
print(long_visits.groupby('months')['visits'].sum())