### Spark structured streaming reads from Kafka
``` scala



val streamingInputDF = spark
  .readStream
  .format("kafka")
  .option("kafka.bootstrap.servers", "host1:port1,host2:port2")
  .option("subscribe", "topic1,topic2")           
  .load()  // #of consumer instances = #of topic partitions by default
  
  
streamingInputDF.printSchema
```
 
 
### Streaming operations
```scala
import org.apache.spark.sql.functions._

var df = streamingInputDF
  .select(get_json_object(($"value").cast("string"), "$.zip").alias("zip"))
  .groupBy($"zip")
  .count()
  
 
// windowing - find out traffic per zip code for a 10 minute window interval, 
// with sliding duration of 5 minutes starting 2 minutes past the hour
var df = streamingInputDF
  .select(get_json_object(($"value").cast("string"), "$.zip").alias("zip"),
get_json_object(($"value").cast("string"), "$.hittime").alias("hittime"))
  .groupBy($"zip"， window($"hittime".cast("timestamp"), "10 minutes", "5 minutes")) // window: 窗口大小10分钟，每5分钟trigger一次
  .count()
 
display(df)

```

### Write stream
https://www.databricks.com/blog/2017/04/04/real-time-end-to-end-integration-with-apache-kafka-in-apache-sparks-structured-streaming.html
```scala
import org.apache.spark.sql.streaming.ProcessingTime

// write to file
val query = df
  .writeStream
  .format("parquet")
  .option("path", "/mnt")
  .option("checkpointLocation", "path/to/checkpoint/dir")     // checkpoint
  .outputMode("complete")                   // outputMode
  .trigger(ProcessingTime("10 seconds"))    // trigger
  .start()   

   
                          
                             
// write to database
class JDBCSink(url:String, usr:String, pwd:String) extends ForeachWriter[(String, String)]{
...
}
val writer = new JDBCSink(url, usr, pwd)


val query = df
  .writeStream
  .foreach(writer)       // a custom JDBC Sink that extends ForeachWriter and implements its methods
  .outputMode("update")                   
  .trigger(ProcessingTime("10 seconds"))    
  .start()   


```


