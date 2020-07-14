#!/bin/bash

project_id=data-cn-landd
declare -a table_array

table_array=(-Dbigquery.src_table=${project_id}.scalatesting.cars
-Dbigquery.src_table=${project_id}.scalatesting.guitars)

tables="spark.driver.extraJavaOptions="
for table in "${table_array[*]}";do  tables="$tables$table "; done
