""" @bruin
name: bronze.ingest.ingest_scm_kaggle
type: python
description: "Retrieve dataset from Kaggle and store it in a specified local directory (Bronze Layer)."
@bruin """

# Import necessary libraries
import os
import shutil
import traceback
from dotenv import load_dotenv
import kagglehub
import requests
import datetime

# Load the environment variables
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

def load_env():
    """
    Load environment variables from .env file and validate required keys.
    """
    required_vars = ["KAGGLE_USERNAME", "KAGGLE_KEY"]
    for var in required_vars:
        if not os.getenv(var):
            send_discord_error(f"Missing environment variable: {var}", task_name = "bronze/ingest.ingest_scm_kaggle")
            raise ValueError(f"Missing environment variable: {var}")


def download_scm_dataset(target_dir: str) -> str:
    """
    Download Car SCM dataset from Kaggle and move it to a target directory.
    """

    # Ensure target directory exists
    os.makedirs(target_dir, exist_ok = True)

    # Idempotent check: skip if data already exists
    if os.listdir(target_dir):
        print(f"Dataset already exists at: {target_dir}")
        return target_dir

    # Download dataset to kagglehub cache
    try:
        cache_path = kagglehub.dataset_download("prashantk93/supply-chain-management-for-car")
    except Exception as e:
        error_detail = traceback.format_exc()
        send_discord_error(error_detail, task_name = "bronze/ingest.ingest_scm_kaggle")
        raise e
    
    # Move files from cache to target directory
    for file_name in os.listdir(cache_path):
        src = os.path.join(cache_path, file_name)
        dst = os.path.join(target_dir, file_name)

        if os.path.isfile(src):
            shutil.move(src, dst)
    
    return target_dir


def list_files(data_path: str):
    """
    List all files in the dataset directory.

    Args:
        data_path (str): Path to dataset folder
    """
    print("\nFiles in dataset:")

    for root, _, files in os.walk(data_path):
        for file in files:
            print(f"- {os.path.join(root, file)}")


def run():
    """
    Main pipeline execution function.
    """

    # Load environment variables
    load_env()

    # Set target directory
    target_dir = os.getenv(
        "RAW_DATA_PATH",
        "/workspaces/scm-data-pipeline-v2/data"
    )

    # Download and store dataset
    try:
        data_path = download_scm_dataset(target_dir)
    except Exception as e:
        error_detail = traceback.format_exc()
        send_discord_error(error_detail, task_name = "bronze/ingest.ingest_scm_kaggle")
        raise e
        
    # List files for verification
    list_files(data_path)
    complete_discord_notification(task_name = "bronze/ingest.ingest_scm_kaggle")


if __name__ == "__main__":
    run()