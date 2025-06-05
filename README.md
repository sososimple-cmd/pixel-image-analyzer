# 📸 Pixel Learning Co. - Automated Image Classification with AWS Rekognition

This project simulates a workflow for a fictional company, **Pixel Learning Co.**, where images uploaded to an S3 bucket are automatically classified using **AWS Rekognition**. The classification results are stored in **DynamoDB**, with metadata tracked using a **Lambda function**. A **GitHub Actions** CI/CD pipeline deploys infrastructure and code.

---

## 🚀 Project Features

- Upload an image to S3 → triggers Lambda
- Lambda classifies image using AWS Rekognition
- Results logged into a corresponding DynamoDB table
- GitHub Actions automates the deployment

---

## 🛠️ AWS Resources Setup

### 1. ✅ S3 Bucket
Create an S3 bucket for image uploads:

![Screenshot 2025-06-05 115611](https://github.com/user-attachments/assets/73526337-a73a-4078-a0e1-999e34cf14c3)


aws s3api create-bucket --bucket pixel-image-uploads --region us-east-1
Enable event notification for new object creation to trigger Lambda:

Go to S3 > your bucket > Properties > Event notifications > Add event.

Name it TriggerLambda, event type: PUT, destination: your Lambda function.
![Screenshot 2025-06-05 134143](https://github.com/user-attachments/assets/f94e1f40-938a-4d31-aaf6-bfe30a39f2e6)

## 2. 🔍 AWS Rekognition
No setup needed — Rekognition is ready to use out of the box. The Lambda function will use the detect_labels API.

Make sure your IAM role has this permission:
```bash
"rekognition:DetectLabels"
```

## 3. 🗃️ DynamoDB Tables
You need two DynamoDB tables (or just one depending on your structure).

Create via AWS CLI or Console:

```bash
aws dynamodb create-table \
  --table-name ImageMetadata \
  --attribute-definitions AttributeName=imageKey,AttributeType=S \
  --key-schema AttributeName=imageKey,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```

🔐 GitHub Secrets Configuration
In your GitHub repo, go to Settings > Secrets and variables > Actions and add the following:

```bash
| Secret Name             | Description                                   |
| ----------------------- | --------------------------------------------- |
| `AWS_ACCESS_KEY_ID`     | Your AWS access key with deploy permissions   |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret key                           |
| `AWS_REGION`            | Region of your AWS services (e.g., us-east-1) |
```

## 4. 🔁 Adding & Analyzing New Images
Go to your S3 bucket.

Click “Upload,” and upload any .jpg or .png image.

Once uploaded:

Lambda will trigger automatically.

Rekognition will analyze the image.

Metadata will be logged to DynamoDB

🧠 Example DynamoDB Record
```bash
{
  "imageKey": "beta_dogs.jpg",
  "labels": ["Dog", "Pet", "Animal"],
  "bucketName": "pixel-image-uploads",
  "timestamp": "2025-06-05T13:42:00Z"
}
```

🧪 Testing Locally
You can test the Lambda using the AWS Console by simulating a test event.

Use an S3 ObjectCreated:Put event as the sample.

Once everything is set up, you’ll have a fully automated image classification pipeline running in the cloud — no manual steps, no guessing. Just upload an image and let AWS handle the rest. This project is a great starting point for anyone looking to learn cloud automation, serverless architecture, or how to integrate security workflows into real-world scenarios.
