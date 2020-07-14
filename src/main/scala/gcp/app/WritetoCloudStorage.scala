package gcp.app

import gcp.utils.SparkSessionWrapper
import org.apache.spark.sql.SaveMode

object WritetoCloudStorage extends App with SparkSessionWrapper {
  val datasetNTableName: String = args(0).toString
  val destBucket: String = s"gs://${args(1).toString}/guitars"
  // Read From BigQuery
  val bigQueryDF =  spark
    .read
    .format("bigquery")
    .option("table",datasetNTableName)
    .load()

  bigQueryDF.write.mode(SaveMode.Overwrite).json(destBucket)

}
