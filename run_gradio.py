#!/usr/bin/env python3
"""
Launcher script for the AWS Agent Core Document Intelligence Agent Gradio interface
"""

import os
import sys
from dotenv import load_dotenv

# Add the document_intelligence directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'document_intelligence'))

# Load environment variables
load_dotenv()

def check_aws_credentials():
    """Check if AWS credentials are configured"""
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    if not access_key or not secret_key:
        print("Warning: AWS credentials not found!")
        print("Please set your AWS credentials:")
        print("1. Create a .env file in the project root with:")
        print("   AWS_ACCESS_KEY_ID=your_access_key")
        print("   AWS_SECRET_ACCESS_KEY=your_secret_key")
        print("   AWS_DEFAULT_REGION=your_region")
        print("2. Or set environment variables:")
        print("   export AWS_ACCESS_KEY_ID=your_access_key")
        print("   export AWS_SECRET_ACCESS_KEY=your_secret_key")
        print("   export AWS_DEFAULT_REGION=your_region")
        print()
        response = input("Do you want to continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    else:
        print("AWS credentials found!")

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