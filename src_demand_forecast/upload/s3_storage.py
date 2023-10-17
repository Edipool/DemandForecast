import os
import boto3
import logging
import sys
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

def upload_dataset(
    local_path: str,
    s3_bucket: str,
    remote_path: str,
    file_names: list = None
):
    if file_names is None:
        # If file_names is None, upload all files in the local_path
        file_names = [f for f in os.listdir(local_path) if os.path.isfile(os.path.join(local_path, f))]

    for file_name in file_names:
        local_file_path = os.path.join(local_path, file_name)
        remote_file_path = os.path.join(remote_path, file_name)

        s3_client.upload_file(local_file_path, s3_bucket, remote_file_path)

        logger.info(f"local_file_path: {local_file_path}")
        logger.info(f"remote_path: {remote_file_path}")

if __name__ == "__main__":
    upload_dataset()
