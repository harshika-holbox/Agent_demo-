#!/usr/bin/env python3
"""
Test script for the Summarization Agent Lambda function
"""

import json
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the summarizer directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'summarizer'))

from app import lambda_handler

def test_summarization():
    """Test the summarization function with sample text"""
    
    # Sample text to summarize
    sample_text = """
    Artificial Intelligence (AI) has emerged as one of the most transformative technologies of the 21st century. 
    It encompasses a wide range of capabilities including machine learning, natural language processing, 
    computer vision, and robotics. AI systems can now perform tasks that traditionally required human intelligence, 
    such as recognizing speech, making decisions, and solving complex problems.
    
    The applications of AI are vast and growing rapidly. In healthcare, AI is being used for disease diagnosis, 
    drug discovery, and personalized treatment plans. In finance, it powers fraud detection, algorithmic trading, 
    and risk assessment. In transportation, AI enables autonomous vehicles and smart traffic management systems.
    
    However, the rapid advancement of AI also raises important ethical and societal questions. Concerns about 
    job displacement, privacy, bias in algorithms, and the potential for misuse have sparked global discussions 
    about responsible AI development and deployment.
    
    Despite these challenges, the potential benefits of AI are enormous. When developed and deployed responsibly, 
    AI can help solve some of humanity's most pressing problems, from climate change to healthcare access. 
    The key is ensuring that AI development is guided by ethical principles and serves the common good.
    """
    
    # Create test event
    test_event = {
        "input": sample_text.strip()
    }
    
    print("Testing Summarization Agent...")
    print(f"Input text length: {len(sample_text)} characters")
    print("-" * 50)
    
    # Check if AWS credentials are available
    if not os.getenv('AWS_ACCESS_KEY_ID') or not os.getenv('AWS_SECRET_ACCESS_KEY'):
        print("Warning: AWS credentials not found in environment variables")
        print("   Make sure your .env file contains AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
        print("   Or run: aws configure")
    
    try:
        # Call the lambda handler
        result = lambda_handler(test_event, None)
        
        print("Function executed successfully!")
        print(f"Status Code: {result.get('statusCode', 'N/A')}")
        
        if result.get('statusCode') == 200:
            body = json.loads(result.get('body', '{}'))
            print(f"Summary: {body.get('summary', 'No summary generated')}")
            print(f"Input Length: {body.get('input_length', 'N/A')}")
            print(f"Summary Length: {body.get('summary_length', 'N/A')}")
        else:
            print(f"Error: {result.get('body', 'Unknown error')}")
            
    except Exception as e:
        print(f"Test failed with error: {str(e)}")
        return False
    
    return True

def test_empty_input():
    """Test with empty input"""
    print("\nTesting with empty input...")
    
    test_event = {"input": ""}
    
    try:
        result = lambda_handler(test_event, None)
        print(f"Status Code: {result.get('statusCode', 'N/A')}")
        
        if result.get('statusCode') == 400:
            print("Correctly handled empty input")
        else:
            print("Should have returned 400 for empty input")
            
    except Exception as e:
        print(f"Test failed: {str(e)}")

def test_large_input():
    """Test with large input text"""
    print("\nTesting with large input...")
    
    # Create a large text (simulate long document)
    large_text = "This is a test sentence. " * 1000  # ~25,000 characters
    
    test_event = {"input": large_text}
    
    try:
        result = lambda_handler(test_event, None)
        print(f"Status Code: {result.get('statusCode', 'N/A')}")
        
        if result.get('statusCode') == 200:
            body = json.loads(result.get('body', '{}'))
            print(f"Input Length: {body.get('input_length', 'N/A')}")
            print(f"Summary Length: {body.get('summary_length', 'N/A')}")
            print("Successfully processed large input")
        else:
            print(f"Failed to process large input: {result.get('body', 'Unknown error')}")
            
    except Exception as e:
        print(f"Test failed: {str(e)}")

if __name__ == "__main__":
    print("Starting Summarization Agent Tests")
    print("=" * 50)
    
    # Run tests
    success = test_summarization()
    test_empty_input()
    test_large_input()
    
    print("\n" + "=" * 50)
    if success:
        print("All tests completed!")
    else:
        print("Some tests failed!")
        sys.exit(1) 