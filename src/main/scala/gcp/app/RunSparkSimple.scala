package gcp.app

import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.{DataFrame, SparkSession}
import gcp.utils.SparkSessionWrapper

object RunSparkSimple extends App with SparkSessionWrapper {
 import spark.implicits._
  val df: DataFrame = Seq(
    (1,"Apple"),
    (1,"Banana"),
    (3,"Pear")
  ).toDF("id","name")
  df.show(truncate = false)
}

//gcloud dataproc jobs submit spark --cluster=scalatest --region=us-central1 --class=gcp.app.RunSparkSimple --jars=gs://kpi01-jars/dataproc1_2.11-0.1.jar