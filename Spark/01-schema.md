# sample record
```json
{
    "frequency": 10,
    "data": [
        {
            "timestamp": "2023-04-12T06:07:22+00:00",
            "notes": "no instrument errors!",
            "data": [
                {
                    "data_type": "Big Box",
                    "instrument_name": "AIC1003.Val_SP",
                    "instrument_type": "Opus",
                    "is_setpoint": true,
                    "number_value": 300.0,
                    "is_baddata": false,
                    "original_timestamp": "2023-04-03T22:43:49.873321+00:00"
                },
                {
                    "data_type": "Big Box",
                    "instrument_name": "FIC1010.Val_PV",
                    "instrument_type": "Opus",
                    "is_setpoint": false,
                    "number_value": 0.0,
                    "is_baddata": false,
                    "original_timestamp": "2023-04-03T22:43:49.873321+00:00"
                },
                {
                    "data_type": "Big Box",
                    "instrument_name": "FIC1010.Val_SP",
                    "instrument_type": "Opus",
                    "is_setpoint": true,
                    "number_value": 0.0,
                    "is_baddata": false,
                    "original_timestamp": "2023-04-03T22:43:49.873321+00:00"
                }
            ]
        }
    ]
}
```

# read from Kafka
```py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, explode
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, BooleanType, DoubleType, TimestampType

spark = SparkSession.builder \
    .appName("pi2kiwi") \
    .getOrCreate()

kafka_params = {
    "kafka.bootstrap.servers": "your_broker_list",
    "subscribe": "topic",
    "startingOffsets": "latest"  
}

kafka_stream = spark.readStream \
    .format("kafka") \
    .options(**kafka_params) \
    .load()    # #of consumer instances = #of topic partitions by default

```

```py
# schema contract 
schema = StructType([
    StructField("frequency", IntegerType()),
    StructField("data", ArrayType(StructType([
        StructField("timestamp", TimestampType()),
        StructField("notes", StringType()),
        StructField("data", ArrayType(StructType([
            StructField("data_type", StringType()),
            StructField("instrument_name", StringType()),
            StructField("instrument_type", StringType()),
            StructField("is_setpoint", BooleanType()),
            StructField("number_value", DoubleType()),
            StructField("is_baddata", BooleanType()),
            StructField("original_timestamp", StringType())
        ])))
    ])))
])

parsed_data = kafka_stream.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("message")) 

```
```py
# retrive schema contract from Schema Registry
from confluent_kafka.avro import CachedSchemaRegistryClient

schema_registry_client = CachedSchemaRegistryClient({"url": "http://your-schema-registry-url:8081")
schema = schema_registry_client.get_latest_schema("your_kafka_topic").schema

parsed_data = kafka_stream.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("message")) 

```

```py
# schema enforcement
class Record:
    def __init__(self, frequency, timestamp, notes, data_type, instrument_name, instrument_type, is_setpoint, number_value, is_baddata, original_timestamp):
        self.frequency = frequency
        self.timestamp = timestamp
        self.notes = notes
        self.data_type = data_type
        self.instrument_name = instrument_name
        self.instrument_type = instrument_type
        self.is_setpoint = is_setpoint
        self.number_value = number_value
        self.is_baddata = is_baddata
        self.original_timestamp = original_timestamp

flattened_data = parsed_data.select(
    col("message.frequency"),
    explode(col("message.data")).alias("data")    
).select(
    col("frequency"),
    col("data.timestamp").alias("timestamp"),
    col("data.notes").alias("notes"),
    explode(col("data.data")).alias("data")
).select(
    col("frequency"),
    col("timestamp"),
    col("notes"),
    col("data.data_type").alias("data_type"),
    col("data.instrument_name").alias("instrument_name"),
    col("data.instrument_type").alias("instrument_type"),
    col("data.is_setpoint").alias("is_setpoint"),
    col("data.number_value").alias("number_value"),
    col("data.is_baddata").alias("is_baddata"),
    col("data.original_timestamp").alias("original_timestamp")
).as[Record]

```

```py
bq_output_options = {
    "table": "your_project_id.your_dataset.your_table",  
    "project": "your_project_id",  
    "location": "US",  
    "temporaryGcsBucket": "your_bucket", 
}

query = dataset.writeStream \
    .format("bigquery")  \
    .outputMode("append") \
    .option("checkpointLocation", "your_checkpoint_location")  \
    .options(**bq_output_options)  \
    .start()  \
    .awaitTermination()

```

# read from json
```py
json_data = spark.read.json("path_to_your_json_file.json", schema=schema)

flattened_data = json_data.select(
    col("frequency"),
    explode(col("data")).alias("data")
).select(
    col("frequency"),
    col("data.timestamp").alias("timestamp"),
    col("data.notes").alias("notes"),
    explode(col("data.data")).alias("data")
).select(
    col("frequency"),
    col("timestamp"),
    col("notes"),
    col("data.data_type").alias("data_type"),
    col("data.instrument_name").alias("instrument_name"),
    col("data.instrument_type").alias("instrument_type"),
    col("data.is_setpoint").alias("is_setpoint"),
    col("data.number_value").alias("number_value"),
    col("data.is_baddata").alias("is_baddata"),
    col("data.original_timestamp").alias("original_timestamp")
)

```
