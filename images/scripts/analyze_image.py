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
    try:
        response = rekognition.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': s3_key}},
            MaxLabels=10,
            MinConfidence=75
        )
        labels = [{'Name': label['Name'], 'Confidence': label['Confidence']} for label in response['Labels']]
        print("🔍 Labels detected:", labels)
    except Exception as e:
        print("❌ Rekognition label detection failed:", e)
        return

    timestamp = datetime.datetime.utcnow().isoformat()

    # Save to DynamoDB
    try:
        table_name = os.getenv("DYNAMODB_TABLE_BETA") if environment == 'beta' else os.getenv("DYNAMODB_TABLE_PROD")
        table = dynamodb.Table(table_name)
        item = {
            'image_name': file_name,
            'branch': environment,
            'labels': json.dumps(labels, indent=2),
            'timestamp': timestamp
        }
        table.put_item(Item=item)
        print(f"✅ Metadata logged to DynamoDB table '{table_name}':\n", json.dumps(item, indent=2))
    except Exception as e:
        print("❌ Failed to write to DynamoDB:", e)