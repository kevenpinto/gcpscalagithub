# create the Initial Buckets
# Store the Jars here
gsutil mb -l europe-west2 -c standard -p data-cn-landd gs://kpi01-jars
# Store the data here
gsutil mb -l europe-west2 -c standard -p data-cn-landd gs://kpi01-data

#

bq --location=europe-west2 mk \
--dataset \
--description "Creating a Dataset to store data and get Scala/Spark  to Query it" \
data-cn-landd:scalatesting

