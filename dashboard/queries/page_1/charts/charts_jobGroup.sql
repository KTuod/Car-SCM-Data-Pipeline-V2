-- Number of Job Group

SELECT
  job_group,
  COUNT(job_group) AS Total
FROM scm_db.dim_customer
GROUP BY job_group
ORDER BY Total DESC