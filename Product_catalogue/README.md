# Product Catalogue Analysis with Pandas

If you're new to working with tables of data in Python, this little project
is meant to be a clear, practical example of one of the most important
skills you'll use over and over again: **getting at the exact rows and
columns you need, and filtering data down to what actually matters.**

Most real-world data work isn't complicated math — it's things like "give
me just these four rows," "show me only the products in this category," or
"update the price, but only for the items that match this condition."
Pandas (the main Python library for working with tables of data) gives you
a small set of tools that make all of this fast and readable, and this
project walks through the most useful ones using a tiny, easy-to-follow
example: a shop's product catalogue with eight items split between two
categories, Kitchen and Garden.

By the end of the script, you'll have seen how to:
- Pull out a specific block of a table by position
- Turn a column into a meaningful row label so you can look things up by
  name/ID instead of by row number
- Grab an entire row using that label
- Filter rows by a condition and pick out just the columns you want
- Apply an edit to only the rows that match a condition — no loop needed
- Combine multiple filter conditions in a readable way
- Count how many rows fall into each category
- Create a cleaned-up copy of your data without touching the original

## Questions this project answers

The script is broken into eight small, numbered examples, each one built
around a question you'd genuinely ask when exploring a table of data:

1. **How do I grab a specific chunk of rows and columns by their position?**
   Uses `.iloc[]` to pull the first 4 rows and first 3 columns, regardless
   of what they're labeled.
2. **How do I turn a column into a meaningful row label?**
   Sets `product_code` as the index, so from here on every row can be
   looked up by its product code instead of by row number.
3. **How do I retrieve one full record by its label?**
   Uses `.loc[]` to pull everything we know about product `P004` in one
   line.
4. **How do I filter rows by a condition and only keep certain columns?**
   Finds every product in the "Kitchen" category and shows just their name
   and price.
5. **How do I edit only the rows that match a condition, without a loop?**
   Applies a 20% price cut to every "Garden" product in a single line, and
   confirms it worked by printing the updated Garden prices.
6. **How do I filter on more than one condition at once, readably?**
   Uses `.query()` to find products that are both expensive (≥ 30) and
   well-stocked (≥ 20 units) — read almost like a plain English sentence.
7. **How many products fall into each category?**
   A quick one-line count of Kitchen vs. Garden products.
8. **How do I create a cleaned-up copy of my data without wrecking the
   original?**
   Builds a `report` table with a renamed column and one column dropped —
   then proves the original `catalogue` table was left completely
   untouched.

## Tools and libraries used

- **Python 3** — the programming language everything is written in.
- **[pandas](https://pandas.pydata.org/)** — the library that does all the
  heavy lifting: reading tabular data, indexing, filtering, and editing it.
  This is the only external library the project depends on.
- **`io` (built into Python)** — specifically `io.StringIO`, which is used
  to treat a plain text string as if it were a CSV file. This means the
  project needs no external data file and no internet connection; the
  "dataset" lives right inside the script as a string and is read into a
  DataFrame with `pandas.read_csv()`.
- **[Thonny](https://thonny.org/)** — a simple, beginner-friendly Python
  editor. The script in this repo was written and tested to run cleanly in
  Thonny with no setup beyond installing pandas, but it will run in any
  Python environment (VS Code, PyCharm, plain terminal, Jupyter, etc.).

## Files in this repository

| File | Purpose |
|---|---|
| `product_catalogue_analysis.py` | The full script — open and run this in Thonny (or any Python environment) |
| `requirements.txt` | Lists the one dependency (`pandas`) so you can install it in one command |
| `.gitignore` | Keeps common Python/editor clutter out of version control |
| `README.md` | This file |

## How to run it

1. Make sure you have Python 3 installed.
2. Install pandas:
   ```bash
   pip install -r requirements.txt
   ```
   (In Thonny: **Tools → Manage Packages**, search for `pandas`, and
   install it.)
3. Open `product_catalogue_analysis.py` in Thonny (or your editor of
   choice) and run it — in Thonny that's the green **Run** button or
   pressing **F5**.
4. Everything happens in the console/Shell — you'll see each of the eight
   questions answered in turn, with a short label above each result so
   it's clear what you're looking at.

No data files, downloads, or extra setup required — the entire dataset is
built into the script.

## A note on the two key pandas tools used throughout

- **`.iloc[]`** selects data by **position** — "give me row 0 through 3,
  column 0 through 2" — the same way you might slice a list.
- **`.loc[]`** selects data by **label** — "give me the row labeled
  `P004`," or "give me every row where this condition is true." This is
  the one you'll reach for most often once your data has a meaningful
  index (like a product code, an ID, or a name).

Getting comfortable with the difference between these two — and with
`.query()` as a more readable alternative for multi-condition filtering —
covers a huge share of what you'll actually do day-to-day when working
with tabular data in pandas.
