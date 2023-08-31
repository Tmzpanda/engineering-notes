# SparkSession
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[1]") \
    .appName("spark demo") \
    .getOrCreate() 


# create spark df
data = [["James","Smith",30,"M"], 
        ["Michael","Rose",50,"M"], 
        ["Robert","Williams",42,""], 
        ["Maria","Jones",38,"F"], 
        ["Jen","Brown",45,None]
       ] 
columns = ['First Name','Last Name','Age','Gender']
df = spark.createDataFrame(data=data, schema=columns)


# read from csv
df = spark.read.csv("/tmp/resources/zipcodes.csv")


# explore
df.printSchema()
df.select('col').show(5)
df.drop('col)


# clean
df.filter(df.age > 40)
df = df.withColumn("age_square", col("age")**2)
df.filter(df.native_country != 'Holand-Netherlands')



# aggregate
df.filter(df.native_country == 'Holand-Netherlands').count()
df.groupBy("education").count().sort("count",ascending=True).show()
df.groupby('marital').agg({'capital_gain': 'mean'}).show()
df.groupby('native_country').agg({'native_country': 'count'}).sort(asc("count(native_country)")).show()



# feature engineer
# onehotencoder




#e.g. Spark transforms the unstructured logs, applies schema and insert into target table, 
# transformations includes cleansing (e.g. deduplicate, rename, cast, json explode, filter), enrichment (join, aggregations), etc.


# Read the CSV file into a PySpark DataFrame
df = spark.read.csv('filename.csv', header=True, inferSchema=True)

# Trim the spaces from the column names
df = df.toDF(*[c.strip() for c in df.columns])

# Trim the spaces from the column values
df = df.select([trim(c).alias(c) if c.dtype == 'string' else c for c in df.columns])

# Find the highest salary for each department
highest_salaries = df.groupBy('department').agg(max('salary').alias('highest_salary'))

# Show the results
highest_salaries.show()









from sparksql.context import spark_session
from pyspark.sql.functions import col, concat_ws,lit
import json


def process():
    # extract
    df = spark_session \
        .read \
        .parquet("resources/employees")
    df.show(5)

    # transform
    with open("resources/etl_config.json", 'r') as config_file:
        config_dict = json.load(config_file)
    steps_per_floor = config_dict["steps_per_floor"]

    df_transformed = df.select(col("id"),
                               concat_ws(' ', col("first_name"), col("second_name")).alias("name"),
                               (col("floor") * lit(steps_per_floor)).alias("steps_to_desk"))
    df_transformed.show(5)

    # load
    df_transformed\
        .write\
        .csv("resources/loaded_data", mode="overwrite", header=True)


if __name__ == '__main__':
    process()
    
---

# df

df = spark.read.table('edw.dim_survey_definition')
df.printSchema()

hadoop fs -ls /prod/data/etl/mongo_extracts/missions/missionInstance/year=2022/month=01/
df_1 = spark.read.parquet("/prod/data/etl/mongo_extracts/missions/missionInstance/year=2022/month=01/day=28")

hadoop fs -ls /prod/data/etl/mongo_extracts/survey/surveyQuestionDefinition/ 
df = spark.read.json("/prod/data/etl/mongo_extracts/survey/surveyQuestionDefinition/")


df['survey_categoty'].distinct
df.select('survey_type', 'survey_category').distinct().show(100, False)

df.filter("survey_di = 'bcbssc").groupBy('survey_id').count.show(10,false)
df.groupBy('partner', 'client_hierarchy').count().sort(desc('count'))


df.withColumn('advantage_login_date_1', to_date(coalesce(fma.advantage_login_date, lit('1900-01-01')),"yyyy-MM-dd"))



df.write.saveAsTable('edw_tim.stg_stats')

df.coalesce(1).
    write.
    option("sep","|").
    option("header","true").
    csv("dsd.csv")




----------------------------------------------------------------------------------------------------------------
# console

spark2-submit \
--executor-memory 5g \
--conf spark.dynamicAllocation.minExecutors=5 \
--conf spark.dynamicAllocation.enabled=true \
--conf spark.dynamicAllocation.maxExecutors=10 \
--conf spark.yarn.executor.memoryOverhead=1024 \
--executor-cores 5 \
--driver-memory 5g \
agg_daily_summary.py \
--db edw --etl-start-date 2021-11-01 \
--etl-end-date 2021-11-16



pyspark2 --executor-memory 10g \
--executor-cores 5 \
--conf spark.dynamicAllocation.enabled=true \
--conf spark.dynamicAllocation.minExecutors=5 \
--conf spark.dynamicAllocation.maxExecutors=10 \
--conf spark.hadoop.hive.exec.dynamic.partition=true



pyspark2 --executor-memory 10g --conf spark.dynamicAllocation.enabled=true --conf spark.dynamicAllocation.minExecutors=10 --conf spark.dynamicAllocation.maxExecutors=20 --conf spark.hadoop.hive.exec.dynamic.partition=true --conf spark.hadoop.hive.exec.dynamic.partition.mode=nonstrict
--conf spark.hadoop.hive.exec.max.dynamic.partitions=1200 


----------------------------------

