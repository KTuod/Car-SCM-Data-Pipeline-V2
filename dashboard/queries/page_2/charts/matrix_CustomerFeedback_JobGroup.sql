SELECT
  d.job_group,
  f.CustomerFeedback,
  COUNT(f.CustomerFeedback) AS Total
FROM scm_db.fact_sales f
JOIN scm_db.dim_customer d
ON f.CustomerID = d.CustomerID
WHERE d.job_group <> 'Others'
GROUP BY
  d.job_group,
  f.CustomerFeedback