SELECT
    category,
    SUM(total_price) AS revenue
FROM sales
GROUP BY category
ORDER BY revenue DESC;