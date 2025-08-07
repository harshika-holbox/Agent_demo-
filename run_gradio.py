#!/usr/bin/env python3
"""
Launcher script for the AWS Agent Core Document Intelligence Agent Gradio interface
"""

import os
import sys
import boto3
from dotenv import load_dotenv

# Add the document_intelligence directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'document_intelligence'))

# Load environment variables
load_dotenv()

def check_aws_credentials():
    """Check if AWS credentials are configured using boto3"""
    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        
        if credentials is None:
            print("Warning: No AWS credentials found!")
            print("Please configure your AWS credentials using one of these methods:")
            print("1. AWS CLI: aws configure")
            print("2. Environment variables:")
            print("   export AWS_ACCESS_KEY_ID=your_access_key")
            print("   export AWS_SECRET_ACCESS_KEY=your_secret_key")
            print("   export AWS_DEFAULT_REGION=your_region")
            print("3. IAM roles (if running on EC2)")
            print("4. AWS credentials file (~/.aws/credentials)")
            print()
            response = input("Do you want to continue anyway? (y/n): ")
            if response.lower() != 'y':
                sys.exit(1)
        else:
            frozen_credentials = credentials.get_frozen_credentials()
            print(f"AWS credentials found!")
            print(f"Access Key: {frozen_credentials.access_key[:8]}...")
            print(f"Region: {session.region_name or 'Not set'}")
            
    except Exception as e:
        print(f"Error checking AWS credentials: {e}")
        print("Please ensure AWS credentials are properly configured.")
        response = input("Do you want to continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)

def main():
    """Main function to launch the Gradio interface"""
    print("=" * 60)
    print("AWS Agent Core - Document Intelligence Agent")
    print("Gradio Web Interface")
    print("=" * 60)
    
    # Check AWS credentials
    check_aws_credentials()
    
    print("\nStarting Gradio interface...")
    print("The web interface will be available at: http://localhost:7860")
    print("Press Ctrl+C to stop the server")
    print("-" * 60)
    
    try:
        # Import and run the Gradio interface
        from document_intelligence.app import create_gradio_interface
        
        iface = create_gradio_interface()
        iface.launch(
            share=False,
            server_name="0.0.0.0",
            server_port=7860,
            show_error=True
        )
        
    except ImportError as e:
        print(f"Error: Could not import required modules. {e}")
        print("Make sure you have installed the requirements:")
        print("pip install -r document_intelligence/requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting Gradio interface: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 