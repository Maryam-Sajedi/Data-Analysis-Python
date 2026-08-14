# Library Loans: Combining & Reshaping Data with Pandas

## The goal of this project:

Real data almost never lives in one tidy table. It's split across systems,
exported in batches, and scattered across sheets that need to be stitched
back together before you can ask any interesting questions of it. This
project simulates exactly that situation for a small library: loan records
are split across two quarterly exports, member details live in a separate
table, book details in another, and there's a wide "one column per month"
visits table that isn't structured the way you'd want for analysis.

The point of this project isn't the library itself — it's practicing the
core pandas skills you need any time you're pulling data together from more
than one source:

- **Stacking** tables that have the same columns but different rows
  (like two quarters of the same export).
- **Joining** tables that share a key but hold different columns (like
  loans and the members who made them).
- **Understanding what a join actually did** — which rows matched, which
  didn't, and why.
- **Summarizing** a merged table with grouped, named aggregations.
- **Reshaping** — turning a long table into a wide cross-tab, and a wide
  table into a long one — depending on what the analysis needs.

Along the way, the data has a couple of deliberate wrinkles: one loan
belongs to a member who isn't in the members table anymore (`M9`), and one
member (Eve Davis) has never borrowed a single book. These aren't bugs —
they're the kind of thing that shows up in real joins all the time, and
part of the exercise is learning how to *find* them instead of silently
losing or duplicating rows.

## What the script does, step by step

1. **Stack the two quarterly loan tables** — `pd.concat([loans_q1,
   loans_q2], ignore_index=True)` combines Q1 and Q2 into one `loans`
   table. `ignore_index=True` is used so the row numbers restart cleanly
   from 0 instead of keeping two overlapping sets of indices.

2. **Left-join loans onto members** — `pd.merge(loans, members,
   on='member_id', how='left')` keeps every loan, even ones whose
   `member_id` doesn't exist in the members table, and fills in `NaN` for
   the missing member details. Counting `NaN` in `member_name` tells you
   how many loans reference a member who isn't on file.

3. **Outer join with `indicator=True`** — repeating the join with
   `how='outer'` keeps rows from *both* sides, matched or not, and
   `indicator=True` adds a `_merge` column labelling each row `both`,
   `left_only`, or `right_only`. Filtering for `right_only` reveals the
   member who exists in the members table but has no loans at all.

4. **Bring in the books table** — a second `pd.merge()`, this time on
   `book_id`, attaches each loan's book title and genre so the loans table
   now tells a complete story: who borrowed what, for how long, and from
   which genre.

5. **Per-genre summary with named aggregations** —
   `groupby('genre').agg(...)` with named aggregations builds one row per
   genre showing the number of loans, the number of *distinct* members who
   borrowed from that genre (`nunique`), and the average number of days
   books were kept, sorted with the most-borrowed genre first.

6. **Cross-tab with `pivot_table()`** — reshapes the merged loans into a
   grid with genre down the side and branch across the top, counting loans
   in each combination and filling any empty combination with `0` instead
   of `NaN`. Margins are included so row/column totals are visible too.

7. **Unpivot with `melt()`** — `monthly_visits` starts wide, with one
   column per month. `melt()` turns it into tidy long form (`branch`,
   `month`, `visits`), which is the shape you actually want for grouping —
   in this case, summing total visits per month across all branches.

## Tools & libraries used

- **Python 3** — the language everything is written in.
- **pandas** — does all of the actual work: `pd.concat()` for stacking,
  `pd.merge()` for joining, `groupby().agg()` for summarizing,
  `pd.pivot_table()` for cross-tabs, and `.melt()` for unpivoting. No other
  libraries are needed for this one — it's a pure pandas exercise.

## Results

Running the script against the sample data produces:

- **Combining:** the two quarterly loan tables combine into **8 loans**
  total.
- **Left join:** **1 loan** (`L6`) references a member ID (`M9`) that
  doesn't exist in the members table — a broken reference that a left join
  surfaces immediately instead of hiding.
- **Outer join / indicator:** the `_merge` breakdown is **7 `both`, 1
  `left_only`, 1 `right_only`**. The `right_only` row identifies
  **Eve Davis** as the member who has never borrowed a book.
- **Genre summary** (loans, distinct borrowers, average days kept), sorted
  by popularity:

  | Genre       | Loans | Distinct members | Avg. days kept |
  |-------------|:-----:|:-----------------:|:---------------:|
  | Non-Fiction | 4     | 3                 | 15.25           |
  | Sci-Fi      | 2     | 2                 | 24.50           |
  | Historical  | 1     | 1                 | 28.00           |
  | Fantasy     | 1     | 1                 | 7.00            |

  Non-Fiction is the most-borrowed genre by a clear margin, while
  Historical and Sci-Fi readers tend to hold onto their books the longest.

- **Pivot table** (loans by genre × branch, with totals):

  | Genre       | Central | North | South | Total |
  |-------------|:-------:|:-----:|:-----:|:-----:|
  | Fantasy     | 1       | 0     | 0     | 1     |
  | Historical  | 1       | 0     | 0     | 1     |
  | Non-Fiction | 1       | 2     | 1     | 4     |
  | Sci-Fi      | 1       | 0     | 0     | 1     |
  | **Total**   | **4**   | **2** | **1** | **7** |

  (This pivot only counts the 7 loans that matched to a known
  member/branch — the M9 loan with no branch information is naturally
  excluded, a nice sanity check that the earlier join issue was real.)

- **Melted monthly visits, totalled per month:**

  | Month | Total visits |
  |-------|:-------------:|
  | Jan   | 1,860         |
  | Feb   | 1,915         |
  | Mar   | 2,115         |

  Visits climbed steadily across the quarter, with March the busiest month
  across all three branches combined.

## How to run it

```bash
pip install -r requirements.txt
python library_combine_reshape.py
```

The script prints its output at every step, so you can watch each table
get stacked, joined, summarized, and reshaped in order.

## Project structure

```
.
├── library_combine_reshape.py   # main script
├── requirements.txt             # dependencies
└── README.md                    # this file
```
