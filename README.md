# kafka-pyspark-structured-streaming

This is POC for log analysis using Kakfa and Spark (for the peace of my mind)

But it can be a great place to get your hands dirty if you know the basics of kafka and spark.

## About
If you look at the docker-compose file you will notice that this project has 4 docker containers.
- Zookeeeper: Looks after kafka cluster
- Kafka: Our kafka cluster has only one broker
- Kafka Producer: Generates dummy syslog message and send it over kafka
- Spark Analytics: Analyzes syslog messages over sliding windows and prints result like this in console.
 
 ### Output
 Window: 10 minutes, Slides: each 5 minutes, Calculates: Total messages per severity level
 ```text
-------------------------------------------
Batch: 1
-------------------------------------------
+------------------------------------------+--------+-----+
|window                                    |severity|count|
+------------------------------------------+--------+-----+
|[2020-06-08 07:26:00, 2020-06-08 07:31:00]|emerg   |695  |
|[2020-06-08 07:30:00, 2020-06-08 07:35:00]|emerg   |695  |
|[2020-06-08 07:28:00, 2020-06-08 07:33:00]|err     |668  |
|[2020-06-08 07:29:00, 2020-06-08 07:34:00]|crit    |650  |
|[2020-06-08 07:27:00, 2020-06-08 07:32:00]|alert   |654  |
|[2020-06-08 07:30:00, 2020-06-08 07:35:00]|err     |668  |
|[2020-06-08 07:28:00, 2020-06-08 07:33:00]|notice  |641  |
|[2020-06-08 07:28:00, 2020-06-08 07:33:00]|warning |680  |
|[2020-06-08 07:30:00, 2020-06-08 07:35:00]|crit    |650  |
|[2020-06-08 07:26:00, 2020-06-08 07:31:00]|notice  |641  |
|[2020-06-08 07:27:00, 2020-06-08 07:32:00]|notice  |641  |
|[2020-06-08 07:30:00, 2020-06-08 07:35:00]|debug   |641  |
|[2020-06-08 07:30:00, 2020-06-08 07:35:00]|warning |680  |
|[2020-06-08 07:30:00, 2020-06-08 07:35:00]|notice  |641  |
|[2020-06-08 07:29:00, 2020-06-08 07:34:00]|warning |680  |
|[2020-06-08 07:27:00, 2020-06-08 07:32:00]|debug   |641  |
|[2020-06-08 07:26:00, 2020-06-08 07:31:00]|alert   |654  |
|[2020-06-08 07:29:00, 2020-06-08 07:34:00]|err     |668  |
|[2020-06-08 07:27:00, 2020-06-08 07:32:00]|crit    |650  |
|[2020-06-08 07:27:00, 2020-06-08 07:32:00]|warning |680  |
+------------------------------------------+--------+-----+
only showing top 20 rows

```

 Window: 1 minutes, Slides: each 1 minutes, Calculates: Total messages per hostname
```text
-------------------------------------------
Batch: 1
-------------------------------------------
+------------------------------------------+---------------------------+-----+
|window                                    |hostname                   |count|
+------------------------------------------+---------------------------+-----+
|[2020-06-08 07:30:00, 2020-06-08 07:31:00]|email-83.blackburn.biz     |72   |
|[2020-06-08 07:30:00, 2020-06-08 07:31:00]|srv-69.price-bray.net      |76   |
|[2020-06-08 07:30:00, 2020-06-08 07:31:00]|laptop-63.roberts.net      |80   |
|[2020-06-08 07:30:00, 2020-06-08 07:31:00]|desktop-68.caldwell.com    |72   |
|[2020-06-08 07:30:00, 2020-06-08 07:31:00]|desktop-40.fisher-allen.com|77   |
|[2020-06-08 07:30:00, 2020-06-08 07:31:00]|db-26.keller-miller.biz    |74   |
|[2020-06-08 07:30:00, 2020-06-08 07:31:00]|web-11.ortega.net          |75   |
|[2020-06-08 07:30:00, 2020-06-08 07:31:00]|desktop-28.hayes-pierce.org|71   |
|[2020-06-08 07:30:00, 2020-06-08 07:31:00]|db-21.white-hensley.com    |74   |
|[2020-06-08 07:30:00, 2020-06-08 07:31:00]|lt-33.lara.info            |75   |
|[2020-06-08 07:30:00, 2020-06-08 07:31:00]|web-09.richards.com        |72   |
|[2020-06-08 07:30:00, 2020-06-08 07:31:00]|email-91.gonzalez-ruiz.com |67   |
|[2020-06-08 07:30:00, 2020-06-08 07:31:00]|lt-92.wilkinson-boone.net  |69   |
|[2020-06-08 07:30:00, 2020-06-08 07:31:00]|email-19.espinoza.biz      |68   |
|[2020-06-08 07:30:00, 2020-06-08 07:31:00]|lt-12.mcbride-walker.com   |76   |
|[2020-06-08 07:30:00, 2020-06-08 07:31:00]|desktop-58.nichols.com     |73   |
|[2020-06-08 07:30:00, 2020-06-08 07:31:00]|laptop-97.wilson.com       |76   |
|[2020-06-08 07:30:00, 2020-06-08 07:31:00]|laptop-82.combs-lewis.com  |71   |
|[2020-06-08 07:30:00, 2020-06-08 07:31:00]|email-28.benson.biz        |80   |
|[2020-06-08 07:30:00, 2020-06-08 07:31:00]|db-60.ramirez.org          |71   |
+------------------------------------------+---------------------------+-----+
only showing top 20 rows

```

We can store these results in database too.

## How to run
```bash
$ git clone https://github.com/faysal-ishtiaq/kafka-pyspark-structured-streaming.git
$ cd kafka-pyspark-structured-streaming
$ docker-compose up -d
$ docker logs -f spark_analytics # to see the outputs
```