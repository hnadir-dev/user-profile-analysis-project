import findspark
findspark.init()

import logging


from pyspark import SparkConf

from cassandra.cluster import Cluster
# from cassandra.query import named_tuple_factory
# from pymongo import MongoClient

from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
SparkSession.builder.config(conf=SparkConf())

from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import from_json, col, lit, concat, when, hash, current_date, months_between, split


def create_keyspace(session):
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS kafka_spark_streams
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
    """)

    print("Keyspace created successfully!")

def create_user_profiles_table(session):
    session.execute("""
    CREATE TABLE IF NOT EXISTS kafka_spark_streams.user_profiles (
        id UUID PRIMARY KEY,
        full_name TEXT,
        gender TEXT,
        address TEXT,
        post_code TEXT,
        email TEXT,
        username TEXT,
        password TEXT,
        dob TEXT,
        age TEXT,
        registered_date TEXT,
        phone TEXT,
        picture TEXT,
        nat TEXT);
    """)

    print("Table created successfully!")

# Cassandra jar :  "com.datastax.spark:spark-cassandra-connector_2.13:3.4.1,"
# .config('spark.cassandra.connection.host', 'localhost') \
def create_spark_cassandra_mongodb_configuration():
    s_conn = None

    try:
        s_conn = SparkSession.builder \
            .appName("KafkaSparkIntegration") \
            .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.2.0,"
                    "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.4,"
                    "org.mongodb.spark:mongo-spark-connector_2.12:10.2.0") \
                    .config('spark.cassandra.connection.host', 'localhost') \
            .getOrCreate()
        
        logging.info("Spark connection created successfully!")
    except Exception as e:
        logging.error(f"Couldn't create the spark session due to exception {e}")

    return s_conn

def connect_to_kafka(spark_conn):
    spark_df = None
    try:
        spark_df = spark_conn.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("subscribe", "user_profiles") \
            .load()
        
        logging.info("kafka dataframe created successfully")
    except Exception as e:
        logging.warning(f"kafka dataframe could not be created because: {e}")

    return spark_df


def create_cassandra_connection():
    try:
        #=> connecting to the cassandra cluster
        cluster = Cluster(['localhost'], port=9042)

        cas_session = cluster.connect()

        return cas_session
    except Exception as e:
        logging.error(f"Could not create cassandra connection due to {e}")
        return None


def create_selection_df_from_kafka(spark_df):
    schema = StructType([
        StructField("id", StringType(), False),
        StructField("first_name", StringType(), False),
        StructField("last_name", StringType(), False),
        StructField("gender", StringType(), False),
        StructField("address", StringType(), False),
        StructField("post_code", StringType(), False),
        StructField("email", StringType(), False),
        StructField("username", StringType(), False),
        StructField("password", StringType(), False),
        StructField("dob", StringType(), False),
        StructField("registered_date", StringType(), False),
        StructField("phone", StringType(), False),
        StructField("picture", StringType(), False),
        StructField("nat", StringType(), False)
    ])

    sel = spark_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col('value'), schema).alias('data')).select("data.*") \
        .withColumn("full_name", concat(col('first_name'),lit(' '),col('last_name'))) \
        .withColumn('post_code',when(col("post_code").isNull(), lit('NoPostCode')).otherwise(col("post_code"))) \
        .withColumn('email',when(col("email").isNull(), lit('NoEmail')).otherwise(col("email"))) \
        .withColumn('dob',when(col("dob").isNull(), lit('NoDateOfB')).otherwise(col("dob"))) \
        .withColumn('age',(months_between(current_date(), col('dob')) / 12).cast('int')) \
        .withColumn('phone',when(col("phone").isNull(), lit('NoPhone')).otherwise(col("phone"))) \
        .withColumn('picture',when(col("picture").isNull(), lit('NoPicture')).otherwise(col("picture"))) \
        .withColumn('password',hash('password')) \
        .withColumn('nat',when(col("nat").isNull(), lit('NoNat')).otherwise(col("nat"))) \
        .select('id','full_name','gender','address','post_code','email','username','password','dob','age','registered_date','phone','picture','nat')

    return sel

def create_selection_df_from_mongodb(spark_df):
    schema = StructType([
        StructField("id", StringType(), False),
        StructField("first_name", StringType(), False),
        StructField("last_name", StringType(), False),
        StructField("gender", StringType(), False),
        StructField("address", StringType(), False),
        StructField("post_code", StringType(), False),
        StructField("email", StringType(), False),
        StructField("username", StringType(), False),
        StructField("password", StringType(), False),
        StructField("dob", StringType(), False),
        StructField("registered_date", StringType(), False),
        StructField("phone", StringType(), False),
        StructField("picture", StringType(), False),
        StructField("nat", StringType(), False)
    ])

    sel = spark_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col('value'), schema).alias('data')).select("data.*") \
        .withColumn("full_name", concat(col('first_name'),lit(' '),col('last_name'))) \
        .withColumn('post_code',when(col("post_code").isNull(), lit('NoPostCode')).otherwise(col("post_code"))) \
        .withColumn('email',when(col("email").isNull(), lit('NoEmail')).otherwise(col("email"))) \
        .withColumn('email_domain',split(col("email"),"@").getItem(1)) \
        .withColumn('dob',when(col("dob").isNull(), lit('NoDateOfB')).otherwise(col("dob"))) \
        .withColumn('age',(months_between(current_date(), col('dob')) / 12).cast('int')) \
        .withColumn('nat',when(col("nat").isNull(), lit('NoNat')).otherwise(col("nat"))) \
        .select('gender','email_domain','age','registered_date','nat')

    return sel
    

spark_connection = create_spark_cassandra_mongodb_configuration()
spark_df = connect_to_kafka(spark_connection)
session = create_cassandra_connection()


if spark_connection is not None:

     #=>Start creation keyspace if not exists
     create_keyspace(session)
     #=>Start creation table if not exists
     create_user_profiles_table(session)

     selection_kafka = create_selection_df_from_kafka(spark_df)
     selection_mongodb = create_selection_df_from_mongodb(spark_df)
     #=>
     #streaming_kafka_query = selection_mongodb.writeStream.outputMode("append").format("console").option("format", "json").start()

     #=>Streaming for save message in cassandra from producer
     streaming_kafka_query = (selection_kafka.writeStream.format("org.apache.spark.sql.cassandra")
                                   .option('checkpointLocation', '/tmp/checkpoint')
                                   .option('keyspace', 'kafka_spark_streams')
                                   .option('table', 'user_profiles')
                                   .start())

     streaming_mongo_query = (selection_mongodb.writeStream
                                   .format("mongodb")
                                   .option("checkpointLocation", "/tmp/pyspark/")
                                   .option("spark.mongodb.connection.uri", 'mongodb://localhost:27023')
                                   .option("spark.mongodb.database", 'user_db')
                                   .option("spark.mongodb.collection", 'user_profiles')
                                   .outputMode("append").start())
     
     streaming_kafka_query.awaitTermination()
     streaming_mongo_query.awaitTermination()
