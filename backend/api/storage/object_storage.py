import boto3

from api.config import settings

# Create an S3 client with R2 config
s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.r2_access_key_id,
    aws_secret_access_key=settings.r2_secret_key,
    endpoint_url=settings.r2_endpoint,
    region_name=settings.r2_bucket_region,  # R2 doesn't care about region; use "auto" or any string
)
