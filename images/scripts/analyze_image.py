import boto3
import os
import json
import datetime

# Setup AWS clients
rekognition = boto3.client('rekognition', region_name=os.getenv("AWS_REGION"))
s3 = boto3.client('s3', region_name=os.getenv("AWS_REGION"))
dynamodb = boto3.resource('dynamodb', region_name=os.getenv("AWS_REGION"))

def analyze_image(file_name, environment):
    # Upload to S3
    bucket = os.getenv("S3_BUCKET")
    s3_key = f"rekognition-input/{file_name}"
    print(f"Uploading {file_name} to S3 bucket '{bucket}' at key '{s3_key}'...")

    try:
        with open(f"images/{file_name}", 'rb') as image:
            s3.upload_fileobj(image, bucket, s3_key)
        print("✅ Upload successful!")
    except Exception as e:
        print("❌ Upload failed:", e)

    # Analyze using Rekognition
    response = rekognition.detect_labels(
        Image={'S3Object': {'Bucket': bucket, 'Name': s3_key}},
        MaxLabels=10,
        MinConfidence=75
    )

    labels = [{'Name': label['Name'], 'Confidence': label['Confidence']} for label in response['Labels']]
    timestamp = datetime.datetime.utcnow().isoformat()

    # Save to DynamoDB
    table_name = os.getenv("DYNAMODB_TABLE_BETA") if environment == 'beta' else os.getenv("DYNAMODB_TABLE_PROD")
    table = dynamodb.Table(table_name)
    table.put_item(Item={
        'image_name': file_name,
        'labels': json.dumps(labels),
        'timestamp': timestamp,
        'branch': environment
    })

if __name__ == "__main__":
    import sys
    file_name = sys.argv[1]
    environment = sys.argv[2]
    analyze_image(file_name, environment)
