# Power BI Dashboard Specification

## Business Objective
Help retail leadership monitor sales trends, customer value, product category performance, and payment behavior.

## Required visuals
1. **KPI Cards**: Total Revenue, Total Orders, Unique Customers, Average Order Value
2. **Line Chart**: Monthly revenue trend
3. **Clustered Bar Chart**: Category revenue vs. order count
4. **Map**: Revenue by city
5. **Donut Chart**: Payment method revenue share
6. **Table**: Top customers (customer_id, city, lifetime_value, order_count)

## Recommended slicers
- Purchase Month
- Category
- City
- Payment Method

## Data model
Single fact table from `transactions` with optional date table generated in Power BI for time intelligence.
