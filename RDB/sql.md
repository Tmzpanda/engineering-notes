# duplicate
```sql
-- DISTINCT
SELECT DISTINCT id, name, department, salary
FROM employee
```
```sql
-- GROUP BY
SELECT id, name, dept_id, salary
FROM employee
GROUP BY id, name, dept_id, salary
HAVING COUNT(*) > 1
```
```sql
-- ROW_NUMBER
WITH temp AS (
  SELECT
    id, name, dept_id, salary, ROW_NUMBER() OVER (PARTITION BY id, name, dept_id, salary ORDER BY salary DESC) AS row_num
    FROM employee
)
SELECT id, name, dept_id, salary
FROM temp
WHERE row_num > 1;
```

# find nth highest salary
```sql
SELECT name, salary
FROM employee
WHERE salary = (
  SELECT DISTINCT salary
  FROM employee
  ORDER BY salary DESC
  LIMIT n-1, 1 -- skip n-1 retrive 1
);
```
```sql
-- deduplicate
SELECT name, salary
FROM (
  SELECT name, salary, DENSE_RANK() OVER(ORDER BY salary DESC) AS rank 
  FROM employee
  )
WHERE rank = n;
```
```sql
-- find nth highest salary in each department
WITH temp AS
(SELECT *, DENSE_RANK() OVER(PARTITION BY dept_id ORDER BY salary DESC) AS rank
 FROM employee  
)
SELECT t.name AS employee, d.name AS department, t.salary 
FROM temp t
JOIN department d ON t.dept_id = d.id
WHERE t.rank == n
```
```py
# pandas
df['rank'] = df.groupby('dept_id')['salary'].rank(method='dense', ascending=False)
df = df[(df['rank'] == n)]
```
```py
# pyspark
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("app").getOrCreate()
df = df.withColumn('rank', dense_rank().over(Window.partitionBy('dept_id').orderBy(col('salary').desc()))).filter(col('rank') == n)
```

# window function
```sql
-- cumulative reset
-- (https://www.xiaohongshu.com/explore/64c1440e000000000103cd3d)
WITH daily_user_count AS
(SELECT date, DATE_FORMAT(date, '%Y-%m') AS ym, daily_count 
 FROM (
   SELECT DATE(created_at) AS date, COUNT(id) AS daily_count
   FROM users
   GROUP BY date
 )
)
SELECT date, SUM(daily_count) OVER(PARTITION BY ym ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS monthly_cumulative
FROM daily_user_count
```
# WITH approach
```sql
-- career jumping
-- (https://www.xiaohongshu.com/explore/64c1440e000000000103cd3d)
WITH job_timeline AS
(SELECT user_id, company, title, DATEDIFF(DATE(end_date), DATE(start_date)) AS days_spent_on_job
 FROM user_experiences
 WHERE user_id IN (SELECT user_id FROM user_experiences WHERE title = 'data science manager' AND is_current_role = True)
 GROUP BY 1, 2, 3
 ORDER BY 1, 2, 3, days_spent_on_job ASC
)
SELECT user_id, 
  COUNT(DISTINCT company) num_switches,
  SUM(days_spent_on_job) num_days_to_dsm
FROM job_timeline
GROUP BY 1
```

# ways of converting row values to new columns
```sql
-- 1479. Sales by Day of the Week
-- CASE WHEN
WITH category_quantity AS
(SELECT i.item_category AS category, DAYNAME(o.order_date) AS day_of_week, SUM(orders.quantity) AS quantity
 FROM orders o
 RIGHT JOIN items i ON o.item_id = i.item_id
 GROUP BY i.item_category, DAYNAME(o.order_date)
)
SELECT category,
MAX(CASE WHEN day_of_week = 'Monday' THEN quantity ELSE 0 END) AS Monday,																
MAX(CASE WHEN day_of_week = 'Tuesday' THEN quantity ELSE 0 END) AS Tuesday,
MAX(CASE WHEN day_of_week = 'Wednesday' THEN quantity ELSE 0 END) AS Wednesday,
MAX(CASE WHEN day_of_week = 'Thursday' THEN quantity ELSE 0 END) AS Thursday,
MAX(CASE WHEN day_of_week = 'Friday' THEN quantity ELSE 0 END) AS Friday,
MAX(CASE WHEN day_of_week = 'Saturday' THEN quantity ELSE 0 END) AS Saturday,
MAX(CASE WHEN day_of_week = 'Sunday' THEN quantity ELSE 0 END) AS Sunday
FROM category_quantity
GROUP BY category

-- PIVOT
WITH category_quantity AS
(SELECT i.item_category AS category, DAYNAME(o.order_date) AS day_of_week, SUM(orders.quantity) AS quantity
 FROM orders o
 RIGHT JOIN items i ON o.item_id = i.item_id
 GROUP BY i.item_category, DAYNAME(o.order_date)
)
SELECT category, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
FROM category_quantity PIVOT(MAX(Quantity) FOR day_of_week IN ([Monday], [Tuesday], [Wednesday], [Thursday], [Friday], [Saturday], [Sunday])) p;
```

```sql
-- 618. Students by Geography
-- CASE WHEN
WITH temp1 AS
(SELECT *, ROW_NUMBER() OVER(PARTITION BY continent ORDER BY name) AS row_id	
 FROM student
),
temp2 AS
(SELECT row_id,
 MAX(CASE WHEN continent = 'America' THEN name END) AS America,			
 MAX(CASE WHEN continent = 'Europe' THEN name END) AS Europe,
 MAX(CASE WHEN continent = 'Asia' THEN name END) AS Asia
 FROM temp1
 GROUP BY row_id
)
SELECT America, Asia, Europe
FROM temp2

-- PIVOT
WITH temp AS
(SELECT *, ROW_NUMBER() OVER(PARTITION BY continent ORDER BY name) AS row_id			
 FROM student
)
SELECT America, Europe, Asia
FROM temp PIVOT (MAX(name) FOR continent IN (America, Europe, Asia)) p
```

```sql
-- Employees Spent Hours at Office	
CREATE TABLE event (
	emp_id INT, 
	event VARCHAR(25), 
	time DATETIME
	); 
INSERT INTO Event VALUES 
	(101, 'in', '2012/04/05 08:14:56'),
	(101, 'out', '2012/04/05 08:24:55'),
	(101, 'in', '2012/04/05 08:34:56'),
	(101, 'out', '2012/04/05 08:44:56'),
	(102, 'in', '2012/04/05 08:14:56'),
	(102, 'out', '2012/04/05 08:44:56');

WITH temp1 AS
(SELECT *, ROW_NUMBER() OVER(PARTITION BY emp_id, event Order BY time) AS row_id
 FROM event
),
temp2 AS
(SELECT * 
 FROM temp1 PIVOT(MAX(time) FOR event in ([in], [out])) p
)
SELECT emp_id, SUM(DATEDIFF(second, [in], [out])) AS timespan
FROM temp2
GROUP BY emp_id

```

# reducing columns while keeping info
```sql
-- 1555. User Transaction and Credit
-- UNION
WITH temp AS
(SELECT paid_by AS user_id, -amount AS transaction
 FROM transactions
 UNION													
 SELECT paid_to AS user_id, amount AS transaction
 FROM transactions
),
user_transaction AS
(SELECT user_id, SUM(transaction) AS transaction_sum
 FROM temp
 GROUP BY user_id
)
SELECT users.user_id, users.user_name, user_transaction.transaction_sum,
  CASE WHEN users.credit + IFNULL(user_transaction.transaction_sum, 0) > 0 THEN 'No' ELSE 'Yes' END AS 'credit_limit_breached'
FROM users 
LEFT JOIN user_transaction ON users.user_id = user_transaction.user_id	

```

# HAVING 
```sql
-- 1398. Customers Who Bought Products A and B but Not C
WITH temp AS
(
    SELECT customer_id
    From orders
    GROUP BY customer_id
    HAVING SUM(product_name = 'A') > 0 AND SUM(product_name = 'B') > 0 AND SUM(product_name = 'C') = 0
)
SELECT customer_id, customer_name
FROM Customers
WHERE customer_id in (SELECT customer_id FROM temp);
```

```sql
-- fraudulent upvotes
-- (https://www.xiaohongshu.com/explore/64c1440e000000000103cd3d)
WITH comment_voters AS
(SELECT comment.id AS comment_id, comment.user_id AS commenter_id, comment_votes.user_id AS voter_id
 FROM comments
 INNER JOIN comment_votes ON comments.id = comment_votes.comment_id
)
voters_never_comment AS
(SELECT comment_votes.user_id
 FROM comment_votes
 LEFT JOIN comments ON comment_votes.user_id = comments.user_id
 WHERE comments.id IS NULL AND is_upvote = True
)
SELECT voter_id
FROM comment_voters
WHERE voter_id IN (SELECT user_id FROM voters_never_comment)
GROUP BY voter_id
HAVING COUNT(DISTINCT commenter_id) = 1 AND COUNT(DISTINCT comment_id) > 3 -- voters who only upvoted one person but have >3 upvotes
```

# CASE WHEN  
```sql
-- Employee Department Onboard Departure Time - SCD
CREATE TABLE department(
dept_id      INT,
dept_name   VARCHAR(20),
start_date    DATE, 
end_date    DATE);
INSERT INTO department VALUES
(1, 'dept_1', '2013-02-23', '2013-09-20'),
(1, 'dept_1a', '2013-09-21', '2013-12-25'),
(1, 'dept_1b', '2013-12-26', NULL),
(2, 'dept_2', '2013-01-21', NULL);

CREATE TABLE employee(
emp_id      INT,
dept_id     INT,
start_date    DATE, 
end_date    DATE);
INSERT INTO employee VALUES
(1, 1, '2013-04-21', NULL),
(2, 2, '2013-01-01', '2013-10-10');

SELECT 
e.emp_id, e.dept_id, d.dept_name
CASE WHEN e.start_date IS NOT NULL AND d.start_date IS NOT NULL AND e.start_date >= d.start_date THEN e.start_date ELSE d.start_date END AS start_date,
CASE 
    WHEN e.end_date IS NOT NULL AND d.end_date IS NOT NULL AND e.end_date >= d.end_date THEN d.end_date
    WHEN e.end_date IS NULL AND d.end_date IS NOT NULL THEN d.end_date
    WHEN e.end_date IS NOT NULL AND d.end_date IS NULL THEN e.end_date
    WHEN e.end_date IS NULL AND d.end_date IS NULL THEN NULL
END AS end_date,
FROM employee e
JOIN department d ON e.dept_id = d.dept_id
```

```sql
-- 615. Average Salary for each Month: Departments vs Company
WITH department_salary AS 
(
    SELECT DATE_FORMAT(s.pay_date, '%Y-%m') AS pay_month, e.department_id, AVG(s.amount) AS department_average 	  
    FROM salary s
    JOIN employee e ON s.employee_id = e.employee_id
    GROUP BY DATE_FORMAT(s.pay_date, '%Y-%m'), e.department_id
), 
company_salary AS (
    SELECT DATE_FORMAT(s.pay_date, '%Y-%m') AS pay_month, AVG(amount) AS company_average
    FROM salary s
    GROUP BY DATE_FORMAT(s.pay_date, '%Y-%m')
)
SELECT department_salary.pay_month, department_salary.department_id, 
    CASE 
        WHEN department_salary.department_average > company_salary.company_average THEN 'higher'
        WHEN department_salary.department_average < company_salary.company_average THEN 'lower'
        ELSE 'same'
    END AS comparison												  
FROM department_salary
JOIN company_salary
ON department_salary.pay_month = company_salary.pay_month
```
```sql


```
```sql


```
```sql


```
```sql


```


