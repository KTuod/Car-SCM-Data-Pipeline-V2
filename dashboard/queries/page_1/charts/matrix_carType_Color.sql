SELECT
  p.CarType,
  p.CarColorGroup,
  SUM(f.Quantity) AS Total
FROM scm_db.dim_product p
JOIN scm_db.fact_sales f
ON p.ProductID = f.ProductID
GROUP BY
  p.CarType,
  p.CarColorGroup