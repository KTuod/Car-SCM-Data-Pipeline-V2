-- The number of Car_Color Group

SELECT
  p.CarColor AS 'Car_Color_Group',
  SUM(f.Quantity) AS 'Count_Car_Color'
FROM scm_db.dim_product p
JOIN scm_db.fact_sales f
ON p.ProductID = f.ProductID
GROUP BY p.CarColor
ORDER BY Count_Car_Color DESC