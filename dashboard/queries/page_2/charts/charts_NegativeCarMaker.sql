SELECT
    p.CarMaker,
    COUNT(f.CustomerFeedback) AS Count_Bad
FROM scm_db.dim_product p
JOIN scm_db.fact_sales f
ON p.ProductID = f.ProductID
WHERE f.CustomerFeedback = 'Bad' OR f.CustomerFeedback = 'Very Bad'
GROUP BY p.CarMaker
ORDER BY Count_Bad DESC
LIMIT 5