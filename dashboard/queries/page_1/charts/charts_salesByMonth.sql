-- Sales by Month

SELECT
  STRFTIME(OrderDateKey, '%Y-%m') AS YearMonth,
  COUNT(ProductID) AS Total_Count
FROM scm_db.fact_sales
GROUP BY YearMonth
ORDER BY YearMonth