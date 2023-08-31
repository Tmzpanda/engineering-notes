# SparkSession
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, from_json, concat_ws, lit
from pyspark.sql.types import StructType, StructField, StringType

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
df = spark.read.csv('filename.csv', header=True, inferSchema=True)

# explore
df.printSchema()
df.select('col').show(5)
df.drop('col)
df['survey_categoty'].distinct
df.select('survey_type', 'survey_category').distinct().show(100, False)

# clean
# Trim the spaces from the column names
df = df.toDF(*[c.strip() for c in df.columns])

# Trim the spaces from the column values
df = df.select([trim(c).alias(c) if c.dtype == 'string' else c for c in df.columns])

# deduplicate
df = df.dropDuplicates(["col1", "col2"])

# transform
df_transformed = df.select(col("id"),
                           concat_ws(' ', col("first_name"), col("second_name")).alias("name"),
                           (col("floor") * lit(steps_per_floor)).alias("steps_to_desk"))

# rename
df = df.withColumnRenamed("old_col", "new_col")

# add a column
df.withColumn('advantage_login_date_1', to_date(coalesce(fma.advantage_login_date, lit('1900-01-01')),"yyyy-MM-dd"))

# cast
df = df.withColumn("new_col", col("old_col").cast("integer"))

# json explode
# pattern matching
json_schema = StructType([
    StructField("key", StringType()), 
    StructField("value", StringType())
    ])
df = df.withColumn("exploded", explode(from_json("json_column", json_schema)))


# filter
df = df.filter(col("column_name") > 10)
df = df.filter(df.native_country != 'Holand-Netherlands')
df.filter("survey_di = 'bcbssc").groupBy('survey_id').count.show(10,false)

# regex
df = df.filter(expr("column_name LIKE 'pattern%'"))



# join
df = df.join(df_dim, on="common_column", how="inner")

# aggregate
df.filter(df.native_country == 'Holand-Netherlands').count()
df.groupBy('partner', 'client_hierarchy').count().sort(desc('count'))
df.groupBy("education").count().sort("count",ascending=True).show()
df.groupby('marital').agg({'capital_gain': 'mean'}).show()
df.groupby('native_country').agg({'native_country': 'count'}).sort(asc("count(native_country)")).show()
df = df.groupBy("group_column").agg(sum("numeric_column"), avg("numeric_column"), max("numeric_column"))
# Find the highest salary for each department
highest_salaries = df.groupBy('department').agg(max('salary').alias('highest_salary'))
highest_salaries.show()


# load 

df_transformed\
    .write\
    .csv("resources/loaded_data", mode="overwrite", header=True)

# feature engineer
# onehotencoder



