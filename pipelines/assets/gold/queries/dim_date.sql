CREATE OR REPLACE TABLE dim_date AS
    SELECT DISTINCT 
        CAST(date_val AS DATE) AS DateKey,
        EXTRACT(YEAR FROM CAST(date_val AS DATE)) AS Year,
        EXTRACT(MONTH FROM CAST(date_val AS DATE)) AS Month,
        EXTRACT(DAY FROM CAST(date_val AS DATE)) AS Day,
        EXTRACT(QUARTER FROM CAST(date_val AS DATE)) AS Quarter,
        DAYNAME(CAST(date_val AS DATE)) AS DayOfWeekName
    FROM (
        SELECT OrderDate AS date_val FROM staging_raw WHERE OrderDate IS NOT NULL
        UNION
        SELECT ShipDate AS date_val FROM staging_raw WHERE ShipDate IS NOT NULL
    ) AS all_dates;