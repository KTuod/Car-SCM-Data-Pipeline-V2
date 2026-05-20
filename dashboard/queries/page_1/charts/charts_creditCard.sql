-- Credit Card Type

SELECT
  CreditCardType,
  COUNT(CreditCardType) AS Total
FROM scm_db.fact_sales
GROUP BY CreditCardType
ORDER BY Total DESC