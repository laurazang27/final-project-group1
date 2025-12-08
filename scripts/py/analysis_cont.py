"""
analysis_cont.py

Input
-----
- figures/summary_by_income_year.csv

Outputs
-----
1) figures/gdp_growth_boxplots.png
   - Boxplots of GDP growth (%) by income group, 2000–2023.

2) figures/gdp_pc_vs_employment_scatter.png
   - Scatter of log GDP per capita vs employment-to-population ratio.

3) figures/growth_employment_correlation.png
   - Bar chart showing Pearson correlation between GDP growth and
     employment-to-population ratio.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

plt.style.use("seaborn-v0_8-whitegrid")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))

FIG_DIR = os.path.join(REPO_ROOT, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

SUMMARY_YEAR_PATH = os.path.join(FIG_DIR, "summary_by_income_year.csv")
summary_year = pd.read_csv(SUMMARY_YEAR_PATH)


def pick_col(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

income_col = pick_col(summary_year, ["income_group", "income", "income_group_name", "IncomeGroup", "income_group_label"])
year_col = pick_col(summary_year, ["year", "Year", "date"])
gdp_percap_col = pick_col(summary_year, ["avg_gdp_pc", "gdp_percapita", "gdp_per_capita", "NY.GDP.PCAP.KD", "gdp_pc", "GDP_per_capita"])
gdp_growth_col = pick_col(summary_year, ["avg_gdp_growth", "gdp_growth", "NY.GDP.MKTP.KD.ZG", "gdp_growth_pct", "gdp_g"])
employment_col = pick_col(summary_year, ["avg_emp_ratio", "employment_ratio", "employment", "SL.EMP.TOTL.SP.ZS", "employment_to_population"])

summary_year[year_col] = pd.to_numeric(summary_year[year_col], errors="coerce")
for col in (gdp_percap_col, gdp_growth_col, employment_col):
    summary_year[col] = pd.to_numeric(summary_year[col], errors="coerce")

summary_year = summary_year.dropna(subset=[year_col, income_col])

long_income_order = ["High income", "Upper middle income", "Lower middle income", "Low income"]
label_map = {
    "High income": "High Income",
    "Upper middle income": "Upper-Mid Income",
    "Lower middle income": "Lower-Mid Income",
    "Low income": "Low Income",
}
income_groups = [g for g in long_income_order if g in summary_year[income_col].unique().tolist()]

colors = plt.cm.tab10(np.linspace(0, 1, max(3, len(income_groups))))

# Figure 1: Boxplots of GDP growth by income group

fig, ax = plt.subplots(figsize=(8, 6))

data_for_box = [
    summary_year.loc[summary_year[income_col] == grp, gdp_growth_col].dropna()
    for grp in income_groups
]

bp = ax.boxplot(
    data_for_box,
    labels=[label_map[g] for g in income_groups],
    patch_artist=True,
)

for patch, color in zip(bp["boxes"], colors[:len(income_groups)]):
    patch.set_facecolor(color)
    patch.set_alpha(0.75)

ax.axhline(0, color="gray", linewidth=0.8, alpha=0.7)
ax.grid(axis="y", alpha=0.3)

ax.set_ylabel("GDP Growth (%)")
ax.set_title("GDP Growth by Income Group, 2000–2023", pad=12)
plt.xticks(rotation=15)
plt.tight_layout()

out1 = os.path.join(FIG_DIR, "gdp_growth_boxplot.png")
plt.savefig(out1, dpi=200, bbox_inches="tight")
plt.close()

# Figure 2: GDP per capita vs employment (true log x-axis)

fig, ax = plt.subplots(figsize=(8.5, 6))

for i, grp in enumerate(income_groups):
    df_grp = summary_year[summary_year[income_col] == grp].dropna(
        subset=[gdp_percap_col, employment_col]
    )
    if df_grp.empty:
        continue

    x_vals = df_grp[gdp_percap_col].values
    y_vals = df_grp[employment_col].values

    ax.scatter(x_vals, y_vals,
               label=label_map[grp],
               alpha=0.75, s=40, color=colors[i])

ax.set_xscale("log")

all_gdp = summary_year[gdp_percap_col].dropna().values
min_raw, max_raw = all_gdp.min(), all_gdp.max()

candidate_ticks = np.array([500, 1000, 2000, 5000, 10000, 20000, 40000, 80000])
ticks = [v for v in candidate_ticks if (v >= min_raw * 0.8) and (v <= max_raw * 1.2)]

ax.set_xticks(ticks)
ax.get_xaxis().set_major_formatter(FuncFormatter(lambda x, pos: f"{int(x):,}"))

ax.set_xlabel("GDP per Capita (constant USD, log scale)")
ax.set_ylabel("Employment-to-Population Ratio (%)")
ax.set_title("GDP per Capita vs Employment", pad=12)
ax.grid(alpha=0.3)
ax.legend(title="Income Group", frameon=True, loc="lower right")
plt.tight_layout()

out2 = os.path.join(FIG_DIR, "gdp_pc_vs_employment_scatters.png")
plt.savefig(out2, dpi=200, bbox_inches="tight")
plt.close()

# Figure 3: Correlation between GDP growth and employment

corrs = []
for grp in income_groups:
    df_grp = summary_year[summary_year[income_col] == grp].dropna(
        subset=[gdp_growth_col, employment_col]
    )
    if len(df_grp) < 2:
        corr_val = np.nan
    else:
        corr_val = np.corrcoef(df_grp[gdp_growth_col].values,
                               df_grp[employment_col].values)[0, 1]
    corrs.append({"income_group": grp, "corr": corr_val})

corr_df = pd.DataFrame(corrs).set_index("income_group")

fig, ax = plt.subplots(figsize=(8, 6))

x = np.arange(len(corr_df))
vals = corr_df["corr"].values

ax.bar(x, vals, color=colors[:len(corr_df)])
ax.axhline(0, color="black", linewidth=0.8)
ax.grid(axis="y", alpha=0.3)

ax.set_xticks(x)
ax.set_xticklabels([label_map[g] for g in corr_df.index], rotation=15)
ax.set_ylim(-1, 1)
ax.set_ylabel("Pearson Correlation")
ax.set_title("GDP Growth & Employment Ratio Correlation", pad=12)

for i, v in enumerate(vals):
    if np.isnan(v):
        continue
    y_pos = v + 0.04 if v >= 0 else v - 0.06
    ax.text(i, y_pos, f"{v:.2f}", ha="center", va="center", fontsize=9)

plt.tight_layout()

out3 = os.path.join(FIG_DIR, "growth_employment_pearson_correlation.png")
plt.savefig(out3, dpi=200, bbox_inches="tight")
plt.close()