SELECT
  d.CarMaker,
  f.CustomerFeedback,
  COUNT(f.CustomerFeedback) AS Total
FROM scm_db.fact_sales f
JOIN scm_db.dim_product d
ON f.ProductID = d.ProductID
WHERE d.CarMaker <> 'Others'
GROUP BY
  d.CarMaker,
  f.CustomerFeedback