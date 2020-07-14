from datetime import datetime, timedelta
from airflow import DAG
from airflow.contrib.operators.dataproc_operator import DataprocClusterCreateOperator, \
    DataProcPySparkOperator, DataprocClusterDeleteOperator, DataProcSparkOperator
from airflow.utils.trigger_rule import TriggerRule

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
with DAG('Run-Some-Scala',
         default_args=DEFAULT_DAG_ARGS,
         schedule_interval=None) as dag:  # Here we are using dag as context.
    # Create the Cloud Dataproc cluster.
    # Note: this operator will be flagged a success if the cluster by this name already exists.
    create_cluster = DataprocClusterCreateOperator(
        task_id='create_dataproc_cluster',
        # ds_nodash is an airflow macro for "[Execution] Date string no dashes"
        # in YYYYMMDD format. See docs https://airflow.apache.org/code.html?highlight=macros#macros
        cluster_name='ephemeral-spark-cluster-{{ ds_nodash }}',
        image_version='1.5-debian10',
        num_workers=2,
        storage_bucket=CLUSTER_STORAGE_BUCKET,
        region=REGION,
        zone=ZONE
    )

    # Submit our Spark Job
    submit_scalaspark = DataProcSparkOperator(
        task_id=TASK_ID,
        region=REGION,
        main_class=MAIN_CLASS,
        cluster_name='ephemeral-spark-cluster-{{ ds_nodash }}',
        dataproc_spark_jars=MAIN_JAR
    )

    # Delete the Cloud Dataproc cluster.
    delete_cluster = DataprocClusterDeleteOperator(
        task_id='delete_dataproc_cluster',
        region=REGION,
        # Obviously needs to match the name of cluster created in the prior two Operators.
        cluster_name='ephemeral-spark-cluster-{{ ds_nodash }}',
        # This will tear down the cluster even if there are failures in upstream tasks.
        trigger_rule=TriggerRule.ALL_DONE)

    create_cluster.dag = dag

    create_cluster.set_downstream(submit_scalaspark)

    submit_scalaspark.set_downstream(delete_cluster)
