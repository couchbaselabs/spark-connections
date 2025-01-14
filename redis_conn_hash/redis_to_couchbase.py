from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr


redis_host = "redis-stack"
redis_port = "6379"
key_pattern = "*"
bucket_name = "test"


spark = SparkSession.builder \
    .appName("Redis to Couchbase Migration") \
    .config("spark.redis.host", redis_host) \
    .config("spark.redis.port", redis_port) \
    .config("spark.couchbase.connectionString", "couchbase://couchbase") \
    .config("spark.couchbase.username", "Administrator") \
    .config("spark.couchbase.password", "password") \
    .config("com.couchbase.bucket." + bucket_name, "") \
    .getOrCreate()

table_name = "sample_session"


print("Loading data from Redis...")
try:

    redis_df = spark.read \
        .format("org.apache.spark.sql.redis") \
        .option("table", table_name) \
        .option("infer.schema", "true") \
        .load()

    print("Data loaded from Redis:")
    redis_df.show(truncate=False)


    redis_df = redis_df.withColumn("__META_ID", expr("uuid()"))

    print("Transformed data:")
    redis_df.show(truncate=False)

    print("Writing data to Couchbase...")

    redis_df.write \
        .format("couchbase.kv") \
        .option("bucket", bucket_name) \
        .option("idField", "__META_ID") \
        .mode("overwrite") \
        .save()

    print("Data successfully written to Couchbase.")

except Exception as e:
    print(f"An error occurred: {e}")

spark.stop()
