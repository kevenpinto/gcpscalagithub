#!/bin/bash

# Set Variables
location=europe-west2
zone=europe-west2-a
project_id=data-cn-landd
machine=n1-standard-2
diskGB=20GB
python_version=3
node_count=2


gcloud composer environments create demo-ephemeral-dataproc \
--project $project_id \
--location $location \
--zone $zone \
--machine-type  $machine \
--node-count $node_count \
--disk-size $diskGB \
--python-version $python_version


