# Retail Customer Behavior and Shopping Trends - Project Report

## Problem Statement
A retail company wants to understand which customers, categories, and payment channels drive revenue, and how sales change over time.

## Workflow Summary
1. Ingest raw transaction data using Python and pandas.
2. Clean and standardize records (types, null handling, duplicates, calculated fields).
3. Store cleaned data into SQLite and run business SQL queries.
4. Export query-ready files for Power BI dashboarding.
5. Deliver insights for decision-makers.

## Key Insights (sample dataset)
- Electronics is the top revenue category.
- Card and UPI dominate cash in payment-linked revenue.
- A small group of customers contributes disproportionately to sales.

## Business Recommendations
- Prioritize top categories in promotional calendars.
- Build retention campaigns for top-value customers.
- Optimize payment incentives for high-revenue channels.

## Deliverables
- Python pipeline: `src/retail_analytics.py`
- SQL queries: `sql/business_queries.sql`
- Power BI dashboard spec: `powerbi/dashboard_spec.md`
- Presentation prompt: `presentations/gamma_prompt.md`
