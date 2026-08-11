# Gym Membership Data Cleaning

Real data is almost never ready to use straight out of the box. Before you
can analyze anything — average revenue, member counts, trends over time —
you first have to deal with the boring-but-essential problem of **data
cleaning**: blank cells, inconsistent missing-value markers, duplicate
records, values stored as the wrong type, and gaps that need to be filled
sensibly rather than just deleted.

This project is a small, realistic example of exactly that process. It
takes a deliberately messy gym membership export and walks through
cleaning it up in a clear, repeatable sequence of steps, using pandas —
the standard Python library for working with tabular data.

## What you can learn from this project

If you're working through this project to learn, here's what each step is
teaching you:

- **How to tell pandas what "missing" looks like in your data.** Real
  exports don't always use a blank cell for missing data — this one uses
  the literal text `"unknown"` and `"??"` as stand-ins. You'll see how
  `na_values` in `read_csv()` lets you tell pandas "treat these specific
  strings as missing, not as real data."
- **How to audit a dataset before touching it.** Counting missing values
  per column (`.isna().sum()`) and checking column types (`.dtypes`)
  *before* cleaning anything is a habit worth building — it tells you
  exactly what you're dealing with and confirms your fixes worked
  afterward.
- **How to find and remove duplicate rows** with `.duplicated()` and
  `.drop_duplicates()`, and — just as importantly — how to report what you
  removed instead of silently discarding data.
- **How to force a column into the right type**, and what to do when some
  values genuinely can't convert. `pd.to_numeric(..., errors='coerce')`
  turns unconvertible values (like the age written as `"thirty"`) into
  missing values instead of crashing the whole script. `pd.to_datetime()`
  does the same job for text dates.
- **When to drop rows vs. when to fill them in.** A row with no
  `member_id` is useless as a record, so it gets dropped. A row with no
  `branch` is still a real, useful record, so it gets a placeholder
  (`"Unknown"`) instead of being thrown away. Knowing which situation
  calls for which approach is one of the most practical judgment calls in
  data cleaning.
- **How to fill in missing numbers *intelligently* instead of with a fixed
  placeholder.** Missing fees are filled with the **average fee for that
  same membership type** (a Premium member's missing fee is estimated
  from other Premium members, not from the whole gym) using
  `groupby(...).transform('mean')`. Missing ages are filled with the
  **overall median age** — median rather than mean, because it's less
  thrown off by unusually young or old outliers.
- **How to verify your cleaning actually worked**, by re-checking for
  missing values at the very end before trusting the data enough to
  calculate a real business number from it (total monthly income).

In short: this project is a compact tour of the standard first stage of
almost any real data project — read it in, understand what's wrong with
it, fix it deliberately and traceably, and confirm it's actually fixed
before you build anything on top of it.

## What the script does, step by step

1. Reads `messy_members.csv`, telling pandas that the text `"unknown"`
   and `"??"` mean "no data," not literal values.
2. Prints how many missing values are in each column, and each column's
   data type, to get a clear picture of the mess before touching it.
3. Finds and removes exact duplicate rows (two members were accidentally
   imported twice), printing how many were removed.
4. Converts `age` to a proper number (any non-numeric entry, like the
   age spelled out as `"thirty"`, becomes a missing value instead of
   causing an error) and `join_date` to a real date type.
5. Drops any row with no `member_id` — a record with no ID isn't usable.
6. Fills missing `branch` values with the placeholder `"Unknown"`.
7. Fills missing `monthly_fee` values with the **average fee for that
   member's membership type**, and missing `age` values with the
   **overall median age**.
8. Confirms there are no missing values left anywhere, then calculates
   and prints the gym's total monthly income.

## Tools and libraries used

- **Python 3** — the language everything is written in.
- **[pandas](https://pandas.pydata.org/)** — the only external library
  this project needs. It handles reading the CSV, detecting and counting
  missing values, removing duplicates, converting data types, filling
  gaps, and grouping/aggregating the data.
- **[Thonny](https://thonny.org/)** — a simple, beginner-friendly Python
  editor. This script was written and tested to run cleanly in Thonny
  with no setup beyond installing pandas, but it runs in any Python
  environment (VS Code, PyCharm, terminal, Jupyter, etc.).

No internet connection, external files, or extra setup are required — the
messy dataset is built into the script itself and written out to
`messy_members.csv` at the start, then read back in exactly the way a
real exported file would be.

## Files in this repository

| File | Purpose |
|---|---|
| `gym_membership_cleaning.py` | The full script — open and run this in Thonny (or any Python environment) |
| `requirements.txt` | Lists the one dependency (`pandas`) |
| `.gitignore` | Excludes the auto-generated CSV and common Python/editor clutter from version control |
| `README.md` | This file |

## How to run it

1. Make sure you have Python 3 installed.
2. Install pandas:
   ```bash
   pip install -r requirements.txt
   ```
   (In Thonny: **Tools → Manage Packages**, search for `pandas`, install.)
3. Open `gym_membership_cleaning.py` and run it — in Thonny that's the
   green **Run** button or **F5**.
4. Read the numbered output in the console — each step prints what it
   found and what it changed.

## Expected results

Running the script exactly as-is produces this output:

```
2. Missing values per column:
member_id          1
name                0
age                 3
membership_type     0
branch              2
monthly_fee         2
join_date           0

Total missing cells: 8

3. Rows before removing duplicates: 14
Exact duplicate rows found: 2
Rows after dropping duplicates: 12

4. Converted column types:
age is now: float64
join_date is now: datetime64[us]

5. Rows dropped for missing member_id: 1

6. Branches now present: ['Central', 'North', 'South', 'Unknown']

7. Average monthly fee by membership type (after filling gaps):
membership_type
Premium     51.24
Standard    30.99
Student     19.99

Overall median age used to fill missing ages: 36.0

8. Remaining missing cells: 0
Final row count: 11
Total monthly income: 420.14€
```

Starting from 14 messy rows, the script ends with **11 clean rows**, zero
missing values anywhere, and a final total monthly income of **420.14€**.

> **Note on column types:** depending on which pandas version you have
> installed, step 2's dtype output may show `object` instead of `str` for
> the text columns — both mean the same thing (a text column); pandas
> introduced a dedicated `str` dtype in newer versions. Either way, the
> important columns (`age`, `monthly_fee`, `join_date`) end up correctly
> typed as numbers and dates by the end of step 4.
