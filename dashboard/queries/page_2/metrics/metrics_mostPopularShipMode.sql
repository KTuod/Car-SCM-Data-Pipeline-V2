SELECT ShipMode
FROM(
  SELECT
    ShipMode,
    COUNT(ShipMode) AS Total
  FROM scm_db.fact_sales
  GROUP BY ShipMode
  ORDER BY Total DESC
)
LIMIT 1