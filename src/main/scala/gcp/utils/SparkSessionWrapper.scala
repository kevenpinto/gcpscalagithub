package gcp.utils

import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.SparkSession

trait SparkSessionWrapper {
  Logger.getLogger("org").setLevel(Level.ERROR)

  lazy val spark: SparkSession = {
    SparkSession
      .builder()
      .appName("Run Spark on DataProc in GCP")
      //.config("spark.master","local")
      .getOrCreate()
  }
}

