package gcp.app
import gcp.utils.SparkSessionWrapper
import org.apache.spark.sql.DataFrame
object ReadFileFromCloudStorage extends App with SparkSessionWrapper{
  val usage = """ Usage: ReadFileFromCloudStorage [gs://....]"""
  if (args.length == 0) {
    println(s"Insufficient Args !!: $usage")
  }
  else
    {
      args.toList match {
        case List(x) if x.startsWith("gs://") => val guitarsDF: DataFrame = spark
                                                                      .read
                                                                      .option("inferSchema","true")
                                                                      .json(x)
          guitarsDF.show()
        case _ => println(s"Invalid cloud Storage Path: $usage")
      }
    }
}

//gcloud dataproc jobs submit spark --cluster=scalatest --region=us-central1 --class=gcp.app.ReadFileFromCloudStorage --jars=gs://kpi01-jars/dataproc1_2.11-0.1.jar -- gs://kpi01-data/guitars.json