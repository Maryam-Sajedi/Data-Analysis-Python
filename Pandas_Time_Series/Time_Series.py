"""
Pandas: Time Series
=======================================
Goals: Learning Pandas Time Series and:

    How to turn a text date column into real dates and put them in the index
    How to pull the year, month or weekday out of a date with the .dt accessor
    How to select a month or a date range by writing it as a string
    How to change the frequency of data with resample() — daily to monthly, and so on
    How to smooth a noisy series with rolling(), and measure change with shift() and pct_change()
======================================
Example 1:
Building a year of daily sales:
======================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Example 1: build a year of daily sales ---

np.random.seed(0)

dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')

# A realistic-looking series: a gentle upward trend, a weekend bump, and noise
trend = np.linspace(500, 800, len(dates))
weekend_bump = np.where(dates.dayofweek >= 5, 180, 0)   # Sat=5, Sun=6
december_rush = np.where(dates.month == 12, 250, 0)
noise = np.random.normal(0, 60, len(dates))

sales = pd.DataFrame({
    'date': dates,
    'revenue': (trend + weekend_bump + december_rush + noise).round(2),
})

print(sales.head())
print()
print(f"date column dtype: {sales['date'].dtype}")
print(f"Rows: {len(sales)}")


"""
=============================
Example 2:
==============================

Below is two years of daily electricity readings for a small factory. Work through the time-series toolkit on it.

    1. Convert reading_date to real dates with pd.to_datetime(), then set it as the index of a DataFrame called power.
    2. Add a weekday column from the index (power.index.day_name()) and print the average kwh per weekday, reordered Monday → Sunday.
    3. Use partial-string selection to print the total kwh for July 2024 and for the range 2023-11 to 2024-01.
    4. Resample to monthly totals with 'MS' and print the result.
    5. Resample to quarterly averages with 'QS'.
    6. Add a 30-day moving average column called ma_30, and plot the raw daily kwh against it on the same axes, with labels, a title and a legend.
    7. Build a monthly report using shift() and pct_change() showing each month's total, the previous month's total, and the percentage change. Print the month with the largest percentage fall.
    
    """

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates   # changing dates in the graphs to a desired form
import os

np.random.seed(7)

reading_dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')

# Higher usage in winter, lower at weekends, plus noise:
seasonal = 400 + 150 * np.cos(2 * np.pi * (reading_dates.dayofyear / 365))
weekend_drop = np.where(reading_dates.dayofweek >= 5, -120, 0)
noise = np.random.normal(0, 35, len(reading_dates))

readings = pd.DataFrame({
    'reading_date': reading_dates.strftime('%Y-%m-%d'),   # deliberately TEXT
    'kwh': (seasonal + weekend_drop + noise).round(1),
})

print(readings.head())
print(f"reading_date dtype: {readings['reading_date'].dtype}  <-- not a date yet")

# 1. Convert reading_date to datetime and set it as the index -> `power`:
print()
readings['reading_date'] = pd.to_datetime(readings['reading_date'])
power = readings.set_index('reading_date')
print(f"\n.1 Index is now a {type(power.index).__name__} with {len(power)} rows.:")
print(power)


# 2. Add a weekday column from the index; print average kwh per weekday,
#    ordered Monday -> Sunday:

power['weekday'] = power.index.day_name()
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
power_weekday = power.groupby('weekday')['kwh'].mean()
print("\n.2 Average kwh per weekday:")
print(power_weekday.reindex(weekday_order).round(2))
print()

# 3. Total kwh for July 2024, and for 2023-11 to 2024-01:
July_power = power.loc['2024-07', 'kwh'].sum()
winter_power = power.loc['2023-11' : '2024-01', 'kwh'].sum()
print("\n.3 Total kwh for July 2024 and winter 23-24:")
print(f"\n.3 July: {July_power:,.2f} kwh, and winter: {winter_power:,.2f} kwh")
print()

# 4. Monthly totals with resample('MS'):
monthly_totals = power.resample('MS')['kwh'].sum().round(2)
print(f"\n.4 Monthly totals: {monthly_totals.head(5)}")
print()

# 5. Quarterly averages with resample('QS'):
quarterly_average = power.resample('QS')['kwh'].mean().round(2)
print(f"\n.5 Quarterly average: {quarterly_average}")
print()

# 6. Add a 30-day moving average `ma_30` and plot it over the raw daily series:
power['ma_30'] = power['kwh'].rolling(30).mean()

print("\n.6 Power cunsumption over two years:")

plt.figure(figsize=(11, 7))
plt.plot(power['kwh'], linewidth=0.8, color='steelblue',label='Daily kwh')
plt.plot(power['ma_30'], linewidth=2, color='orange', label='30-day moving avrg')
plt.xlabel('Date')
plt.ylabel('Power (kwh)')
plt.title('Power cunsumption over two years')
plt.legend()

# --- format the x-axis date labels ---
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))   # one tick every 3 months
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))   # e.g. "January 2023"
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
os.makedirs('images', exist_ok=True)
plt.savefig('images/power_consumption.png', dpi=150)  # <-- saves the figure to disk
plt.show()
print()

# 7. Monthly report with shift() and pct_change(); print the biggest percentage fall:
report= monthly_totals.to_frame(name='kwh')
report['previous'] =report['kwh'].shift(1)
report['pct_change'] = (report['kwh'].pct_change() * 100).round(2)
print("\n.7 Monthly report:")
print(report.head(6))
worst = report['pct_change'].idxmin()
print()
print("Biggest fall:")
print(f"Biggest fall: {worst.strftime('%B %Y')}, at {report.loc[worst, 'pct_change']}%")
















