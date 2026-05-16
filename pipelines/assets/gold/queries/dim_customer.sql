CREATE OR REPLACE TABLE dim_customer AS
    SELECT DISTINCT
        CustomerID,
        CustomerName,
        Gender,
        JobTitle,
        CASE
            -- Engineering
            WHEN JobTitle ILIKE '%Engineer%' THEN 'Engineering'

            -- IT & Software
            WHEN JobTitle ILIKE '%Developer%'
            OR JobTitle ILIKE '%Programmer%'
            OR JobTitle ILIKE '%Software%'
            OR JobTitle ILIKE '%Systems Administrator%'
            OR JobTitle ILIKE '%Database Administrator%'
            OR JobTitle ILIKE '%Web Developer%'
            OR JobTitle ILIKE '%Web Designer%'
            OR JobTitle ILIKE '%IT%'
            THEN 'IT & Software'

            -- Data & Analytics
            WHEN JobTitle ILIKE '%Analyst%'
            OR JobTitle ILIKE '%Statistician%'
            OR JobTitle ILIKE '%Biostatistician%'
            OR JobTitle ILIKE '%Actuary%'
            THEN 'Data & Analytics'

            -- Finance
            WHEN JobTitle ILIKE '%Accountant%'
            OR JobTitle ILIKE '%Financial%'
            OR JobTitle ILIKE '%Accounting%'
            OR JobTitle ILIKE '%Auditor%'
            OR JobTitle ILIKE '%Cost%'
            THEN 'Finance & Accounting'

            -- Sales & Marketing
            WHEN JobTitle ILIKE '%Sales%'
            OR JobTitle ILIKE '%Marketing%'
            OR JobTitle ILIKE '%Account Executive%'
            OR JobTitle ILIKE '%Sales Associate%'
            THEN 'Sales & Marketing'

            -- HR & Admin
            WHEN JobTitle ILIKE '%Human Resources%'
            OR JobTitle ILIKE '%Recruit%'
            OR JobTitle ILIKE '%Administrative%'
            OR JobTitle ILIKE '%Office Assistant%'
            OR JobTitle ILIKE '%Secretary%'
            THEN 'HR & Admin'

            -- Healthcare
            WHEN JobTitle ILIKE '%Nurse%'
            OR JobTitle ILIKE '%Therapist%'
            OR JobTitle ILIKE '%Pharmacist%'
            OR JobTitle ILIKE '%Dental%'
            OR JobTitle ILIKE '%Clinical%'
            THEN 'Healthcare'

            -- Education
            WHEN JobTitle ILIKE '%Professor%'
            OR JobTitle ILIKE '%Teacher%'
            OR JobTitle ILIKE '%Research%'
            THEN 'Education & Research'

            -- Legal
            WHEN JobTitle ILIKE '%Legal%'
            OR JobTitle ILIKE '%Paralegal%'
            THEN 'Legal'

            -- Creative
            WHEN JobTitle ILIKE '%Designer%'
            OR JobTitle ILIKE '%Media%'
            OR JobTitle ILIKE '%Editor%'
            OR JobTitle ILIKE '%Writer%'
            THEN 'Creative & Media'

            -- Operations
            WHEN JobTitle ILIKE '%Manager%'
            OR JobTitle ILIKE '%Operator%'
            OR JobTitle ILIKE '%Coordinator%'
            THEN 'Operations'

            ELSE 'Others'
        END AS job_group,
        PhoneNumber,
        EmailAddress,
        CustomerAddress,
        City,
        State,
        Country,
        CountryCode,
        PostalCode,
        ProductID,
        SupplierID
    FROM staging_raw;