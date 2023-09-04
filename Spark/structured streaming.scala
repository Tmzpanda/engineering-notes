import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.streaming.Trigger

// Spark Structured Streaming reads from Kafka
val spark = SparkSession
  .builder()
  .master("local[*]")
  .config("spark.sql.streaming.checkpointLocation", "path/to/checkpoint/dir")  // checkpoint
  .getOrCreate()

import spark.implicits._

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
  .withWatermark(eventTime="timestamp", delayThreshold="1 minutes") // watermark
  .groupBy("timestamp")
  .sum(usage)

processed.writeStream
  .format("csv")
  .start(path="output")  // file-based sink
  .awaitTermination()

// windowing
stream
  .withWatermark("timestamp", "10 minutes")  
  .groupBy(
    window(timeColumn=$"timestamp", windowDuration="5 minutes", slideDuration="1 minutes"),  // window of 10mins, triggered every 5mins
    $"zip"
  )
  .count

// trigger
processed.writeStream
  .format("console")
  .outputMode("update")  // output mode
  .trigger(Trigger.ProcessingTime("1 minute"))  // trigger
  .start()
  .awaitTermination()

// batch
df.write   
  .format("csv")
  .save(path="output")

// custom ForeachWriter
class HBaseForeachWriter extends ForeachWriter[Row] {        // ForeachWriter
  override def open(partitionId: Long, epochId: Long): Boolean = {
    
  }

  override def process(value: Row): Unit = {
    
  }

  override def close(errorOrNull: Throwable): Unit = {
    
  }
}

processed.writeStream
  .outputMode("update")  // output mode
  .trigger(Trigger.ProcessingTime("1 minute"))  // trigger
  .foreach(new HBaseForeachWriter()) // custom ForeachWriter
  .start()
  .awaitTermination()

