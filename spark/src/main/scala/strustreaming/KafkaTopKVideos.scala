package streaming

// spark-shell  --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.1.0
object KafkaTopKVideos {

  val spark = SparkSession.builder.appName("Structured_"+KafkaTopKVideos.getClass.getName).getOrCreate()

  import org.apache.spark.sql.functions._
  import org.apache.spark.sql.SparkSession
  import org.apache.spark.sql.streaming.ProcessingTime
  import org.apache.spark.streaming.kafka._


  val source = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "kunliu1.fyre.ibm.com:6667").option("subscribe", "view").load()

  // CAST binary value as string type
  val ds_activity = source.selectExpr("CAST(value AS STRING)").toDF("activity").trigger(ProcessingTime("5 seconds"))

  val ds_video = ds_activity.select("activity").map(row => row.getString(0).split(",")(1)).filter(_ != "?")

  // Currently sort will lead to HDFSBackedStateStoreProvider IOException: Failed to rename
  val video_count = ds_video.groupBy("value").count()//.sort("count")//.orderBy($"count".desc)

  //val query = video_count.writeStream.trigger(ProcessingTime("5 seconds")).outputMode("complete").format("console")
  val query = video_count.writeStream.outputMode("complete").format("console")

  query.start()
  query.awaitTermination()

}