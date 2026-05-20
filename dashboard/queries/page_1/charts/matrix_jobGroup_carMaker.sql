SELECT
  s.job_group,
  p.CarMaker,
  COUNT(job_group) AS Total
FROM scm_db.dim_customer s
JOIN scm_db.dim_product p
  ON s.ProductID = p.ProductID
GROUP BY
  s.job_group,
  p.CarMaker
ORDER BY Total DESC