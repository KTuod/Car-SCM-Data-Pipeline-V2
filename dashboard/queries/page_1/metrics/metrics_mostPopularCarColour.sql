-- Most Popular Car_Color Group

SELECT Car_Color_Group
FROM(
    SELECT
        CarColor AS 'Car_Color_Group',
        COUNT(CarColor) AS 'Count_Car_Color'
    FROM scm_db.dim_product
    GROUP BY CarColor
    ORDER BY COUNT(CarColor) DESC
    LIMIT 1
)
