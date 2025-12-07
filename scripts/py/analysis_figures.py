#!/usr/bin/env python3
"""
generate_figures.py
- Loads figures/summary_by_income.csv and figures/summary_by_income_year.csv:
  * Bar chart: mean GDP per capita by income group
  * Line charts: indicator trends over time by income group
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("seaborn-v0_8-whitegrid")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))           
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))  

FIG_DIR = os.path.join(REPO_ROOT, "figures")
os.makedirs(FIG_DIR, exist_ok=True)
summary_path = os.path.join(REPO_ROOT, "figures", "summary_by_income.csv")
summary_year_path = os.path.join(REPO_ROOT, "figures", "summary_by_income_year.csv")
summary = pd.read_csv(summary_path)
summary_year = pd.read_csv(summary_year_path)

def pick_col(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

income_col_candidates = ["income_group", "income", "income_group_name", "IncomeGroup", "income_group_label"]
year_col_candidates = ["year", "Year", "date"]
gdp_percap_candidates = ["avg_gdp_pc", "gdp_percapita", "gdp_per_capita", "NY.GDP.PCAP.KD", "gdp_pc", "GDP_per_capita"]
gdp_growth_candidates = ["avg_gdp_growth", "gdp_growth", "NY.GDP.MKTP.KD.ZG", "gdp_growth_pct", "gdp_g"]
employment_candidates = ["avg_emp_ratio", "employment_ratio", "employment", "SL.EMP.TOTL.SP.ZS", "employment_to_population"]

income_col = pick_col(summary, income_col_candidates) or pick_col(summary_year, income_col_candidates)
year_col = pick_col(summary_year, year_col_candidates) or pick_col(summary, year_col_candidates)
gdp_percap_col = pick_col(summary, gdp_percap_candidates) or pick_col(summary_year, gdp_percap_candidates)
gdp_growth_col = pick_col(summary, gdp_growth_candidates) or pick_col(summary_year, gdp_growth_candidates)
employment_col = pick_col(summary, employment_candidates) or pick_col(summary_year, employment_candidates)


required = {
    "income_col": income_col,
    "year_col": year_col,
    "gdp_percap_col": gdp_percap_col,
    "gdp_growth_col": gdp_growth_col,
    "employment_col": employment_col,
}


for col in (gdp_percap_col, gdp_growth_col, employment_col):
    summary[col] = pd.to_numeric(summary[col], errors="coerce")
    summary_year[col] = pd.to_numeric(summary_year[col], errors="coerce")


#Bar chart: average GDP per capita by income group (summary) using matplotlib
plt.figure(figsize=(8,6))
order = summary.sort_values(by=gdp_percap_col, ascending=False)[income_col].tolist()
vals = summary.set_index(income_col).loc[order, gdp_percap_col].values
x = np.arange(len(order))
colors = plt.cm.tab10(np.linspace(0, 1, max(3, len(order))))
plt.bar(x, vals, color=colors[:len(order)])
plt.xticks(x, order, rotation=25)
plt.ylabel("GDP per capita (constant USD)")
plt.xlabel("Income group")
plt.title("Average GDP per capita by World Bank income group (2000–2023)")
plt.tight_layout()
outp = os.path.join(FIG_DIR, "gdp_percapita_by_income.png")
plt.savefig(outp, dpi=200)
plt.close()
print("Saved:", outp)


#Line plots: indicator trends over time by income group (summary_year) using matplotlib
indicators = [
    (gdp_percap_col, "GDP per capita (constant USD)"),
    (gdp_growth_col, "GDP growth (annual %)"),
    (employment_col, "Employment to population ratio (%)")
]

n_ind = len(indicators)
fig, axes = plt.subplots(n_ind, 1, figsize=(10, 4*n_ind), sharex=True)
summary_year[year_col] = pd.to_numeric(summary_year[year_col], errors="coerce")
income_groups = summary_year[income_col].dropna().unique().tolist()
colors = plt.cm.tab10(np.linspace(0, 1, max(3, len(income_groups))))

for ax_idx, (col, label) in enumerate(indicators):
    ax = axes[ax_idx]
    for i, grp in enumerate(income_groups):
        grp_df = summary_year[summary_year[income_col] == grp].copy()
        grp_df = grp_df.sort_values(by=year_col)
        ax.plot(grp_df[year_col], grp_df[col], marker='o', label=str(grp), color=colors[i % len(colors)])
    ax.set_ylabel(label)
    if ax_idx == n_ind - 1:
        ax.set_xlabel("Year")
    ax.set_title(label)
    ax.legend(title="Income group", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
outp = os.path.join(FIG_DIR, "indicator_trends_by_income.png")
plt.savefig(outp, dpi=200, bbox_inches="tight")
plt.close()
print(outp)
