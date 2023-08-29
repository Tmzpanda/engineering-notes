
## RDD, DF, DS
[转换](https://blog.csdn.net/muyingmiao/article/details/102963103)                  

[操作](https://github.com/Tmzpanda/spark-demo/blob/master/src/main/scala/com/tmzpanda/spark/sparksql/DataFrame_Functions.scala)

/**************************************************** create dataframe ********************************************************/
// Seq
import spark.implicits._
val df = Seq(("DEPT1", 1000), ("DEPT1", 500), ("DEPT1", 700), ("DEPT2", 400), ("DEPT2", 200),  ("DEPT3", 500), ("DEPT3", 200))
         .toDF("department", "salary")

// csv
import spark.implicits._
val df = spark
        .read
        .option("header", "true")
        .csv("src/main/resources/questions_10K.csv") // json, text, parquet
        .toDF("id", "creation_date", "closed_date", "deletion_date", "score", "owner_user_id", "answer_count")

df.write
  .parquet("file.parquet")

df.write
  .format("csv")
  .save("file_path")


// hive
val spark = SparkSession
  .builder()
  .appName("Spark-Hive")
  .config("spark.sql.warehouse.dir", warehouseLocation)
  .enableHiveSupport()
  .getOrCreate()

import spark.implicits._
import spark.sql
val df = sql("SELECT key, value FROM src WHERE key < 10 ORDER BY key")

df.write.
  mode(SaveMode.Overwrite).
  saveAsTable("hive_records")


// jdbc
val df = spark.read
    .jdbc("jdbc:mysql://localhost:3306", "employees.dept_emp", connectionProperties)
    .toDF("Employee ID", "Department Code", "From Date", "To Date")



// rdd to df
val rdd = sc.parallelize(Seq(("Sales", 101, 30000), ("IT", 203, 40000)))
val rdd = sc.textFile("file.txt")

import spark.implicits._
val df = rdd.toDF("department", "eid", "salary")
val df = spark.createDataFrame(rdd).toDF("department", "eid", "salary")


// Dataset -> type safe 
// Dataframe: Dataset[Row]
case class Record (department: String, eid: Double, salary: Double)
import spark.implicits._
val ds = df.as[Record]  // implicit conversion

val data = Seq(Person("Bob", 21), Person("Mandy", 22), Person("Julia", 19))
val ds = spark.createDataset(data)




/**************************************************** dataframe SQL ********************************************************/

// split
val dfSplit = df.select(split(df("field"), "\\|").getItem(0).alias("name"),
                        split(df("field"), "\\|").getItem(1).alias("brand"),
                        split(df("field"), "\\|").getItem(2).alias("rating"),
                        split(df("field"), "\\|").getItem(3).alias("login"),
                        split(df("field"), "\\|").getItem(4).alias("ptype"),
                        split(df("field"), "\\|").getItem(5).alias("slot"),
                        split(df("field"), "\\|").getItem(6).alias("pos"))
dfSplit.show()

// explode
val dfExplode = df.select(col("id"), col("name"), explode(col("data")).alias("fruit"))



// window function
import sparkSession.implicits._
val df = Seq(("DEPT1", 1000), ("DEPT1", 500), ("DEPT1", 700), ("DEPT2", 400), ("DEPT2", 200),  ("DEPT3", 500), ("DEPT3", 200))
         .toDF("department", "salary")

df.withColumn("rank", dense_rank().over(Window.partitionBy($"department").orderBy($"assetValue".desc))).filter("rank = 1").show


// aggregation function
df.groupBy($"department").count.orderBy($"count".desc).limit(2)   // return a df
df.groupBy($"department").agg(count($"eid"), mean($"salary")).show


// filter
val items = List("a", "b", "c")
val items = df1.select("department").distinct.map(x=>x.getString(0)).collect.toList
df.filter(!$"department".isin(items:_*))   // unpack the list into arguments with the :_* operator


// join
df.join(df1, df("department") === df1("department"), "left_anti").show













