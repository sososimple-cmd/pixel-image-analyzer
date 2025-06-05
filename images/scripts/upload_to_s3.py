import sys
import os
import boto3

file_name = sys.argv[1]
env = sys.argv[2]
bucket = os.getenv("S3_BUCKET")

# Prefix based on environment
s3_key = f"rekognition-input/{env}-{file_name}"

s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION"))
with open(f"images/{file_name}", 'rb') as f:
    s3.upload_fileobj(f, bucket, s3_key)

print(f"Uploaded {file_name} to {bucket}/{s3_key}")