"""
Seaborn: Statistical Visualisation:

Seaborn is usually quicker than plain Matplotlib for charting a DataFrame.

In this project we will:

    -Learn how to load seaborn's built-in example datasets with sns.load_dataset()
    -Distributions with histplot and kdeplot; comparisons with barplot, countplot, boxplot and violinplot
    -Relationships with scatterplot, and how hue, size and style add extra variables
    -The difference between axes-level and figure-level functions, and how to facet a chart into a grid with relplot and catplot
    -Correlation heatmaps with sns.heatmap()

=============================
Project overview:
=============================
You are given a year of café transactions (generated below — no download needed). Use seaborn to explore it.

    1. Call sns.set_theme() with the style of your choice.
    2. Plot the distribution of amount as a histogram with a KDE curve overlaid.
    3. On a second chart, use kdeplot with hue='category' to compare the amount distributions of the three categories.
    4. Draw a countplot of transactions per weekday, with the days in Monday → Sunday order (hint: pass order=).
    5. Draw a boxplot of amount by category, with hue='member'. Which category has the widest spread?
    6. Draw a scatterplot of items against amount, coloured by category and sized by queue_minutes. Add a regplot trend line on a second axes beside it.
    7. Use catplot with kind='bar', x='weekday', y='amount' and col='category' to facet the mean spend per weekday across the three categories. Give the figure a title with g.figure.suptitle().
    8. Build a pivot_table() of mean amount with weekday down the side and category across the top, and draw it as an annotated heatmap.
    9. Draw a correlation heatmap of the numeric columns using coolwarm and center=0.
    
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------------
# Output folder for figures:
# ---------------------------------------------------------------
# Path(__file__).parent = the folder this script lives in, so the
# images always land next to the script regardless of the working
# directory Thonny happens to be using.
from pathlib import Path

IMAGES = Path(__file__).parent / "images"
IMAGES.mkdir(exist_ok=True)

def save(fig, name):
    fig.savefig(IMAGES / f"{name}.png", dpi=150, bbox_inches="tight")
    print(f"saved -> {name}.png")

np.random.seed(21)

# Data generation:
n = 600
dates = pd.to_datetime('2024-01-01') + pd.to_timedelta(np.random.randint(0, 365, n), unit='D')
category = np.random.choice(['Coffee', 'Lunch', 'Bakery'], n, p=[0.5, 0.3, 0.2])

base = {'Coffee': 3.2, 'Lunch': 8.5, 'Bakery': 4.0}
items = np.where(category == 'Lunch',
                 np.random.randint(1, 4, n),
                 np.random.randint(1, 6, n))
amount = np.array([base[c] for c in category]) * items + np.random.normal(0, 1.2, n)

weekday = dates.day_name()

cafe = pd.DataFrame({
    'date': dates,
    'weekday': weekday,
    'category': category,
    'items': items,
    'amount': amount.round(2).clip(1.0),
    'queue_minutes': np.random.gamma(2.0, 1.6, n).round(1),
    'member': np.random.choice(['Yes', 'No'], n, p=[0.35, 0.65]),
})

weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                 'Friday', 'Saturday', 'Sunday']

print(cafe.groupby('weekday')['amount'].mean().reindex(weekday_order).round(0).head())
print()
print(cafe.head())
print(f"\nShape: {cafe.shape}")

# 1. Set a seaborn theme:
sns.set_style(style='whitegrid')

# 2. Histogram of `amount` with a KDE curve:
fig, axes = plt.subplots(1, 2, figsize=(15,5))

sns.histplot(data=cafe, x='amount', kde=True, bins=30, color='steelblue', ax=axes[0])

axes[0].set_xlabel('Amount €')
axes[0].set_ylabel('counts')
axes[0].set_title('Distribution of transaction amount')

# 3. kdeplot of `amount` with hue='category':
sns.kdeplot(data=cafe, x='amount', hue='category', alpha=0.4, fill=True, ax=axes[1])

axes[1].set_xlabel('Amount €')
axes[1].set_title('Distribution of amount by category')

plt.tight_layout()
save(fig, "01_distributions")
plt.show()

# 4. countplot of transactions per weekday, in Monday -> Sunday order:
fig, axes= plt.subplots(1, 2, figsize=(15, 5))

sns.countplot(data=cafe, x='weekday', order=weekday_order, ax=axes[0])

axes[0].set_xlabel('Weekday')
axes[0].set_title('Transcations per weekday')
axes[0].tick_params(axis='x', rotation=45)


# 5. boxplot of amount by category, with hue='member':
sns.boxplot(data=cafe, x='category', y='amount', hue='member', ax=axes[1])

axes[1].set_xlabel('Category')
axes[1].set_title('Amount by category and membership')

plt.tight_layout()
save(fig, "02_boxplot_amount_by_cat")
plt.show()

# Widest spread:
spread = cafe.groupby('category')['amount'].agg(['median', 'std']).round(2)
print("Widest spread:")
print(spread['std'].idxmax())

                     
# 6. scatterplot of items vs amount (hue=category, size=queue_minutes),
#    plus a regplot trend line beside it:
fig, axes= plt.subplots(1,2, figsize=(15,5))

sns.scatterplot(cafe, x='items', y='amount', hue='category', size='queue_minutes', sizes=(20, 200), alpha=0.5, ax=axes[0])
axes[0].set_title('Items vs amount €')
axes[0].set_xlabel('Items')
axes[1].set_ylabel('Amount €')

sns.regplot(data=cafe, x='items', y='amount', scatter_kws={'alpha': 0.5}, line_kws={'color': 'crimson'}, ax=axes[1])
axes[1].set_title('Items vs amount with their trend line fit')
axes[1].set_xlabel('Items')
axes[1].set_ylabel('Amount €')

plt.tight_layout()
save(fig, "03_scatterplot_item_vs_amount")
plt.show()

print()
print("Correlation between items and amount:")
print(cafe['items'].corr(cafe['amount']).round(3))
print()
# 7. catplot: kind='bar', x='weekday', y='amount', col='category', with a suptitle:
g= sns.catplot(data=cafe, x='weekday', y='amount', kind='bar', col='category', order=weekday_order, height=5, aspect=1.1
    
)

g.set_axis_labels('Weekday', 'Amount €')
g.set_xticklabels(rotation=45)
g.figure.suptitle('Amount spend per week by category')
plt.tight_layout()
save(fig, "04_Facet_weekday by category")
plt.show()



# 8. pivot_table of mean amount (weekday down, category across) as an annotated heatmap:
fig, axes= plt.subplots(1,2, figsize=(15, 5))

grid=cafe.pivot_table(values='amount', index='weekday', columns='category', aggfunc='mean', fill_value=0)
grid= grid.reindex(weekday_order)  # calendar order,

sns.heatmap(grid, annot=True, fmt='.2f', cmap='YlGnBu', ax=axes[0])
axes[0].set_xlabel('Weekday')
axes[0].set_title('Mean amount by weekday and category (€)')

# 9. Correlation heatmap of the numeric columns:
correlations = cafe.select_dtypes('number').corr()

sns.heatmap(correlations, annot=True, fmt='.2f', cmap='coolwarm', center=0, square=True, ax=axes[1])
axes[1].set_title('Correlation between numeric columns')

plt.tight_layout()
save(fig, "05_heatmap_grid_correlations")
plt.show()