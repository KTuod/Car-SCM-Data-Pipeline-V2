-- charts_ShipMode&Shipping.sql
SELECT
  ShipMode,
  Shipping,
  COUNT(Shipping) AS Total
FROM scm_db.fact_sales
GROUP BY
  ShipMode,
  Shipping
ORDER BY Total DESC