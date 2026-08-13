# Conference Attendee Data Cleaning

## Why this project exists

Real-world exports are messy. This one simulates a conference attendee list
pulled straight out of a registration system: names typed in every possible
case, emails with stray spaces, prices stored as text with currency symbols
and thousands separators, and company sizes spelled out in half a dozen
inconsistent ways ("SME", "Sme", "startup", "Corp", "Enterprise"...).

None of that is usable for analysis as-is. You can't sum a column of strings
like `"£1,499.00"`, you can't group by company size when "Small" is written
five different ways, and you can't trust an average that's being dragged
around by a typo or a genuinely huge outlier ticket.

The goal of this project is **not** to analyze the data — it's to get the
data into a shape where analysis is actually possible. That's most of the
real work in any data project, and it's the part that's easy to skip past.
So this script walks through the standard pandas cleaning playbook step by
step: strip and normalize text, fix data types, collapse inconsistent
categories, and flag outliers before they quietly distort your summary
statistics.

## What the script does

The raw data lives inline in the script as a CSV string (`attendee_csv`), so
there's nothing to download — just run it. The pipeline goes through eight
steps:

1. **Clean names and companies** — `.str.strip()` removes stray leading and
   trailing whitespace, `.str.title()` normalizes casing (`"jane DOE "` →
   `"Jane Doe"`).
2. **Clean emails** — strip whitespace and lower-case everything, since
   emails should be compared/matched case-insensitively.
3. **Split full names** — `attendee_name` is split into `first_name` and
   `family_name` using `.str.split(' ', expand=True)`.
4. **Fix ticket prices** — prices arrive as text like `"£1,499.00"`. The `£`
   symbol and thousands comma are stripped out with `.str.replace()`, then
   `pd.to_numeric()` converts the result to an actual float column so it can
   be summed, averaged, and binned.
5. **Tidy company size** — strip/title-case the text first, then use
   `.replace()` with a dictionary to collapse all the variants
   (`Sme`, `Small`, `Startup` → `"Small"`; `Corp`, `Enterprise` → `"Large"`).
   `value_counts()` is printed both before and after so you can see the
   cleanup actually happening.
6. **Make company size an ordered category** — `pd.Categorical(...,
   categories=['Small', 'Medium', 'Large'], ordered=True)` turns the column
   into a proper ordinal type, which means comparisons like
   `company_size >= 'Medium'` just work.
7. **Band ticket prices into tiers** — `pd.cut()` splits `ticket_price` into
   `"Standard"` (≤£300), `"Business"` (≤£800), and `"VIP"` (>£800) buckets,
   stored in a new `ticket_tier` column.
8. **Flag outliers** — the classic 1.5 × IQR rule (Q1 − 1.5·IQR to
   Q3 + 1.5·IQR) is applied to `ticket_price` to catch any values that are
   unusually far from the rest of the distribution.

## Libraries used

- **pandas** — does essentially all the work here: string cleaning
  (`.str.strip`, `.str.title`, `.str.replace`, `.str.split`), type conversion
  (`pd.to_numeric`), category handling (`pd.Categorical`), and binning
  (`pd.cut`).
- **numpy** — used for `np.inf` as the open-ended upper bound in the
  `pd.cut()` bins (the VIP tier has no ceiling).
- **io** — `io.StringIO` lets the CSV text be read with `pd.read_csv()` as
  if it were a file, so the script is self-contained and needs no external
  data file.

## Results

Running the script on this sample of 12 attendees:

- **Total ticket revenue:** £10,441.00, once prices were converted from text
  to numbers.
- **Company size, before cleaning:** 6 different spellings in the data
  (`Medium`, `Sme`, `Enterprise`, `Startup`, `Corp`, `Small`).
  **After cleaning:** collapsed down to the intended 3 categories —
  5 Small, 3 Medium, 4 Large.
- **Attendees from Medium-or-larger companies:** 7, made possible by
  the ordered category comparison (`company_size >= 'Medium'`).
- **Ticket tiers:** 4 Standard, 6 Business, 2 VIP.
- **Outlier detected:** Tom Baker (Umbrella Corp) at £3,999.00 — well above
  the IQR upper bound of £1,549.00, and roughly 5x the price of a typical
  ticket.
- **Average ticket price:** £870.08 including that outlier, vs. £585.64
  with it excluded — a good reminder of how much a single bad (or simply
  extreme) data point can distort a mean.

## How to run it

```bash
pip install -r requirements.txt
python clean_attendees.py
```

The script prints its progress at each cleaning step, so you can follow
along and see the data change shape as it runs.
