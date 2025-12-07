# final-project-group1

## Data Pre-Processing 

This project uses World Bank World Development Indicators (WDI) data to construct a cleaned country–year dataset and summary tables by income group. The data preparation pipeline is implemented in a Jupyter notebook and uses SQLite for structured storage.

Required software: 
- Python 3 (Conda recommended)
- SQLite (via Python sqlite3)
Required Python packages:
- pandas, jupyter, nbformat, pathlib

To install dependencies using conda:
- conda install pandas jupyter nbformat -y

### Run the data pipeline
The following CSV files must be located in the data/ directory:
- wdi_employment_raw.csv
- wdi_gdp_growth_raw.csv
- wdi_gdp_per_capita_raw.csv
- wdi_income_group.csv

Open and run all cells in: scripts/sql/data_cleaning.ipynb

This notebook:
- imports and reshapes raw WDI data
- builds a SQLite database (econ_dev.db)
- constructs a country–year panel dataset
- merges World Bank income group classifications
- generates summary tables by income group

Running the notebook will produce:
- A SQLite database stored at: data/econ_dev.db

- Summary tables saved to: figures/summary_by_income.csv and figures/summary_by_income_year.csv

These files are used directly in the final analysis and report.

## Data Analysis

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
