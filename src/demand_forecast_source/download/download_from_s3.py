import os
import boto3
import logging
import sys
import click
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

session = boto3.session.Session()
s3_client = session.client(
    service_name="s3",
    region_name="ru-msk",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    endpoint_url="https://storage.yandexcloud.net",
)

def download_dataset(
    s3_bucket: str,
    remote_path: str,
    output_path: str,
    file_names: list = None
):
    if file_names is None:
        file_names = ["demand_orders.csv", "demand_orders_status.csv"]

    os.makedirs(output_path, exist_ok=True)

    for file_name in file_names:
        remote_file_path = f"{remote_path}/{file_name}"
        output_local_path = f"{output_path}/{file_name}"

        s3_client.download_file(s3_bucket, remote_file_path, output_local_path)

        logger.info(f"remote_path: {remote_file_path}")
        logger.info(f"output_local_path: {output_local_path}")


if __name__ == "__main__":
    download_dataset()
