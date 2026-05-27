SELECT
  job_group
FROM (
  SELECT
    c.job_group,
    COUNT(f.CustomerFeedback) AS Count_Bad
  FROM scm_db.dim_customer c
  JOIN scm_db.fact_sales f
  ON c.CustomerID = f.CustomerID
  WHERE f.CustomerFeedback = 'Bad' OR f.CustomerFeedback = 'Very Bad'
  GROUP BY c.job_group
  ORDER BY Count_Bad DESC
  LIMIT 1
)