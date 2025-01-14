from pyspark.sql import SparkSession
from pyspark.sql import functions as F


spark = SparkSession.builder \
    .appName("HDFS to Couchbase Migration") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://hadoop-namenode:9000") \
    .config("spark.couchbase.connectionString", "couchbase://couchbase") \
    .config("spark.couchbase.username", "Administrator") \
    .config("spark.couchbase.password", "password") \
    .config("com.couchbase.bucket.test", "") \
    .getOrCreate()


bucket_name = "test"


def process_json_file(file_path, multiline=False):
    print(f"Processing JSON file: {file_path}")
    try:
        schema = spark.read.option("multiline", multiline).json(file_path).schema
        json_df = spark.read.schema(schema).option("multiline", multiline).json(file_path)
        json_df = json_df.withColumn("id", F.expr("uuid()"))
        json_df = json_df.withColumn("__META_ID", F.expr("uuid()"))
        json_df.write \
            .format("couchbase.kv") \
            .option("bucket", bucket_name) \
            .option("batchSize", 500) \
            .save()
        print(f"Inserted JSON data into Couchbase.")
    except Exception as e:
        print(f"Error processing JSON file {file_path}: {e}")


hdfs_dir = "hdfs://hadoop-namenode:9000/user/test/data"
try:
    files = [row.path for row in spark.read.format("binaryFile").load(hdfs_dir).select("path").collect()]
except Exception as e:
    print(f"Error listing files in HDFS: {e}")
    files = []


for file_path in files:
    print(f"Processing file: {file_path}")
    try:
        process_json_file(file_path)
    except Exception as e:
        print(f"Error processing JSON: {e}")


print("Data migration completed!")
