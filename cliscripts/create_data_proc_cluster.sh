dataproc_cluster_name=kpi01-scalateststatic

# Hadoop Cluster Specific Params -Leave these as Set to these defaults for now
region=europe-west2
zone=europe-west2-a
machine_type=n1-standard-4
num_workers=2
image_version=1.4.29-debian9

gcloud dataproc clusters create $dataproc_cluster_name --region $region --zone $zone \
--master-machine-type $machine_type --master-boot-disk-size 50 \
--num-workers $num_workers --worker-machine-type $machine_type --worker-boot-disk-size 50 \
--image-version $image_version