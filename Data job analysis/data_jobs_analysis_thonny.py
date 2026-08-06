"""
Data Jobs Market Analysis
==========================
Run this file top to bottom in Thonny (or any plain Python interpreter).

Answers:
  1. What are the skills most in demand for the top 3 most popular data roles?
  2. How are in-demand skills trending for Data Analysts?
  3. How well do jobs and skills pay for Data Analysts?
  4. What are the optimal skills for Data Analysts to learn
     (High Demand AND High Paying)?

Data source: 'lukebarousse/data_jobs' dataset on Hugging Face
(~785k real-world data job postings, scraped from Google job search
results, covering data-related roles posted throughout 2023).

First-time setup (run once, e.g. in Thonny's Tools > Open System Shell,
or just uncomment the lines below and run this file):

    pip install pandas numpy matplotlib seaborn

Note: this version loads the data with plain pandas.read_csv() from a
direct CSV file on Hugging Face, instead of the 'datasets' library.
That avoids installing 'datasets' and its heavier dependencies (like
pyarrow), which can fail to build a wheel on some Thonny/Windows setups.
"""

# import subprocess, sys
# subprocess.check_call([sys.executable, "-m", "pip", "install",
#                         "pandas", "numpy", "matplotlib", "seaborn"])

import ast
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, FuncFormatter

pd.set_option("display.max_columns", None)
sns.set_theme(style="ticks")


# =====================================================================
# 0. LOAD & CLEAN DATA
# =====================================================================
CSV_URL = "https://huggingface.co/datasets/lukebarousse/data_jobs/resolve/main/data_jobs.csv"

print("Loading dataset (~231 MB, first run may take a minute)...")
df = pd.read_csv(CSV_URL)

# Parse posting dates
df["job_posted_date"] = pd.to_datetime(df["job_posted_date"])


# job_skills is stored as a stringified Python list -> convert to a real list
def parse_skills(x):
    if pd.isna(x):
        return x
    if isinstance(x, list):
        return x
    return ast.literal_eval(x)


df["job_skills"] = df["job_skills"].apply(parse_skills)

print(f"Loaded {len(df):,} job postings")
print(df["job_title_short"].value_counts().head(10))


# =====================================================================
# QUESTION 1: Skills most in demand for the top 3 most popular data roles
# =====================================================================
print("\n--- Question 1: Skills in demand for the top 3 data roles ---")

top_3_roles = df["job_title_short"].value_counts().head(3).index.tolist()
print("Top 3 most popular data roles:", top_3_roles)

df_top3 = df[df["job_title_short"].isin(top_3_roles)]
df_skills_top3 = df_top3.explode("job_skills")

skill_counts = (
    df_skills_top3.groupby(["job_title_short", "job_skills"])
    .size()
    .reset_index(name="skill_count")
)
role_totals = df_top3["job_title_short"].value_counts().rename("role_total")
skill_counts = skill_counts.merge(role_totals, left_on="job_title_short", right_index=True)
skill_counts["skill_pct"] = skill_counts["skill_count"] / skill_counts["role_total"] * 100

fig, axes = plt.subplots(len(top_3_roles), 1, figsize=(9, 10))
for i, role in enumerate(top_3_roles):
    role_df = (
        skill_counts[skill_counts["job_title_short"] == role]
        .sort_values("skill_pct", ascending=False)
        .head(5)
    )
    sns.barplot(
        data=role_df, x="skill_pct", y="job_skills", ax=axes[i],
        hue="job_skills", palette="dark:b_r", legend=False,
    )
    axes[i].set_title(role, fontsize=13, fontweight="bold")
    axes[i].set_xlabel("")
    axes[i].set_ylabel("")
    axes[i].xaxis.set_major_formatter(PercentFormatter(decimals=0))
    for n, v in enumerate(role_df["skill_pct"]):
        axes[i].text(v + 0.3, n, f"{v:.0f}%", va="center")
    if i != len(top_3_roles) - 1:
        axes[i].set_xticks([])

fig.suptitle("Top 5 In-Demand Skills for the 3 Most Popular Data Roles",
             fontsize=15, fontweight="bold")
plt.tight_layout()
plt.show()


# =====================================================================
# QUESTION 2: How are in-demand skills trending for Data Analysts?
# =====================================================================
print("\n--- Question 2: Trending skills for Data Analysts ---")

df_da = df[df["job_title_short"] == "Data Analyst"].copy()
# Optional: focus on one country - uncomment to narrow the picture
# df_da = df_da[df_da["job_country"] == "United States"]

df_da["job_posted_month"] = df_da["job_posted_date"].dt.strftime("%b")
month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

df_da_exploded = df_da.explode("job_skills")

skills_by_month = (
    df_da_exploded.pivot_table(
        index="job_posted_month", columns="job_skills", aggfunc="size", fill_value=0
    ).reindex(month_order)
)

postings_per_month = (
    df_da.groupby(df_da["job_posted_date"].dt.strftime("%b")).size().reindex(month_order)
)
skills_pct_by_month = skills_by_month.div(postings_per_month, axis=0) * 100

top5_overall = df_da_exploded["job_skills"].value_counts().head(5).index.tolist()

plt.figure(figsize=(10, 6))
sns.lineplot(data=skills_pct_by_month[top5_overall], dashes=False,
             palette="tab10", linewidth=2.5)
plt.title("Trending Skills for Data Analysts in 2023", fontsize=14, fontweight="bold")
plt.ylabel("Likelihood in Job Posting (%)")
plt.xlabel("")
plt.gca().yaxis.set_major_formatter(PercentFormatter(decimals=0))
plt.legend(title="Skill", loc="upper left", bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.show()


# =====================================================================
# QUESTION 3: How well do jobs and skills pay for Data Analysts?
# =====================================================================
print("\n--- Question 3: Pay for Data Analyst jobs and skills ---")

# 3a. Salary distribution across the top 6 data roles (for context)
top6_roles_by_count = df["job_title_short"].value_counts().head(6).index.tolist()
df_top6 = df[df["job_title_short"].isin(top6_roles_by_count)]
order_by_median = (
    df_top6.groupby("job_title_short")["salary_year_avg"].median()
    .sort_values(ascending=False).index
)

plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df_top6, x="salary_year_avg", y="job_title_short", order=order_by_median,
    hue="job_title_short", palette="Set2", legend=False,
)
plt.title("Yearly Salary Distribution by Data Role", fontsize=14, fontweight="bold")
plt.xlabel("Yearly Salary (USD)")
plt.ylabel("")
plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${int(x/1000)}K"))
plt.xlim(0, 300000)
plt.tight_layout()
plt.show()

# 3b. Highest paid vs most in-demand skills, for Data Analyst specifically
df_da_pay = df[(df["job_title_short"] == "Data Analyst") & (df["salary_year_avg"].notna())].copy()
df_da_pay_exploded = df_da_pay.explode("job_skills")

skill_pay = df_da_pay_exploded.groupby("job_skills")["salary_year_avg"].median()
skill_demand_pay = df_da_pay_exploded["job_skills"].value_counts()

top10_highest_paid = skill_pay.sort_values(ascending=False).head(10)
top10_most_demanded = skill_demand_pay.head(10)
top10_most_demanded_pay = skill_pay.loc[top10_most_demanded.index].sort_values(ascending=False)

fig, axes = plt.subplots(2, 1, figsize=(9, 10))

sns.barplot(x=top10_highest_paid.values, y=top10_highest_paid.index, ax=axes[0],
            hue=top10_highest_paid.index, palette="dark:b_r", legend=False)
axes[0].set_title("Top 10 Highest Paid Skills for Data Analysts", fontweight="bold")
axes[0].xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${int(x/1000)}K"))
axes[0].set_xlabel("")

sns.barplot(x=top10_most_demanded_pay.values, y=top10_most_demanded_pay.index, ax=axes[1],
            hue=top10_most_demanded_pay.index, palette="light:b", legend=False)
axes[1].set_title("Median Salary for the 10 Most In-Demand Skills", fontweight="bold")
axes[1].xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${int(x/1000)}K"))
axes[1].set_xlabel("Median Yearly Salary (USD)")

plt.tight_layout()
plt.show()

print("Median Data Analyst salary overall: ${:,.0f}".format(df_da_pay["salary_year_avg"].median()))


# =====================================================================
# QUESTION 4: Optimal skills for Data Analysts (High Demand AND High Pay)
# =====================================================================
print("\n--- Question 4: Optimal skills to learn ---")

skill_stats = pd.DataFrame({
    "demand_pct": skill_demand_pay / len(df_da_pay) * 100,
    "median_salary": skill_pay,
}).dropna()

# Require a skill to appear in >= 5% of postings, to avoid noise from rare skills.
# Lower this to see more (noisier) skills, raise it for only the most common ones.
skill_stats = skill_stats[skill_stats["demand_pct"] >= 5].sort_values(
    "median_salary", ascending=False
)

plt.figure(figsize=(10, 7))
sns.scatterplot(data=skill_stats, x="demand_pct", y="median_salary", s=60)

for skill, row in skill_stats.iterrows():
    plt.text(row["demand_pct"] + 0.1, row["median_salary"], skill, fontsize=9)

plt.axhline(skill_stats["median_salary"].median(), color="grey", linestyle="--", linewidth=1)
plt.axvline(skill_stats["demand_pct"].median(), color="grey", linestyle="--", linewidth=1)

plt.title("Optimal Skills for Data Analysts\n(High Demand AND High Pay)",
          fontsize=14, fontweight="bold")
plt.xlabel("Percent of Data Analyst Job Postings Requiring Skill")
plt.ylabel("Median Yearly Salary (USD)")
plt.gca().xaxis.set_major_formatter(PercentFormatter(decimals=0))
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${int(x/1000)}K"))
plt.tight_layout()
plt.show()

print("\nSkills above both median pay AND median demand (top-right quadrant) "
      "are the best bets - high demand and high pay:")
best = skill_stats[
    (skill_stats["median_salary"] > skill_stats["median_salary"].median())
    & (skill_stats["demand_pct"] > skill_stats["demand_pct"].median())
].sort_values("median_salary", ascending=False)
print(best)

print("\nDone! Close all chart windows to finish.")
