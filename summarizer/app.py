import boto3
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def lambda_handler(event, context):
    """
    Lambda function for text summarization using Amazon Bedrock
    """
    try:
        # Extract input from the event
        input_text = event.get("input", "")
        
        if not input_text:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No input text provided"})
            }

        # Configure AWS credentials from environment variables
        aws_config = {}
        
        # Check for AWS credentials in environment variables
        if os.getenv('AWS_ACCESS_KEY_ID') and os.getenv('AWS_SECRET_ACCESS_KEY'):
            aws_config.update({
                'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
                'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
                'region_name': os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
            })
            
            # Add session token if available
            if os.getenv('AWS_SESSION_TOKEN'):
                aws_config['aws_session_token'] = os.getenv('AWS_SESSION_TOKEN')
        
        # Initialize Bedrock client with credentials
        bedrock = boto3.client("bedrock-runtime", **aws_config)
        
        # Get model ID from environment or use default
        model_id = os.getenv('BEDROCK_MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0')
        
        # Use the correct format for Claude 3 in Bedrock
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 300,
            "messages": [
                {
                    "role": "user",
                    "content": f"Please provide a concise summary of the following text. Focus on the main points and key information:\n\n{input_text}"
                }
            ]
        }
        
        # Invoke the Bedrock model
        response = bedrock.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body),
            contentType="application/json",
            accept="application/json"
        )

        # Parse the response
        result = json.loads(response['body'].read())
        
        # Extract content from the response
        if 'content' in result and len(result['content']) > 0:
            summary = result['content'][0].get('text', 'No summary generated')
        else:
            summary = "No summary generated"
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "summary": summary.strip(),
                "input_length": len(input_text),
                "summary_length": len(summary)
            })
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Error processing request: {str(e)}"})
        }
