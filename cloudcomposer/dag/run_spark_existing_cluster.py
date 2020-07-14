from datetime import datetime, timedelta
from airflow import DAG
from airflow.contrib.operators.dataproc_operator import DataProcSparkOperator

# Loads of Info here https://airflow.apache.org/docs/stable/_api/airflow/contrib/operators/dataproc_operator/index.html
TASK_ID = 'dataproc_spark_submit'
MAIN_JAR = 'gs://kpi01-jars/gcpscala-0.1.jar'
JOB_NAME = 'kpi01-RunScalaSparkJob'
MAIN_CLASS = 'gcp.app.RunSparkSimple'
BIG_QUERY_JAR = 'gs://spark-lib/bigquery/spark-bigquery-latest.jar'
CLUSTER_STORAGE_BUCKET = 'kpi01-dataproc-cluster-storage-bucket'
PROJECT = 'data-cn-landd'
ZONE = 'europe-west2-a'
REGION='europe-west2'
CLUSTER_NAME='kpi01-scalateststatic'

SPARK_PROPERTIES = {
 'spark.driver.extraJavaOptions':'-Dbigquery.src_table1=data-cn-landd.scalatesting.cars -Dbigquery.src_table2=data-cn-landd.scalatesting.cars'
}

def getSparkJobHandle(taskID, mainClass):
    return DataProcSparkOperator(
        task_id=taskID,
        region=REGION,
        main_class=mainClass,
        cluster_name=CLUSTER_NAME,
        dataproc_spark_jars=[MAIN_JAR,BIG_QUERY_JAR]
    )

def getSparkJobHandleWithSparkProperties(taskID, mainClass):
    return DataProcSparkOperator(
        task_id=taskID,
        region=REGION,
        main_class=mainClass,
        cluster_name=CLUSTER_NAME,
        dataproc_spark_jars=[MAIN_JAR,BIG_QUERY_JAR],
        dataproc_spark_properties=SPARK_PROPERTIES
    )


# Airflow parameters, see https://airflow.incubator.apache.org/code.html
DEFAULT_DAG_ARGS = {
    'owner': 'airflow',  # The owner of the task.
    # Task instance should not rely on the previous task's schedule to succeed.
    'depends_on_past': False,
    # We use this in combination with schedule_interval=None to only trigger the DAG with a
    # POST to the REST API.
    # Alternatively, we could set this to yesterday and the dag will be triggered upon upload to the
    # dag folder.
    'start_date': datetime(2020, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,  # Retry once before failing the task.
    'retry_delay': timedelta(minutes=1),  # Time between retries.
    'project_id': PROJECT,  # Cloud Composer project ID.
    # We only want the DAG to run when we POST to the api.
    # Alternatively, this could be set to '@daily' to run the job once a day.
    # more options at https://airflow.apache.org/scheduler.html#dag-runs
}

# Create Directed Acyclic Graph for Airflow
with DAG('Run-Some-Scala-on-static-cluster',
         default_args=DEFAULT_DAG_ARGS,
         schedule_interval=None) as dag:  # Here we are using dag as context.
    # Submit our Spark Job
    first_spark_job = getSparkJobHandle("Spark-App1","gcp.app.RunSparkSimple")
    second_spark_job = getSparkJobHandleWithSparkProperties("Spark-App2","gcp.app.ReadFromBigQuery")
   # third_spark_job = getSparkJobHandle("Spark-App3","gcp.app.RunSparkSimple")

    first_spark_job.dag = dag
    first_spark_job.set_downstream(second_spark_job)
   # second_spark_job.set_downstream(third_spark_job)