# Retail Customer Trends Data Analysis (Python, SQL, Power BI)

This repository implements a complete analytics workflow for a retail customer behavior use case, from raw data cleaning to SQL business analysis and dashboard-ready outputs.

## Project Deliverables
- **Business problem statement and reporting**: `reports/project_report.md`
- **Python data pipeline (pandas)**: `src/retail_analytics.py`
- **SQL business analysis queries**: `sql/business_queries.sql`
- **Power BI dashboard blueprint**: `powerbi/dashboard_spec.md`
- **Gamma AI presentation prompt**: `presentations/gamma_prompt.md`

## End-to-End Workflow
1. Load raw retail transactions from `data/raw/retail_customer_behavior.csv`.
2. Clean and standardize data with pandas:
   - enforce numeric/date types
   - remove invalid rows and duplicates
   - compute `total_amount`
3. Save cleaned data to `data/processed/retail_customer_behavior_cleaned.csv`.
4. Load cleaned data into SQLite (`outputs/retail_analytics.db`).
5. Execute business SQL queries and export results to `outputs/*.csv`.
6. Use exported outputs to build the Power BI dashboard.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run pipeline
```bash
python src/retail_analytics.py
```

## Run tests
```bash
python -m unittest discover -s tests -q
```
