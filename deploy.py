#!/usr/bin/env python3
"""
Document Intelligence Agent Deployment Script
This script automates the deployment of the document intelligence agent to AWS
"""

import subprocess
import sys
import os
import json
import re

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"{description} completed successfully")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {description} failed")
        print(f"   Command: {command}")
        print(f"   Error: {e.stderr}")
        sys.exit(1)

def check_aws_cli():
    """Check if AWS CLI is installed"""
    print("Checking AWS CLI installation...")
    try:
        subprocess.run(["aws", "--version"], check=True, capture_output=True)
        print("AWS CLI is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("AWS CLI is not installed. Please install it first.")
        print("   Visit: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html")
        return False

def check_sam_cli():
    """Check if SAM CLI is installed"""
    print("Checking AWS SAM CLI installation...")
    try:
        subprocess.run(["sam", "--version"], check=True, capture_output=True)
        print("AWS SAM CLI is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("AWS SAM CLI is not installed. Please install it first.")
        print("   Visit: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html")
        return False

def check_aws_credentials():
    """Check if AWS credentials are configured"""
    print("Checking AWS credentials...")
    try:
        result = subprocess.run(["aws", "sts", "get-caller-identity"], 
                              check=True, capture_output=True, text=True)
        identity = json.loads(result.stdout)
        print(f"AWS credentials configured")
        print(f"   Account ID: {identity['Account']}")
        print(f"   User ARN: {identity['Arn']}")
        return identity['Account']
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        print("AWS credentials not configured. Please run 'aws configure' first.")
        return None

def get_aws_region():
    """Get the configured AWS region"""
    try:
        result = subprocess.run(["aws", "configure", "get", "region"], 
                              check=True, capture_output=True, text=True)
        region = result.stdout.strip()
        print(f"   Region: {region}")
        return region
    except subprocess.CalledProcessError:
        print("AWS region not configured. Please run 'aws configure' first.")
        return None

def update_agent_config(account_id, region):
    """Update agent-config.yaml with actual AWS values"""
    print("Updating agent configuration...")
    
    config_file = "agent-config.yaml"
    if not os.path.exists(config_file):
        print(f"{config_file} not found")
        return False
    
    try:
        with open(config_file, 'r') as f:
            content = f.read()
        
        # Replace placeholders with actual values
        content = content.replace("REGION", region)
        content = content.replace("ACCOUNT_ID", account_id)
        
        with open(config_file, 'w') as f:
            f.write(content)
        
        print("Agent configuration updated")
        return True
    except Exception as e:
        print(f"Error updating configuration: {e}")
        return False

def build_application():
    """Build the SAM application"""
    print("🏗️ Building application...")
    run_command("sam build", "Building SAM application")

def deploy_application(region, account_id):
    """Deploy the application to AWS"""
    print("Deploying to AWS...")
    
    # Run SAM deploy with guided mode
    deploy_command = f"sam deploy --guided --parameter-overrides Region={region} AccountId={account_id}"
    run_command(deploy_command, "Deploying to AWS")

def show_deployment_summary():
    """Show deployment summary and next steps"""
    print("\n" + "="*60)
    print("🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!")
    print("="*60)
    
            print("\nDeployment Summary:")
    print("   - Lambda Function: document_intelligence_function")
    print("   - API Gateway: Created automatically")
    print("   - IAM Roles: Created with minimal permissions")
    
    print("\n🔗 Next Steps:")
    print("   1. Test the API endpoint")
    print("   2. Submit to AWS Agent Marketplace")
    print("   3. Update documentation with actual endpoints")
    
    print("\n🧪 To test the function:")
    print("   curl -X POST https://your-api-gateway-url/Prod/process \\")
    print("     -H \"Content-Type: application/json\" \\")
    print("     -d '{\"input\": \"Your document text...\", \"user_query\": \"Summarize this document\"}'")
    
    print("\n📚 For more information:")
    print("   - AWS Agent Marketplace: https://aws.amazon.com/agent-marketplace/")
    print("   - SAM Documentation: https://docs.aws.amazon.com/serverless-application-model/")

def main():
    """Main deployment function"""
    print("Document Intelligence Agent Deployment")
    print("="*50)
    
    # Check prerequisites
    if not check_aws_cli():
        sys.exit(1)
    
    if not check_sam_cli():
        sys.exit(1)
    
    account_id = check_aws_credentials()
    if not account_id:
        sys.exit(1)
    
    region = get_aws_region()
    if not region:
        sys.exit(1)
    
            print(f"\nDeployment Configuration:")
    print(f"   Account ID: {account_id}")
    print(f"   Region: {region}")
    
    # Update configuration
    if not update_agent_config(account_id, region):
        sys.exit(1)
    
    # Build and deploy
    build_application()
    deploy_application(region, account_id)
    
    # Show summary
    show_deployment_summary()

if __name__ == "__main__":
    main() 