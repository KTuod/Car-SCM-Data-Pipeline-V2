SELECT
  CustomerFeedback
FROM (
  SELECT
    CustomerFeedback,
    COUNT(CustomerFeedback) AS Total
  FROM scm_db.fact_sales
  GROUP BY CustomerFeedback
  ORDER BY Total DESC
)
LIMIT 1