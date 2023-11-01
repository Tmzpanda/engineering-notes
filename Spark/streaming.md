# streaming operations

```scala
// watermark
val processed = stream
  .selectExpr("SPLIT(value, '@') AS parts")
  .withColumn("usage", col("parts").getItem(0).cast(DoubleType))
  .withColumn("timestamp", col("parts").getItem(1).cast(TimestampType))
  .drop("parts")
  .withWatermark(eventTime="timestamp", delayThreshold="1 minutes") 
  .groupBy("timestamp")
  .sum(usage)

```

```scala
// windowing
stream
  .withWatermark("timestamp", "10 minutes")  
  .groupBy(
    window(timeColumn=$"timestamp", windowDuration="5 minutes", slideDuration="1 minutes"),  // window of 10mins, triggered every 5mins
    $"zip")
  .count

```

```scala
// trigger
processed.writeStream
  .format("console")
  .outputMode("update") 
  .trigger(Trigger.ProcessingTime("1 minute"))  
  .start()
  .awaitTermination()

```

```scala
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
  .outputMode("append")  \
  .trigger(Trigger.ProcessingTime("1 minute"))  
  .foreach(new HBaseForeachWriter()) // custom ForeachWriter
  .start()
  .awaitTermination()
```
