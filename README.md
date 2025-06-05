# Pixel Learning Co. Image Analyzer

## 🛠 AWS Resources
- S3 Bucket: `pixel-learning-images`
- Rekognition: enabled
- DynamoDB: `beta_results`, `prod_results`

## 🔒 GitHub Secrets
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_REGION
- S3_BUCKET
- DYNAMODB_TABLE_BETA
- DYNAMODB_TABLE_PROD

## 📂 How to Use
1. Add a .jpg/.png image to `images/`.
2. Commit via PR: result logs to `beta_results`.
3. Merge to main: logs to `prod_results`.

## ✅ Verifying
Go to your AWS DynamoDB console, check either `beta_results` or `prod_results` table for new entries.
## This is a Level up in Tech project!!
