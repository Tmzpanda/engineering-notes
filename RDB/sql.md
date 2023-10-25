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

# [Tesla SQL approaches](https://www.xiaohongshu.com/explore/64c1440e000000000103cd3d)
```sql
-- cumulative reset
WITH daily_user_count AS
(SELECT date, DATE_FORMAT(date, '%Y-%m') AS ym, daily_count 
 FROM (
   SELECT DATE(created_at) AS date, COUNT(id) AS daily_count
   FROM users
   GROUP BY date
 )
)
SELECT date, SUM(daily_count) OVER(PARTITION BY ym ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS monthly_cumulative -- window function
FROM daily_user_count
```
```sql
-- fraudulent upvotes
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
```sql
-- career jumping
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

```


```sql

```


```sql

```



