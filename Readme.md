/gcpscala
├── cliscripts/
├── datproc-templates/
├── src/
│   ├── main/resources

PreReqs: 
1) Install Gcloud on your Mac as the scripts will run from your PC
2) Run 'gcloud auth login to Authenticate to GCP 
3) Select the data-cn-landd project id -- gcloud config set project data-cn-landd
4) Ensure jar files are available in gs://kpi01-jars or create your own bucket and put jars in there
5) Ensure the Dataset you want to Query is available in the BigQuery
 
TODO: The assembly command does not include the bigquery jar so we are having to pass it to the Dataproc job manually

How to Run
In order to create an ephemeral cluster run the following command
source dataproc-templates/managed_cluster.sh -- The Scala code for this is in app/ReadFromBigQuery.scala