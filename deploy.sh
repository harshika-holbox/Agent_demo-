#!/bin/bash

# Summarization Agent Deployment Script
# This script automates the deployment of the summarization agent to AWS

set -e

echo "Starting Summarization Agent Deployment..."

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check if SAM CLI is installed
if ! command -v sam &> /dev/null; then
    echo "AWS SAM CLI is not installed. Please install it first."
    exit 1
fi

# Check if user is authenticated
if ! aws sts get-caller-identity &> /dev/null; then
    echo "AWS credentials not configured. Please run 'aws configure' first."
    exit 1
fi

# Get AWS account ID and region
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=$(aws configure get region)

echo "📋 Deployment Configuration:"
echo "   Account ID: $ACCOUNT_ID"
echo "   Region: $REGION"

# Update agent config with actual values
echo "Updating agent configuration..."
sed -i "s/REGION/$REGION/g" agent-config.yaml
sed -i "s/ACCOUNT_ID/$ACCOUNT_ID/g" agent-config.yaml

# Build the application
echo "Building application..."
sam build

# Deploy the application
echo "Deploying to AWS..."
sam deploy --guided --parameter-overrides \
    Region=$REGION \
    AccountId=$ACCOUNT_ID

echo "Deployment completed successfully!"
echo ""
echo "Deployment Summary:"
echo "   - Lambda Function: summarizer_function"
echo "   - API Gateway: Created automatically"
echo "   - IAM Roles: Created with minimal permissions"
echo ""
echo "🔗 Next Steps:"
echo "   1. Test the API endpoint"
echo "   2. Submit to AWS Agent Marketplace"
echo "   3. Update documentation with actual endpoints"
echo ""
echo "To test the function:"
echo "   curl -X POST https://your-api-gateway-url/Prod/summarize \\"
echo "     -H \"Content-Type: application/json\" \\"
echo "     -d '{\"input\": \"Your text to summarize...\"}'" 