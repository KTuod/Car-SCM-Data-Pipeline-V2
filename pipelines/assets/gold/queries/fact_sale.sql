CREATE OR REPLACE TABLE fact_sales AS
    SELECT
        OrderID,
        CustomerID,
        ProductID,
        SupplierID,
        CAST(OrderDate AS DATE) AS OrderDateKey,
        CAST(ShipDate AS DATE) AS ShipDateKey,
        ShipMode,
        CreditCardType,
        CreditCard,
        CustomerFeedback,
        CAST(Sales AS DOUBLE) AS Sales,
        CAST(Quantity AS INTEGER) AS Quantity,
        CAST(Discount AS DOUBLE) AS Discount,
        Shipping
    FROM staging_raw;