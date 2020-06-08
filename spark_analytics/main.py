from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, DecimalType
from pyspark.sql.functions import *

json_schema = StructType()\
    .add("severity", StringType())\
    .add("facility", StringType())\
    .add("version", DecimalType())\
    .add("timestamp", StringType())\
    .add("hostname", StringType())\
    .add("appname", StringType())\
    .add("procid", DecimalType())\
    .add("msgid", StringType())\
    .add("sd", StringType())\
    .add("msg", StringType())

if __name__ == "__main__":
    sc = SparkContext()
    sc.setLogLevel("ERROR")
    spark = SparkSession.builder.appName("SyslogAnalyzer").getOrCreate()

    messages = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "syslog") \
        .load() \
        .select(from_json(col("value").cast("string"), json_schema).alias("parsed_logs")) \
        .select(
        "parsed_logs.severity",
        "parsed_logs.facility",
        "parsed_logs.version",
        "parsed_logs.timestamp",
        "parsed_logs.hostname",
        "parsed_logs.appname",
        "parsed_logs.procid",
        "parsed_logs.msgid",
        "parsed_logs.sd",
        "parsed_logs.msg"
    )

    severity = messages.groupBy(window(messages.timestamp, "5 minute", "1 minute"), messages.severity).count()
    hostname = messages.groupBy(window(messages.timestamp, "1 minute"), messages.hostname).count()

    # csv_writer = messages \
    #     .writeStream \
    #     .outputMode("append") \
    #     .format("csv") \
    #     .option("path", "/spark_analytics/output") \
    #     .option("checkpointLocation", "/spark_analytics/checkpoint") \
    #     .start()

    severity_writer = severity.writeStream.outputMode("update").format("console").option("truncate", False).start()
    hostname_writer = hostname.writeStream.outputMode("update").format("console").option("truncate", False).start()

    severity_writer.awaitTermination()
    hostname_writer.awaitTermination()
