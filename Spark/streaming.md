
```pyspark code

# streaming from tcp socekt
df = spark.readStream
      .format("socket")
      .option("host","localhost")
      .option("port","9090")
      .load()


query = count.writeStream
      .format("console")
      .outputMode("complete")
      .start()
      .awaitTermination()


# streaming from kafka
df = spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "192.168.1.100:9092")
        .option("subscribe", "json_topic")
        .option("startingOffsets", "earliest") // From starting
        .load()


df.selectExpr("CAST(id AS STRING) AS key", "to_json(struct(*)) AS value")
   .writeStream
   .format("kafka")
   .outputMode("append")
   .option("kafka.bootstrap.servers", "192.168.1.100:9092")
   .option("topic", "josn_data_topic")
   .start()
   .awaitTermination()



```


## Streaming



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

```scala

val windowedCounts = words
    .withWatermark("timestamp", "10 minutes")               // watermark: 在12:20trigger时, watermark 为 12:21 - 10m = 12:11，所以late data (12:04, donkey)丢弃了。
    .groupBy(
        window($"timestamp", "10 minutes", "5 minutes"),    // window: 窗口大小10分钟，每5分钟trigger一次
        $"word")
    .count()


/*
- window: aggregation 
- watermark: late data(ProcessingTime比EventTime晚），更新其对应的ResultTable的记录。
- stateful operator

*/
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




/*
- trigger模式
  - micro-batch(default): exactly-once 语义。原因是因为在input端和output端都做了很多工作来进行保证幂等。
  - continuous mode: at-least-once(处理完才commit, 处理错误会重操作。需要保证幂等性（两次处理不会影响系统）)

- 三种输出模式
  - 附加模式（Append Mode）(default)：上一次触发之后新增加的行才会被写入外部存储，老数据有改动不适合该模式
  - 更新模式（Update Mode）：上一次触发之后被更新的行才会被写入外部存储
  - 完全模式（Complete Mode）：整个更新过的输出表都被写入外部存储
  
*/
```



 










