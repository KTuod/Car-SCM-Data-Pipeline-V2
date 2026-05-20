SELECT
  CarType,
  CarColorGroup,
  COUNT(CarType) AS Total
FROM scm_db.dim_product
GROUP BY
  CarType,
  CarColorGroup