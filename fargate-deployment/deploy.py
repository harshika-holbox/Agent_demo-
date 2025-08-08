#!/usr/bin/env python3
"""
CrewAI Document Intelligence Agent - ECS Fargate Deployment Script
Automates the complete deployment process to AWS ECS Fargate
"""

import subprocess
import sys
import os
import json
import time
import boto3
from datetime import datetime

def run_command(command, description, capture_output=True):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        if capture_output:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            return result.stdout.strip()
        else:
            subprocess.run(command, shell=True, check=True)
            return ""
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {description} failed")
        print(f"   Command: {command}")
        print(f"   Error: {e.stderr if e.stderr else e}")
        sys.exit(1)

def check_prerequisites():
    """Check if all required tools are installed"""
    print("🔍 Checking prerequisites...")
    
    tools = [
        ("aws", "AWS CLI"),
        ("docker", "Docker"),
        ("jq", "jq (JSON processor)")
    ]
    
    for tool, name in tools:
        try:
            subprocess.run([tool, "--version"], check=True, capture_output=True)
            print(f"✅ {name} is installed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"❌ {name} is not installed")
            print(f"   Please install {name} and try again")
            return False
    
    return True

def get_aws_info():
    """Get AWS account info and region"""
    print("🔍 Getting AWS information...")
    
    try:
        # Get account ID
        result = subprocess.run(["aws", "sts", "get-caller-identity"], 
                              check=True, capture_output=True, text=True)
        identity = json.loads(result.stdout)
        account_id = identity['Account']
        
        # Get region
        result = subprocess.run(["aws", "configure", "get", "region"], 
                              check=True, capture_output=True, text=True)
        region = result.stdout.strip()
        
        print(f"✅ Account ID: {account_id}")
        print(f"✅ Region: {region}")
        
        return account_id, region
        
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"❌ Error getting AWS info: {e}")
        print("   Please ensure AWS CLI is configured: aws configure")
        sys.exit(1)

def create_ecr_repository(account_id, region, repo_name="crewai-document-agent"):
    """Create ECR repository if it doesn't exist"""
    print(f"🐳 Creating ECR repository: {repo_name}...")
    
    try:
        # Check if repository exists
        subprocess.run([
            "aws", "ecr", "describe-repositories", 
            "--repository-names", repo_name,
            "--region", region
        ], check=True, capture_output=True)
        print(f"✅ ECR repository {repo_name} already exists")
        
    except subprocess.CalledProcessError:
        # Repository doesn't exist, create it
        run_command(f"""
            aws ecr create-repository \
                --repository-name {repo_name} \
                --region {region} \
                --image-scanning-configuration scanOnPush=true
        """, f"Creating ECR repository {repo_name}")
        print(f"✅ ECR repository {repo_name} created")
    
    return f"{account_id}.dkr.ecr.{region}.amazonaws.com/{repo_name}"

def build_and_push_image(ecr_uri, region):
    """Build Docker image and push to ECR"""
    print("🏗️ Building and pushing Docker image...")
    
    # Login to ECR
    print("🔐 Logging into ECR...")
    login_cmd = f"aws ecr get-login-password --region {region} | docker login --username AWS --password-stdin {ecr_uri.split('/')[0]}"
    run_command(login_cmd, "Logging into ECR", capture_output=False)
    
    # Build image
    print("🏗️ Building Docker image...")
    build_cmd = f"docker buildx build --platform linux/amd64 -t crewai-document-agent -f ../Dockerfile .."
    run_command(build_cmd, "Building Docker image", capture_output=False)
    
    # Tag image
    tag_cmd = f"docker tag crewai-document-agent:latest {ecr_uri}:latest"
    run_command(tag_cmd, "Tagging Docker image")
    
    # Push image
    print("📤 Pushing image to ECR...")
    push_cmd = f"docker push {ecr_uri}:latest"
    run_command(push_cmd, "Pushing Docker image to ECR", capture_output=False)
    
    print("✅ Docker image built and pushed successfully")
    return f"{ecr_uri}:latest"

def deploy_infrastructure(region, image_uri, stack_name="crewai-document-agent"):
    """Deploy CloudFormation stack"""
    print(f"🚀 Deploying infrastructure stack: {stack_name}...")
    
    # Deploy CloudFormation stack
    deploy_cmd = f"""
        aws cloudformation deploy \
            --template-file template.yaml \
            --stack-name {stack_name} \
            --parameter-overrides \
                Environment=prod \
                ImageURI={image_uri} \
            --capabilities CAPABILITY_NAMED_IAM \
            --region {region}
    """
    
    run_command(deploy_cmd, "Deploying CloudFormation stack", capture_output=False)
    
    # Wait for stack to be complete
    print("⏳ Waiting for stack deployment to complete...")
    wait_cmd = f"aws cloudformation wait stack-deploy-complete --stack-name {stack_name} --region {region}"
    run_command(wait_cmd, "Waiting for stack completion")
    
    print("✅ Infrastructure deployed successfully")

def get_outputs(stack_name, region):
    """Get CloudFormation stack outputs"""
    print("📄 Getting deployment outputs...")
    
    try:
        result = subprocess.run([
            "aws", "cloudformation", "describe-stacks",
            "--stack-name", stack_name,
            "--region", region
        ], check=True, capture_output=True, text=True)
        
        stack_info = json.loads(result.stdout)
        outputs = stack_info['Stacks'][0].get('Outputs', [])
        
        output_dict = {}
        for output in outputs:
            output_dict[output['OutputKey']] = output['OutputValue']
        
        return output_dict
        
    except Exception as e:
        print(f"⚠️ Warning: Could not get stack outputs: {e}")
        return {}

def test_endpoints(load_balancer_url):
    """Test the deployed endpoints"""
    print("🧪 Testing deployed endpoints...")
    
    import requests
    import time
    
    # Wait for load balancer to be ready
    print("⏳ Waiting for load balancer to be ready...")
    time.sleep(60)
    
    endpoints = [
        ("/health", "Health check"),
        ("/api/capabilities", "Capabilities"),
        ("/docs", "API documentation")
    ]
    
    for endpoint, description in endpoints:
        try:
            url = f"{load_balancer_url}{endpoint}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {description}: {url} - OK")
            else:
                print(f"⚠️ {description}: {url} - Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ {description}: {url} - Error: {e}")

def show_deployment_summary(outputs, stack_name):
    """Show deployment summary and next steps"""
    print("\n" + "="*80)
    print("🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!")
    print("="*80)
    
    print(f"\n📊 Deployment Summary:")
    print(f"   Stack Name: {stack_name}")
    print(f"   Deployment Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if outputs:
        print(f"\n🔗 Endpoints:")
        if 'LoadBalancerURL' in outputs:
            lb_url = outputs['LoadBalancerURL']
            print(f"   🌐 Web Interface: {lb_url}")
            print(f"   📚 API Docs: {lb_url}/docs")
            print(f"   ❤️ Health Check: {lb_url}/health")
            print(f"   🛠️ Capabilities: {lb_url}/api/capabilities")
        
        if 'ECSClusterName' in outputs:
            print(f"   🐳 ECS Cluster: {outputs['ECSClusterName']}")
        
        if 'S3BucketName' in outputs:
            print(f"   📦 S3 Bucket: {outputs['S3BucketName']}")
    
    print(f"\n🚀 AWS Marketplace Integration:")
    print(f"   📋 API Endpoint: {outputs.get('LoadBalancerURL', 'N/A')}/api/process")
    print(f"   📖 Documentation: {outputs.get('LoadBalancerURL', 'N/A')}/docs")
    print(f"   💰 Pricing Info: {outputs.get('LoadBalancerURL', 'N/A')}/api/pricing")
    
    print(f"\n📝 Request Format for AWS Marketplace:")
    print(f"""   POST {outputs.get('LoadBalancerURL', 'YOUR_ENDPOINT')}/api/process
   Content-Type: application/json
   {{
       "input_text": "Your document text here...",
       "user_query": "Summarize this document"
   }}""")
    
    print(f"\n🧪 Test Commands:")
    if outputs.get('LoadBalancerURL'):
        lb_url = outputs['LoadBalancerURL']
        print(f"""   # Health Check
   curl {lb_url}/health
   
   # Process Document
   curl -X POST {lb_url}/api/process \\
     -H "Content-Type: application/json" \\
     -d '{{"input_text": "Test document", "user_query": "Summarize"}}'
   
   # Upload File
   curl -X POST {lb_url}/api/upload \\
     -F "file=@your_document.pdf" \\
     -F "query=Summarize this document"
   """)
    
    print(f"\n📋 Next Steps for AWS Marketplace:")
    print(f"   1. Test all endpoints thoroughly")
    print(f"   2. Configure custom domain (optional)")
    print(f"   3. Set up monitoring and alerting") 
    print(f"   4. Submit to AWS Marketplace")
    print(f"   5. Update pricing and documentation")

def main():
    """Main deployment function"""
    print("CrewAI Document Intelligence Agent - ECS Fargate Deployment")
    print("="*70)

    account_id, region = get_aws_info()
    
    # # Configuration
    stack_name = "crewai-document-agent"
    repo_name = "crewai-document-agent"
    
    print(f"\n🔧 Deployment Configuration:")
    print(f"   Stack Name: {stack_name}")
    print(f"   ECR Repository: {repo_name}")
    print(f"   Region: {region}")
    print(f"   Account: {account_id}")
    
    try:
        # Step 1: Create ECR repository
        ecr_uri = create_ecr_repository(account_id, region, repo_name)
        
        # Step 2: Build and push Docker image
        image_uri = build_and_push_image(ecr_uri, region)
        # print(image_uri)
        # Step 3: Deploy infrastructure
        deploy_infrastructure(region, image_uri, stack_name)
        
        # Step 4: Get outputs
        outputs = get_outputs(stack_name, region)
        
        # Step 5: Test endpoints (optional)
        if outputs.get('LoadBalancerURL'):
            test_endpoints(outputs['LoadBalancerURL'])
        
        # Step 6: Show summary
        show_deployment_summary(outputs, stack_name)
        
    except KeyboardInterrupt:
        print("\n❌ Deployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
