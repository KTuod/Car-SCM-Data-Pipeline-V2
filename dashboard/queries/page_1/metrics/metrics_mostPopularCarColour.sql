-- Most Popular Car_Color Group

SELECT Car_Color_Group
FROM(
    SELECT
        p.CarColor AS 'Car_Color_Group',
        SUM(f.Quantity) AS Quantity
    FROM scm_db.dim_product p
    JOIN scm_db.fact_sales f
    ON p.ProductID = f.ProductID
    GROUP BY CarColor
    ORDER BY COUNT(CarColor) DESC
    LIMIT 1
)