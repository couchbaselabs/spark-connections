# from pyspark.sql import SparkSession
# from pyspark.sql.functions import col


# redis_host = "redis-stack"
# redis_port = "6379"
# bucket_name = "test"
# couchbase_host = "couchbase"
# couchbase_username = "Administrator"
# couchbase_password = "password"
# keys_pattern = "string:*"
#

# spark = SparkSession.builder \
#     .appName("Redis to Couchbase Migration") \
#     .config("spark.redis.host", redis_host) \
#     .config("spark.redis.port", redis_port) \
#     .config("spark.redis.persistence", "string") \
#     .config("spark.couchbase.connectionString", f"couchbase://{couchbase_host}") \
#     .config("spark.couchbase.username", couchbase_username) \
#     .config("spark.couchbase.password", couchbase_password) \
#     .config(f"com.couchbase.bucket.{bucket_name}", "") \
#     .getOrCreate()
#
# try:
#     print("Loading data from Redis...")


#     redis_df = spark.read \
#         .format("org.apache.spark.sql.redis") \
#         .option("keys.pattern", keys_pattern) \
#         .load()
#
#     print("Data loaded from Redis:")
#     redis_df.show(truncate=False)
#

#     redis_df = redis_df.withColumn("__META_ID", col("key"))
#
#     print("Transformed data:")
#     redis_df.show(truncate=False)
#
#     print("Writing data to Couchbase...")
#

#     redis_df.write \
#         .format("couchbase.kv") \
#         .option("bucket", bucket_name) \
#         .option("idField", "__META_ID") \
#         .mode("overwrite") \
#         .save()
#
#     print("Data successfully written to Couchbase.")
#
# except Exception as e:
#     print(f"An error occurred: {e}")
#
# finally:

#     spark.stop()


from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Redis to Couchbase Migration") \
    .config("spark.redis.host", "redis-stack") \
    .config("spark.redis.port", "6379") \
    .config("spark.redis.type", "string") \
    .getOrCreate()

try:
    print("Loading data from Redis...")
    # Read Redis string data
    redis_df = spark.read \
        .format("org.apache.spark.sql.redis") \
        .option("keys.pattern", "cars:*") \
        .option("table", "string") \
        .schema("key STRING, value STRING") \
        .load()

    # Show the loaded data
    print("Loaded data from Redis:")
    redis_df.show()

except Exception as e:
    print("An error occurred while loading data from Redis:")
    print(e)

# Stop Spark session
spark.stop()
