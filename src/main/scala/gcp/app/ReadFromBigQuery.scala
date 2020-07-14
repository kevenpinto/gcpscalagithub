package gcp.app
import gcp.utils.SparkSessionWrapper

object ReadFromBigQuery extends App with SparkSessionWrapper {
  val datasetNTableName1: String = AppConfig.srcTable1
  val bigQueryDF1 =  spark
    .read
    .format("bigquery")
    .option("table",datasetNTableName1)
    .load()
  bigQueryDF1.show(truncate=false)

  val datasetNTableName2: String = AppConfig.srcTable2
  println(s"datasetNTableName2 = $datasetNTableName2")
}

// gcloud dataproc jobs submit spark --cluster=scalatest --region=us-central1 --class=gcp.app.ReadFromBigQuery --jars=gs://kpi01-jars/dataproc1-0.1.jar,gs://spark-lib/bigquery/spark-bigquery-latest.jar -- data-cn-landd.spark_read_demos.guitars


