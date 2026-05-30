-- 1) Monthly revenue trend
SELECT strftime('%Y-%m', purchase_date) AS month,
       ROUND(SUM(total_amount), 2) AS revenue,
       COUNT(*) AS orders
FROM transactions
GROUP BY month
ORDER BY month;

-- 2) Category performance
SELECT category,
       ROUND(SUM(total_amount), 2) AS revenue,
       ROUND(AVG(total_amount), 2) AS avg_order_value,
       COUNT(*) AS orders
FROM transactions
GROUP BY category
ORDER BY revenue DESC;

-- 3) Top customer segments by spend
SELECT customer_id,
       city,
       ROUND(SUM(total_amount), 2) AS lifetime_value,
       COUNT(*) AS order_count
FROM transactions
GROUP BY customer_id, city
ORDER BY lifetime_value DESC
LIMIT 10;

-- 4) Payment method distribution
SELECT payment_method,
       COUNT(*) AS orders,
       ROUND(SUM(total_amount), 2) AS revenue
FROM transactions
GROUP BY payment_method
ORDER BY revenue DESC;
