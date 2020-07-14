package gcp.app

import com.typesafe.config.ConfigFactory

object AppConfig {
  val conf = ConfigFactory.load()
  val srcTable1 = conf.getString("bigquery.src_table1")
  val srcTable2 = conf.getString("bigquery.src_table2")
}
