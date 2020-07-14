gcloud dataproc jobs submit spark --cluster=scalatest --region=us-central1 \
--class=gcp.app.WritetoCloudStorage --jars=gs://kpi01-jars/dataproc1-0.1.jar,gs://spark-lib/bigquery/spark-bigquery-latest.jar \
-- data-cn-landd.spark_read_demos.guitars kpi01-data