from os import environ
import boto3
from botocore.exceptions import NoCredentialsError
import uuid
import sys


def upload_to_cloud(file):
    AWS_ACCESS_KEY_ID = environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = environ.get("AWS_SECRET_ACCESS_KEY")

    s3_resource = boto3.resource(
        "s3", aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    bucket = s3_resource.Bucket("learngram-videos")
    key = f"{uuid.uuid4().hex}{file.filename}"
    bucket.Object(key).put(Body=file.read())
    return key
