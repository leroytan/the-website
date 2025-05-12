import boto3

# TODO: Replace with your Cloudflare R2 credentials
s3 = boto3.resource('s3',
  endpoint_url = 'https://<accountid>.r2.cloudflarestorage.com',
  aws_access_key_id = '<access_key_id>',
  aws_secret_access_key = '<access_key_secret>'
)

