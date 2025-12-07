#!/usr/bin/env python3
"""
Simple descriptive statistics & exploratory checks using the project summary CSVs.

inputs:
    - repo-root/data/summary_by_income.csv
    - repo-root/data/summary_by_income_year.csv
outputsL
    - figures/descriptive_stats_by_income.csv  (summary stats by income group)
    - figures/descriptive_stats_yearly.csv     (yearly averages across income groups)
    - figures/global_indicator_trends.png      ( mean indicator trends over time plot)
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
# DATA_DIR = os.path.join(REPO_ROOT, "data")
FIG_DIR = os.path.join(REPO_ROOT, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

SUMMARY_PATH = os.path.join(FIG_DIR, "summary_by_income.csv")
SUMMARY_YEAR_PATH = os.path.join(FIG_DIR, "summary_by_income_year.csv")


summary = pd.read_csv(SUMMARY_PATH)
summary_year = pd.read_csv(SUMMARY_YEAR_PATH)
def pick_col(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

income_col = pick_col(summary, ["income_group", "income", "income_group_name", "IncomeGroup", "income_group_label"])
year_col = pick_col(summary_year, ["year", "Year", "date"])
gdp_percap_col = pick_col(summary, ["avg_gdp_pc", "gdp_percapita", "gdp_per_capita", "NY.GDP.PCAP.KD", "gdp_pc", "GDP_per_capita"])
gdp_growth_col = pick_col(summary, ["avg_gdp_growth", "gdp_growth", "NY.GDP.MKTP.KD.ZG", "gdp_growth_pct", "gdp_g"])
employment_col = pick_col(summary, ["avg_emp_ratio", "employment_ratio", "employment", "SL.EMP.TOTL.SP.ZS", "employment_to_population"])

required = [income_col, year_col, gdp_percap_col, gdp_growth_col, employment_col]


for col in (gdp_percap_col, gdp_growth_col, employment_col):
    if col in summary.columns:
        summary[col] = pd.to_numeric(summary[col], errors="coerce")
    if col in summary_year.columns:
        summary_year[col] = pd.to_numeric(summary_year[col], errors="coerce")


#Descriptive statistics by income group (concise)
#(mean, median, std, count for each of the three indicators)
agg_funcs = {
    gdp_percap_col: ['mean', 'median', 'std', 'count'],
    gdp_growth_col: ['mean', 'median', 'std', 'count'],
    employment_col: ['mean', 'median', 'std', 'count']
}

desc_by_income = summary.groupby(income_col).agg(agg_funcs)
desc_by_income.columns = ["_".join(col).strip() for col in desc_by_income.columns.values]
desc_by_income = desc_by_income.reset_index()

out_desc_income = os.path.join(FIG_DIR, "descriptive_stats_by_income.csv")
desc_by_income.to_csv(out_desc_income, index=False)
print("Saved:", out_desc_income)


#Yearly averages across income groups 
#for each year, compute the mean of each indicator across income groups
yearly_means = summary_year.groupby(year_col)[[gdp_percap_col, gdp_growth_col, employment_col]].mean().reset_index()
out_desc_yearly = os.path.join(FIG_DIR, "descriptive_stats_yearly.csv")
yearly_means.to_csv(out_desc_yearly, index=False)
print("Saved:", out_desc_yearly)


#global mean trends over time across income groups
plt.figure(figsize=(9,5))
x = yearly_means[year_col].astype(int)
ax1 = plt.gca()
ax1.plot(x, yearly_means[gdp_percap_col], marker='o', label='GDP per capita', color='C0')
ax1.set_xlabel('Year')
ax1.set_ylabel('GDP per capita', color='C0')
ax1.tick_params(axis='y', labelcolor='C0')


ax2 = ax1.twinx()
ax2.plot(x, yearly_means[gdp_growth_col], marker='s', label='GDP growth (%)', color='C1')
ax2.plot(x, yearly_means[employment_col], marker='^', label='Employment ratio (%)', color='C2')
ax2.set_ylabel('GDP growth / Employment (%)', color='C2')
ax2.tick_params(axis='y', labelcolor='C2')


lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left', bbox_to_anchor=(0,1.15), ncol=3)

plt.title('Mean indicators across income groups (yearly)')
plt.tight_layout()
out_plot = os.path.join(FIG_DIR, "global_indicator_trends.png")
plt.savefig(out_plot, dpi=200, bbox_inches="tight")
plt.close()