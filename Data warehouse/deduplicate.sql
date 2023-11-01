-- drop duplicates
CREATE OR REPLACE TABLE `report.kpi_requisition` AS (
SELECT DISTINCT * FROM `report.kpi_requisition`
)
