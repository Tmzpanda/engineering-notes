# duplicate
```sql
-- DISTINCT
SELECT DISTINCT id, name, department, salary
FROM Employee
```
```sql
-- GROUP BY
SELECT id, name, dept_id, salary
FROM Employee
GROUP BY id, name, dept_id, salary
HAVING COUNT(*) > 1
```
```sql
-- ROW_NUMBER
WITH Temp AS (
  SELECT
    id, name, dept_id, salary, ROW_NUMBER() OVER (PARTITION BY id, name, dept_id, salary ORDER BY salary DESC) AS row_num
    FROM Employee
)
SELECT id, name, dept_id, salary
FROM Temp
WHERE row_num > 1;
```

# find nth highest salary
```sql
SELECT name, salary
FROM Employee
WHERE salary = (
  SELECT DISTINCT salary
  FROM Employee
  ORDER BY salary DESC
  LIMIT n-1, 1 -- skip n-1 retrive 1
);
```
```sql
-- deduplicate
SELECT name, salary FROM (
  SELECT name, salary, DENSE_RANK() OVER(ORDER BY salary DESC) AS rank 
  FROM Employee
  )
WHERE rank = n;
```
```sql
-- find nth highest salary in each department
WITH Temp AS
(
    SELECT *, DENSE_RANK() OVER(PARTITION BY dept_id ORDER BY salary DESC) AS rank
    FROM Employee  
)
SELECT T.name AS employee, D.name AS department, T.salary 
FROM Temp T
JOIN Department D ON Temp.dept_id = Department.id
WHERE Temp.rank == n
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
WITH daily_user_count AS
(
 SELECT date, SUBSTRING(date, 1, 7) AS ym, daily_count 
 FROM (
   SELECT DATE(created_at) AS date, COUNT(id) AS daily_count
   FROM users
   GROUP BY date
 )
)
SELECT date, SUM(daily_count) OVER(PARTITION BY ym ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS monthly_cumulative 
FROM daily_user_count
```

# [Tesla SQL approaches](https://www.xiaohongshu.com/explore/64c1440e000000000103cd3d)
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

```



```sql

```


```sql

```


```sql

```



