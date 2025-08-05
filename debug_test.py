#!/usr/bin/env python3
"""
Debug test script for Document Intelligence Agent
"""

import os
import sys
from dotenv import load_dotenv

# Add the document_intelligence directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'document_intelligence'))

# Load environment variables
load_dotenv()

from agent_intelligence import DocumentIntelligenceAgent

def test_intent_analysis():
    """Test the intent analysis with different queries"""
    
    # Initialize the agent
    agent = DocumentIntelligenceAgent()
    
    # Test queries
    test_queries = [
        "What the paper is about?",
        "Who are the key people mentioned?",
        "Summarize this document",
        "Extract action items",
        "Translate to Spanish",
        "What is this about?"
    ]
    
    print("🧪 Testing Intent Analysis")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\n🔍 Testing query: '{query}'")
        
        # Test intent analysis only
        intent = agent.analyze_user_intent(query)
        print(f"   Action: {intent['action']}")
        print(f"   Confidence: {intent['confidence']}")
        print(f"   Reasoning: {intent['reasoning']}")
        print(f"   Parameters: {intent['parameters']}")

def test_action_execution():
    """Test action execution with sample content"""
    
    # Initialize the agent
    agent = DocumentIntelligenceAgent()
    
    # Sample document content
    sample_content = """
    Machine Learning Applications in Healthcare: A Comprehensive Review
    
    Abstract:
    This paper examines the transformative impact of machine learning algorithms in modern healthcare systems. Our analysis of 150 peer-reviewed studies reveals significant improvements in diagnostic accuracy, treatment planning, and patient outcomes.
    
    Key Findings:
    - ML algorithms achieve 94% accuracy in early cancer detection
    - Treatment recommendation systems reduce errors by 67%
    - Patient monitoring systems improve recovery rates by 23%
    
    Authors:
    - Dr. Sarah Johnson (Lead Researcher)
    - Prof. Michael Chen (Principal Investigator)
    - Dr. David Rodriguez (Data Scientist)
    
    Organizations:
    - Stanford Medical Center
    - MIT Computer Science Department
    - Google Health Research
    
    Action Items:
    - Implement pilot program by March 2024
    - Review regulatory compliance by February 15th
    - Schedule stakeholder meeting for January 30th
    """
    
    test_queries = [
        "What the paper is about?",
        "Who are the key people mentioned?",
        "What are the main findings?",
        "Extract action items"
    ]
    
    print("\n🧪 Testing Action Execution")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\n🔍 Testing query: '{query}'")
        
        # Process the full query
        result = agent.process_query(query, sample_content)
        
        print(f"   Intent Action: {result['intent_analysis']['action']}")
        print(f"   Confidence: {result['intent_analysis']['confidence']}")
        
        # Check the action result
        action_result = result['action_result']
        print(f"   Action Result Keys: {list(action_result.keys())}")
        
        # Show the main result
        if 'answer' in action_result:
            print(f"   Answer: {action_result['answer'][:200]}...")
        elif 'entities' in action_result:
            print(f"   Entities: {action_result['entities']}")
        elif 'action_items' in action_result:
            print(f"   Action Items: {action_result['action_items'][:200]}...")
        elif 'result' in action_result:
            print(f"   Summary: {action_result['result'][:200]}...")
        else:
            print(f"   Other Result: {action_result}")

if __name__ == "__main__":
    print("🤖 Document Intelligence Agent Debug Test")
    print("=" * 60)
    
    # Test intent analysis
    test_intent_analysis()
    
    # Test action execution
    test_action_execution()
    
    print("\n✅ Debug test completed!") 