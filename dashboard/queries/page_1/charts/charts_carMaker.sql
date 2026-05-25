SELECT
  p.CarMaker,
  SUM(F.Quantity) AS 'Count_Car_Maker'
FROM scm_db.dim_product p
JOIN scm_db.fact_sales f
ON p.ProductID = f.ProductID
GROUP BY p.CarMaker
ORDER BY Count_Car_Maker DESC