SELECT
  p.CarMaker,
  STRFTIME(t.OrderDateKey, '%Y-%m') AS YearMonth,
  COUNT(t.ProductID) AS Total_Count
FROM scm_db.fact_sales t
JOIN scm_db.dim_product p
ON t.ProductID = p.ProductID
WHERE p.CarMaker IN (
  SELECT CarMaker
  FROM (
    SELECT 
      CarMaker, 
      COUNT(CarMaker) AS Count_CarMaker
    FROM scm_db.dim_product
    GROUP BY CarMaker
    ORDER BY Count_CarMaker DESC
  )
  LIMIT 10
)
GROUP BY 
  YearMonth,
  p.CarMaker
ORDER BY YearMonth