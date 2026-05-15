""" @bruin
name: gold.load_to_motherduck
type: python
depends:
    - silver.data_normalization
description: "Upload and create table for dashboard."
@bruin """

import os
import duckdb
from dotenv import load_dotenv
import traceback
import requests
import datetime

# Load environment variables
load_dotenv()

R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY")
R2_ENDPOINT = f"{os.getenv('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com"
MOTHERDUCK_TOKEN = os.getenv("MOTHERDUCK_TOKEN")

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

def setup_connection():
    try:
        con = duckdb.connect(f"md:?motherduck_token={MOTHERDUCK_TOKEN}")
        con.execute("INSTALL httpfs; LOAD httpfs;")
        con.execute(f"""
            CREATE OR REPLACE SECRET r2_secret (
                TYPE S3,
                KEY_ID '{R2_ACCESS_KEY}',
                SECRET '{R2_SECRET_KEY}',
                ENDPOINT '{R2_ENDPOINT}',
                REGION 'auto',
                URL_STYLE 'path'
            );
        """)
        return con
    except Exception as e:
        error_detail = traceback.format_exc()
        send_discord_error(error_detail, task_name = "gold.load_to_motherduck")
        raise e

def create_tables(con):
    try:
        # Create database and load it to staging_raw table
        con.execute("CREATE DATABASE IF NOT EXISTS scm_db;")
        con.execute("USE scm_db;")
        con.execute("""
        CREATE OR REPLACE TABLE staging_raw AS
        SELECT * FROM read_parquet(
            's3://scm-car-dataset/silver/*.parquet'
            );
        """)
    except Exception as e:
        error_detail = traceback.format_exc()
        send_discord_error(error_detail, task_name = "gold.load_to_motherduck")
        raise e
    
def run_sql_file(con, filepath):
    with open(filepath, "r", encoding = "utf-8") as f:
        query = f.read()
    con.execute(query)
    
def main():
    con = setup_connection()
    try:
        create_tables(con)
        run_sql_file(con, "pipelines/assets/gold/queries/dim_customer.sql")
        run_sql_file(con, "pipelines/assets/gold/queries/dim_date.sql")
        run_sql_file(con, "pipelines/assets/gold/queries/dim_product.sql")
        run_sql_file(con, "pipelines/assets/gold/queries/dim_supplier.sql")
        run_sql_file(con, "pipelines/assets/gold/queries/fact_sale.sql")
    except Exception as e:
        error_detail = traceback.format_exc()
        send_discord_error(error_detail, task_name = "gold.load_to_motherduck")
        raise e
    complete_discord_notification(task_name = "gold.load_to_motherduck")
    con.close()
    
if __name__ == "__main__":
    main()