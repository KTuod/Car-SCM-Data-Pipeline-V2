-- Most Popular Car Maker

SELECT Car_Maker
FROM (
SELECT
  CarMaker AS 'Car_Maker',
  COUNT(CarMaker) AS 'Count_Car_Maker'
FROM scm_db.dim_product
GROUP BY CarMaker
ORDER BY COUNT(CarMaker) DESC
LIMIT 1
)