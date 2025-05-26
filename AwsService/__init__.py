import os
import boto3
import boto3.resources


from dotenv import load_dotenv

load_dotenv()

# Specify the bucket name you wish to create
s3 = boto3.resource(
    service_name=os.getenv("SERVICE_NAME"),
    region_name=os.getenv("REGION_NAME"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv(
        "AWS_SECRET_ACCESS_KEY"
    ),  # replace with your actual AWS credentials
)

BUCKET_NAME = os.getenv("BUCKET_NAME")
s3_client = s3.meta.client  # Get the S3 client from the resource
