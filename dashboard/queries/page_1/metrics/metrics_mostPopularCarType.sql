-- Most Popular Car Type

SELECT Car_Type
FROM (
SELECT
  p.CarType AS 'Car_Type',
  SUM(f.Quantity) AS Quantity
FROM scm_db.dim_product p
JOIN scm_db.fact_sales f
ON p.ProductID = f.ProductID
GROUP BY CarType
ORDER BY Quantity DESC
LIMIT 1
)