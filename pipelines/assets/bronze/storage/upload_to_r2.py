""" @bruin
name: bronze.storage.upload_to_r2
type: python
depends:
    - bronze.ingest.ingest_scm_kaggle
description: "Upload raw scm dataset from local storage to Cloudflare R2 (Bronze layer)."
@bruin """

import os
import boto3
from dotenv import load_dotenv
from pathlib import Path
import traceback
import requests
import datetime

# Load environment variables
load_dotenv()

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

def get_r2_client():
    """
    Create Cloudflare R2 client using boto3 (S3-compatible API).
    """
    try:
        return boto3.client(
            service_name = "s3",
            endpoint_url = f"https://{os.getenv('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com",
            aws_access_key_id = os.getenv("R2_ACCESS_KEY"),
            aws_secret_access_key = os.getenv("R2_SECRET_KEY"),
            region_name = "auto"
        )
    except Exception as e:
        error_detail = traceback.format_exc()
        send_discord_error(error_detail, task_name = "bronze/storage.upload_to_r2")
        raise e


def upload_to_r2():
    """
    Upload all files from local data directory to R2 Bronze layer.
    """
    
    s3 = get_r2_client()
    bucket_name = os.getenv("R2_BUCKET_NAME")

    # Define source and destination
    local_folder_path = os.getenv("RAW_DATA_PATH", "./data")
    r2_prefix = "bronze/car-scm"
    base_path = Path(local_folder_path)

    # Recursively upload files
    for file_path in base_path.rglob("*"):
        if file_path.is_file():
            relative_path = file_path.relative_to(base_path)

            # Ensure correct path format for R2
            r2_key = os.path.join(r2_prefix, str(relative_path)).replace("\\", "/")

            try:
                print(f"Uploading file: {relative_path} -> r2://{bucket_name}/{r2_key}")
                s3.upload_file(str(file_path), bucket_name, r2_key)

            except Exception as e:
                error_detail = traceback.format_exc()
                send_discord_error(error_detail, task_name = "bronze/storage.upload_to_r2")
                print(f"ERROR: Failed to upload {file_path}: {e}")
                
    complete_discord_notification(task_name = "bronze/storage.upload_to_r2")

if __name__ == "__main__":
    upload_to_r2()