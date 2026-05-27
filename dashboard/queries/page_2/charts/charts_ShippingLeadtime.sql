SELECT
  Shipping,
  strftime(ShipDateKey, '%Y-%m') AS YearMonth,
  MEDIAN(datediff('day', OrderDateKey, ShipDateKey)) AS LeadTime
FROM scm_db.fact_sales
GROUP BY
  Shipping,
  strftime(ShipDateKey, '%Y-%m')