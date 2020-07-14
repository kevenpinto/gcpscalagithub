#!/bin/bash

# Set Variables
project_id=data-cn-landd
workflow_template_name=kpi01-select-cluster-template  # Name for Your Template
dataproc_cluster_name=kpi01-scalateststatic
class_file=gcp.app.ReadFromBigQuery
jar_files=gs://kpi01-jars/gcpscala-0.1.jar
bigquery_jar_file=gs://spark-lib/bigquery/spark-bigquery-latest.jar # Do not Modify

# Hadoop Cluster Specific Params -Leave these as Set to these defaults for now
region=europe-west2
zone=europe-west2-a
machine_type=n1-standard-4
num_workers=4
image_version=1.4.29-debian9
spark_properties="spark.driver.extraJavaOptions=""-Dbigquery.src_table1=${project_id}.scalatesting.cars
-Dbigquery.src_table2=${project_id}.scalatesting.guitars""
,spark.dynamicAllocation.enabled=true"


# Delete the template and recreate if one already exists
template_exists=$(gcloud dataproc workflow-templates list | grep $workflow_template_name| wc -l)
if [ $template_exists -gt 0 ]
then
  echo "Deleting Template $workflow_template_name"
  gcloud dataproc workflow-templates delete -q $workflow_template_name
fi

# Create a WorkFlow Template Resource
# https://cloud.google.com/dataproc/docs/concepts/workflows/using-workflows#adding_jobs_to_a_template
echo "Creating Template $workflow_template_name"
gcloud dataproc workflow-templates create --region $region $workflow_template_name

# Attach Template to an existing Cluster
echo "Setting Managed Cluster $dataproc_cluster_name for $workflow_template_name"
gcloud dataproc workflow-templates set-cluster-selector $workflow_template_name \
--region $region \
--cluster-labels goog-dataproc-cluster-name=$dataproc_cluster_name

# Attach a Spark Job to the Template
echo "Attaching Spark Job to $dataproc_cluster_name"
gcloud dataproc workflow-templates add-job spark \
--step-id kpi01-spark-job-step1 \
--workflow-template $workflow_template_name \
--class=$class_file  \
--jars=$jar_files,$bigquery_jar_file \
--properties=$spark_properties

# Instantiate(Run) the Workflow template
echo "Running Spark Job On $dataproc_cluster_name"
gcloud dataproc workflow-templates instantiate $workflow_template_name
