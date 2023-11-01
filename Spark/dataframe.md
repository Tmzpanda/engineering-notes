# createDataFrame
```py
# createDataFrame
data = [["James","Smith",30,"M"], 
        ["Michael","Rose",50,"M"], 
        ["Robert","Williams",42,""], 
        ["Maria","Jones",38,"F"], 
        ["Jen","Brown",45,None]
       ] 
columns = ['First Name','Last Name','Age','Gender']
df = spark.createDataFrame(data=data, schema=columns)

```

``` scala
// createDataFrame
val data = Seq(("Alice", 30), ("Bob", 25), ("Charlie", 35))
val df = spark.createDataFrame(data).toDF("name", "age")

// implicit conversion
import spark.implicits._
val ds = df.as[Record]  

// toDF
val df = spark.createDataFrame(rdd).toDF("department", "eid", "salary")

// createDataset
val data = Seq(Person("Bob", 21), Person("Mandy", 22), Person("Julia", 19))
val ds = spark.createDataset(data)

// row-specific methods
val firstRow: Row = df.head()
val firstName = firstRow.getAs[String]("name")    
val firstAge = firstRow.getAs[Int]("age")
println(s"First person: Name - $firstName, Age - $firstAge")

df.filter($"age" > 30).show()

// ds
case class Person(name: String, age: Int)
val ds: Dataset[Person] = spark.createDataset(data.map { case (name, age) => Person(name, age) })

ds.filter(person => person.age > 30).show()

```

# transform
```py

# concat_ws
df_transformed = df.select(concat_ws(' ', col("first_name"), col("second_name")).alias("name"),
                           (col("floor") * lit(steps_per_floor)).alias("steps_to_desk"))

# coalesce
df.withColumn('advantage_login_date_1', to_date(coalesce(fma.advantage_login_date, lit('1900-01-01')),"yyyy-MM-dd"))

# filter
df = df.filter(col("column_name") > 10)
df = df.filter(df.native_country != 'Holand-Netherlands')
df.filter("survey_di = 'bcbssc").groupBy('survey_id').count.show(10,false)
df = df.filter(expr("column_name LIKE 'pattern%'"))

# join
df = df.join(df_dim, on="common_column", how="inner")

# groupBy
df.groupBy('partner', 'client_hierarchy').count().sort(desc('count'))
df.groupBy("education").count().sort("count",ascending=True).show()
df.groupby('marital').agg({'capital_gain': 'mean'}).show()
df.groupby('native_country').agg({'native_country': 'count'}).sort(asc("count(native_country)")).show()
df = df.groupBy("group_column").agg(sum("numeric_column"), avg("numeric_column"), max("numeric_column"))

df = df.groupBy('department').agg(max('salary').alias('highest_salary'))
df = df.withColumn('rank', dense_rank().over(Window.partitionBy('dept_id').orderBy(col('salary').desc()))).filter(col('rank') == n)
```

```scala
// split
val dfSplit = df.select(split(df("field"), "\\|").getItem(0).alias("name"),
                        split(df("field"), "\\|").getItem(1).alias("brand"),
                        split(df("field"), "\\|").getItem(2).alias("rating"),
                        split(df("field"), "\\|").getItem(3).alias("login"),
                        split(df("field"), "\\|").getItem(4).alias("ptype"),
                        split(df("field"), "\\|").getItem(5).alias("slot"),
                        split(df("field"), "\\|").getItem(6).alias("pos"))

// window function
import sparkSession.implicits._
val df = Seq(("DEPT1", 1000), ("DEPT1", 500), ("DEPT1", 700), ("DEPT2", 400), ("DEPT2", 200),  ("DEPT3", 500), ("DEPT3", 200))
         .toDF("department", "salary")
df.withColumn("rank", dense_rank().over(Window.partitionBy($"department").orderBy($"assetValue".desc))).filter("rank = 1").show

```





