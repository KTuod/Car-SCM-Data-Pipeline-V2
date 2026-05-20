-- The number of Car_Type

SELECT
  CarType AS 'Car_Type',
  COUNT(CarType) AS 'Count_Car_Type'
FROM scm_db.dim_product
GROUP BY CarType
ORDER BY COUNT(CarType) DESC