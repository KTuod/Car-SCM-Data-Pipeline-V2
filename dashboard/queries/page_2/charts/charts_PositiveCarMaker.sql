SELECT
    p.CarMaker,
    COUNT(f.CustomerFeedback) AS Count_Good
FROM scm_db.dim_product p
JOIN scm_db.fact_sales f
ON p.ProductID = f.ProductID
WHERE f.CustomerFeedback = 'Good' OR f.CustomerFeedback = 'Very Good' OR f.CustomerFeedback = 'Okay'
GROUP BY p.CarMaker
ORDER BY Count_Good DESC
LIMIT 5