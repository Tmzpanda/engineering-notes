-- find duplicates
-- HAVING
SELECT id, updated_at, created_at, requested_by, department, commodity, item, quantity, total ,status, COUNT(*)
FROM `report.kpi_requisition`
GROUP BY 1,2,3,4,5,6,7,8,9,10 
HAVING COUNT(*) > 1;

-- ROW_NUMBER()
SELECT * FROM ( 
  SELECT 
    *,
    ROW_NUMBER() OVER (PARTITION BY id, commodity, item, quantity, updated_at ORDER BY id, commodity, item, quantity, updated_at DESC ) rn
  FROM `report.kpi_requisition`
  ) 
WHERE rn > 1;

-- drop duplicates
CREATE OR REPLACE TABLE `report.kpi_requisition` AS (
SELECT DISTINCT * FROM `report.kpi_requisition`
)
