import os

import boto3
from dotenv import load_dotenv

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


def upload_file(local_path: str, bucket_name: str, remote_path: str):
    s3_client.upload_file(local_path, bucket_name, remote_path)


if __name__ == "__main__":
    upload_file()
