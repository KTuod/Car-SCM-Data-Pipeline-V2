CREATE OR REPLACE TABLE dim_supplier AS
    SELECT DISTINCT
        SupplierID,
        SupplierName,
        SupplierAddress,
        SupplierContactDetails
    FROM staging_raw;