// Spark Structured Streaming reads from Kafka
val spark = SparkSession
  .builder()
  .master("local[*]")
  .config("spark.sql.streaming.checkpointLocation", "path/to/checkpoint/dir")  // checkpoint
  .getOrCreate()

val stream = spark.readStream
  .format("kafka")
  .option("kafka.bootstrap.servers", "192.168.1.100:9092")
  .option("subscribe", "topic")
  .option("startingOffsets", "latest")
  .load()  // #of consumer instances = #of topic partitions by default

val processed = stream
  .selectExpr("SPLIT(value, '@') AS parts")
  .withColumn("usage", col("parts").getItem(0).cast(DoubleType))
  .withColumn("timestamp", col("parts").getItem(1).cast(TimestampType))
  .drop("parts")
  .withWatermark(eventTime="timestamp", delayThreshold="10 minutes") 
  .groupBy("timestamp")
  .sum(usage)

stream
  .withWatermark("timestamp", "10 minutes")  // if trigger at 12:10, watermark = 12:10-10mins = 12:00，then late data (11:04, donkey) will be discarded
  .groupBy(
    window("timestamp", "10 minutes", "5 minutes"),  // sliding window 10mins, triggered every 5mins
    "zip")
  .count

processed.writeStream
  .format("csv")
  .outputMode("append")  
  .start(path="output")
  .awaitTermination

// batch
df.write   
  .format("csv")
  .save(path="output")

// ForeachWriter


