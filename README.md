# final-project-group1


### Run the analysis_figures.py script

How to run
1. (Optional) Create and activate a virtual environment, then install dependencies:
   - python -m venv venv
   - source venv/bin/activate   # Windows: venv\Scripts\activate
   - pip install -r requirements.txt

2. Run the script from the repository root (it computes paths relative to the repo so it can be run from anywhere):
   - python scripts/py/analysis_figures.py

Inputs
- figures/summary_by_income.csv
- figures/summary_by_income_year.csv

Expected outputs (saved to figures/)
- gdp_percapita_by_income.png
- indicator_trends_by_income.png

Notes
- The script will create the figures/ folder if it does not exist.
- Make sure the two input CSVs above are present before running.


### Run the descriptive_checks.py script

How to run
1. (Optional) Create and activate a virtual environment, then install dependencies:
   - python -m venv venv
   - source venv/bin/activate   # Windows: venv\Scripts\activate
   - pip install -r requirements.txt

2. Run the script from the repository root:
   - python scripts/py/descriptive_checks.py

Inputs
- figures/summary_by_income.csv
- figures/summary_by_income_year.csv

Expected outputs (saved to figures/)
- descriptive_stats_by_income.csv (mean, median, std, count for each indicator by income group)
- descriptive_stats_yearly.csv (yearly averages across income groups)
- global_indicator_trends.png (line plot of mean indicator trends over time)

Notes
- The script will create the figures/ folder if it does not exist.
- Make sure the two input CSVs above are present before running.
