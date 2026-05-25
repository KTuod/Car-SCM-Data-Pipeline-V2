SELECT
  p.CarMaker,
  STRFTIME(f.OrderDateKey, '%Y-%m') AS YearMonth,
  SUM(f.Quantity) AS Total_Count
FROM scm_db.fact_sales f
JOIN scm_db.dim_product p
ON f.ProductID = p.ProductID
WHERE p.CarMaker IN (
  SELECT CarMaker
  FROM (
    SELECT 
      p.CarMaker, 
      SUM(f.Quantity) AS Count_CarMaker
    FROM scm_db.dim_product p
    JOIN scm_db.fact_sales f
    ON p.ProductID = f.ProductID
    GROUP BY p.CarMaker
    ORDER BY Count_CarMaker DESC
  )
  LIMIT 10
)
GROUP BY 
  YearMonth,
  p.CarMaker
ORDER BY YearMonth