""" @bruin
name: silver.data_normalization
type: python
depends:
    - bronze.storage.upload_to_r2
description: "Read data from R2 Bronze, clean & normalize in Spark, map payment types, and save to Silver/Gold"
@bruin """

import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, trim, lit, create_map, coalesce
from dotenv import load_dotenv
from itertools import chain
import traceback
import requests
import datetime

# Load environment variables
load_dotenv()

# R2 config
ACCESS_KEY = os.getenv('R2_ACCESS_KEY')
SECRET_KEY = os.getenv('R2_SECRET_KEY')
ENDPOINT = f"https://{os.getenv('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com"
BUCKET = os.getenv('R2_BUCKET_NAME')

def send_discord_error(error_message, task_name = "Car SCM Pipeline"):
    webhook_url = os.getenv("DISCORD_WEBHOOK")
    
    payload = {
        "username": "Error Bot",
        "embeds": [
            {
                "title": f"ERROR: {task_name}",
                "description": f"```python\n{error_message}\n```",
                "color": 15158332,  # Red
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
        ]
    }
    
    try:
        response = requests.post(webhook_url, json = payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Cannot send the message to Discord: {e}")

def complete_discord_notification(task_name = "Car SCM Pipeline"):
    webhook_url = os.getenv("DISCORD_WEBHOOK")
    
    payload = {
        "username": "Notification Bot",
        "embeds": [
            {
                "title": f"{task_name}",
                "description": f"Completed",
                "color": 3066993,  # Green
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
        ]
    }
    
    try:
        response = requests.post(webhook_url, json = payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Cannot send the message to Discord: {e}")

# Spark Session
def create_spark_session():
    try:
        return (SparkSession.builder
            .appName("Car_SCM_Bronze_to_Silver")
            .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.4.2")
            .config("spark.hadoop.fs.s3a.endpoint", ENDPOINT)
            .config("spark.hadoop.fs.s3a.access.key", ACCESS_KEY)
            .config("spark.hadoop.fs.s3a.secret.key", SECRET_KEY)
            .config("spark.hadoop.fs.s3a.path.style.access", "true")
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
            .config("spark.hadoop.fs.s3a.connection.timeout", "60000")
            .config("spark.hadoop.fs.s3a.connection.establish.timeout", "5000")
            .config("spark.hadoop.fs.s3a.socket.timeout", "60000")
            .config("spark.hadoop.fs.s3a.endpoint.region", "auto")
            .config("spark.hadoop.fs.s3a.multiregion.access.point.disable", "true")
            .getOrCreate())
    except Exception as e:
        error_detail = traceback.format_exc()
        send_discord_error(error_detail, task_name = "silver.data_normalization")
        raise e

# Main processing
def process_data():
    try: 
        spark = create_spark_session()
        df = spark.read.option("header", True).option("inferSchema", True) \
        .csv("s3a://scm-car-dataset/bronze/car-scm/Car_SupplyChainManagementDataSet.csv")
        
        mapping = {
            'visa': 'visa',
            'visa-electron': 'visa',
            'mastercard': 'mastercard',
            'maestro': 'mastercard',
            'americanexpress': 'amex',
            'china-unionpay': 'unionpay',
            'diners-club-carte-blanche': 'diners',
            'diners-club-enroute': 'diners',
            'diners-club-us-ca': 'diners',
            'diners-club-international': 'diners',
            'jcb': 'jcb',
            'solo': 'solo',
            'switch': 'switvh',
            'laser': 'laser',
            'bankcard': 'bankcard',
            'instapayment': 'instapayment'
        }

        mapping_expr = create_map([lit(x) for x in chain(*mapping.items())])

        df = df.withColumn(
            "CreditCardType",
            coalesce(mapping_expr[col("CreditCardType")], col("CreditCardType"))
        )
        
        mapping2 = {
            "Fuscia": "Fuchsia",
            "Mauv": "Mauve"
        }
        
        mapping_expr2 = create_map([lit(x) for x in chain(*mapping2.items())])
    except Exception as e:
        error_detail = traceback.format_exc()
        send_discord_error(error_detail, task_name = "silver.data_normalization")
        raise e

    df = df.withColumn(
        "CarColor",
        coalesce(mapping_expr2[col("CarColor")], col("CarColor"))
    )
    
    # Write Output

    silver_path = f"s3a://{BUCKET}/silver/"
    df.write.mode("overwrite").parquet(silver_path)

    spark.stop()
    
    complete_discord_notification(task_name = "silver.data_normalization")


if __name__ == "__main__":
    process_data()