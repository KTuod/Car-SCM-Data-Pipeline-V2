-- Highest Sales Supplier 

SELECT SupplierName
FROM (
    SELECT
        s.SupplierName,
        ROUND(SUM(f.Sales), 2) AS Total_Sale
    FROM scm_db.dim_supplier s
    JOIN scm_db.fact_sales f
    ON s.SupplierID = f.SupplierID
    GROUP BY s.SupplierName
    ORDER BY Total_Sale DESC
    LIMIT 1
    )