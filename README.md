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
- repo-root/data/summary_by_income.csv
- repo-root/data/summary_by_income_year.csv

Expected outputs (saved to repo-root/figures/)
- gdp_percapita_by_income.png
- indicator_trends_by_income.png
- summary_by_income_generated.csv

Notes
- The script will create the figures/ folder if it does not exist.
- Make sure the two input CSVs above are present before running.
