examples of connecting to HDFS or redis and migrating data to couchbase

# example env
this will use docker as an env for testing
SPARK v3.3.2
PYTHON v3.7.11
HADOOP v3.2.1
COUCHBASE v7.6.4
COUCHBASE-SPARK-CONNECTOR v3.5.2
REDIS vlatest
SPARK-REDIS-CONNECTOR v3.1.0


# create a docker network
docker network create hadoop-couchbase-network

# create Hadoop cluster
docker run -it --name hadoop-namenode --network hadoop-couchbase-network -p 9870:9870 -p 9000:9000 -e CORE_CONF_fs_defaultFS=hdfs://hadoop-namenode:9000 -e CORE_CONF_hadoop_http_staticuser_user=root -e CLUSTER_NAME="test-cluster" -e HDFS_CONF_dfs_replication=1 -v namenode-data:/hadoop/dfs/name bde2020/hadoop-namenode:latest

docker run -d --name hadoop-datanode --network hadoop-couchbase-network -e CORE_CONF_fs_defaultFS=hdfs://hadoop-namenode:9000 -e CORE_CONF_hadoop_http_staticuser_user=root -e HDFS_CONF_dfs_replication=1 -v datanode-data:/hadoop/dfs/data bde2020/hadoop-datanode:latest

this can be viewed at http://localhost:9870

# connect to the main hadoop container and set up an endpoint
docker exec -it hadoop-namenode bash

hdfs dfs -ls /
hdfs dfs -mkdir /user
hdfs dfs -mkdir /user/test
hdfs dfs -ls /user

# generate 1000 documents and place them in hadoop
create a new directory then run sample/sample.py
move the directory into the hadoop-namenode container
then:

docker exec -it hadoop-namenode bash

hdfs dfs -put /tmp/<whatever you named the dir> /user/test/

# create a couchbase cluster
docker run -d --name couchbase -p 8091-8096:8091-8096 -p 11210-11211:11210-11211 --network hadoop-couchbase-network couchbase

connect to the couchbase cluster through the browser using http://localhost:8091
username: Administrator
password: password

configure the cluster and create a bucket called "test"


# create a redis container:

docker run -d --name redis-stack --network hadoop-couchbase-network -p 6379:6379 -p 8001:8001 redis/redis-stack:latest

this can be viewed at http://localhost:8001

# create the spark image:
cd into pyspark/conn

docker build -t pyspark-migrator .  


# run the spark container
docker run --rm -it --name pyspark-migrator --network hadoop-couchbase-network  -v "$(pwd):/app" pyspark-migrator spark-submit --master local[2] --jars /opt/spark/jars/spark-connector-assembly-3.5.2.jar ./migrate_hdfs_to_couchbase.py

# result
1000 documents should be present in couchbase
view this in the UI

# create the spark-redis image
cd into pyspark/redis_conn_hash

docker build -t redis-migrator  . 

# run the spark-redis container
docker run --rm --name redis-migrator --network hadoop-couchbase-network redis-migrator spark-submit --jars /opt/spark/jars/spark-redis_2.12-3.1.0-jar-with-dependencies.jar,/opt/spark/jars/spark-connector-assembly-3.5.2.jar /app/redis_to_couchbase.py


# note
the basis for a spark-redis connector for data type string is in pyspark/redis_conn_string
it is not complete

