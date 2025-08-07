import boto3
import json
import os
from dotenv import load_dotenv
import gradio as gr
from document_processor import DocumentProcessor
from crewai_agent_system import DocumentIntelligenceCrew

# Load environment variables from .env file
load_dotenv()

def lambda_handler(event, context):
    """
    Lambda function for Document Intelligence Agent using Amazon Bedrock
    """
    try:
        # Extract input from the event
        input_text = event.get("input", "")
        file_content = event.get("file_content", "")  # Base64 encoded file content
        filename = event.get("filename", "")
        user_query = event.get("user_query", "Summarize this document")
        
        # Initialize document processor and agent
        doc_processor = DocumentProcessor()
        agent = DocumentIntelligenceCrew()
        
        # Determine input source
        if file_content and filename:
            try:
                # Decode base64 file content
                import base64
                file_bytes = base64.b64decode(file_content)
                
                # Process file
                extracted_text, file_type = doc_processor.process_file(file_bytes, filename)
                document_content = extracted_text
                source_info = f"File: {filename} ({file_type.upper()})"
                
            except Exception as e:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": f"Error processing file: {str(e)}"})
                }
        elif input_text:
            document_content = input_text
            source_info = "Direct text input"
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No input text or file provided"})
            }

        # Process with intelligent agent
        result = agent.process_query(user_query, document_content, filename if filename else "text_input")
        
        # Extract the main response (CrewAI format, handle CrewOutput objects)
        main_response = getattr(result['result'], 'raw', str(result['result']))
        agent_type = "CrewAI Multi-Agent System"
        agents_used = result.get('agents_used', [])
        crew_type = result.get('crew_type', 'unknown')
        complexity = result.get('complexity', 'unknown')
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "agent_response": main_response,
                "source": source_info,
                "user_query": user_query,
                "agent_type": agent_type,
                "agents_used": agents_used,
                "crew_type": crew_type,
                "complexity": complexity,
                "input_length": len(document_content)
            })
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Error processing request: {str(e)}"})
        }

def intelligent_document_agent(input_text, uploaded_file, user_query):
    """
    Advanced Document Intelligence Agent interface using CrewAI
    """
    try:
        # Initialize document processor and agent
        doc_processor = DocumentProcessor()
        agent = DocumentIntelligenceCrew()
        agent_type = "CrewAI Multi-Agent System"
        
        # Determine input source
        if uploaded_file is not None:
            # Process uploaded file
            try:
                print(f"🔧 Debug - Gradio file object type: {type(uploaded_file)}")
                print(f"🔧 Debug - Gradio file object: {uploaded_file}")
                
                file_content = None
                filename = None
                
                # Handle different Gradio file formats
                if isinstance(uploaded_file, str):
                    # Gradio 3.x - file path as string
                    file_path = uploaded_file
                    filename = os.path.basename(file_path)
                    print(f"📁 Reading file from path: {file_path}")
                    with open(file_path, 'rb') as f:
                        file_content = f.read()
                        
                elif isinstance(uploaded_file, tuple) and len(uploaded_file) >= 2:
                    # Tuple format (file_path, filename)
                    file_path = uploaded_file[0]
                    filename = uploaded_file[1] if uploaded_file[1] else os.path.basename(file_path)
                    print(f"📁 Reading file from tuple: {file_path}, name: {filename}")
                    with open(file_path, 'rb') as f:
                        file_content = f.read()
                        
                elif hasattr(uploaded_file, 'name') and os.path.isfile(uploaded_file.name):
                    # File object with path
                    file_path = uploaded_file.name
                    filename = os.path.basename(file_path)
                    print(f"📁 Reading file from object.name: {file_path}")
                    with open(file_path, 'rb') as f:
                        file_content = f.read()
                        
                elif hasattr(uploaded_file, 'read'):
                    # File-like object with read method
                    print("📁 Reading from file-like object")
                    file_content = uploaded_file.read()
                    filename = getattr(uploaded_file, 'name', 'uploaded_file')
                    if hasattr(file_content, 'decode'):
                        # If it's text, we might need to handle it differently
                        print("⚠️  Warning: Got text content, might need binary")
                        
                else:
                    # Last resort - try to use the object directly
                    print(f"⚠️  Unknown file format, attempting direct use")
                    file_content = uploaded_file
                    filename = getattr(uploaded_file, 'name', 'uploaded_file')
                
                # Validate we got content
                if file_content is None:
                    return f"Error: Could not extract file content from uploaded file"
                    
                if not filename:
                    filename = 'uploaded_file'
                
                print(f"📊 File info: {filename}, {len(file_content)} bytes")
                
                # Extract text from file
                extracted_text, file_type = doc_processor.process_file(file_content, filename)
                document_content = extracted_text
                source_info = f"File: {filename} ({file_type.upper()})"
                
            except Exception as e:
                error_msg = f"Error processing file: {str(e)}"
                print(f"❌ {error_msg}")
                import traceback
                traceback.print_exc()
                return error_msg
        elif input_text and input_text.strip():
            # Use provided text
            document_content = input_text
            source_info = "Direct text input"
        else:
            return "Error: Please provide either text input or upload a file."
        
        # Check if AWS credentials are available using boto3 (updated from env vars)
        try:
            session = boto3.Session()
            credentials = session.get_credentials()
            if credentials is None:
                return "Error: AWS credentials not configured. Please configure your AWS credentials using AWS CLI, environment variables, or IAM roles."
        except Exception as e:
            return f"Error checking AWS credentials: {str(e)}"
        
        # Test AWS Bedrock connection
        try:
            test_bedrock = boto3.client("bedrock-runtime")
            print("AWS Bedrock client created successfully")
        except Exception as e:
            return f"Error: Cannot create AWS Bedrock client: {str(e)}"
        
        # Process user query with the intelligent agent
        if user_query and user_query.strip():
            # Use the intelligent agent to process the query
            result = agent.process_query(user_query, document_content, filename if 'filename' in locals() else "text_input")
                
            # Debug: Print the full result structure
            print(f"Debug - Full result: {result}")
            
            # Extract the main result (CrewAI format, handle CrewOutput objects)
            main_result = getattr(result['result'], 'raw', str(result['result']))
            agents_used = result.get('agents_used', [])
            crew_type = result.get('crew_type', 'unknown')
            complexity = result.get('complexity', 'unknown')
            result_title = f"CrewAI {crew_type.replace('_', ' ').title()}"
            
            print(f"Debug - Agent type: {agent_type}")
            print(f"Debug - Main result: {main_result[:200]}...")
            
            # Format the response
            response = f"""
## Document Intelligence Agent Response

**Source:** {source_info}
**User Query:** {result['user_query']}
**Agent Type:** {agent_type}

### Agent Information
**Crew Type:** {crew_type.replace('_', ' ').title()}
**Complexity:** {complexity.title()}
**Agents Used:** {', '.join(agents_used)}

### {result_title}
{main_result}

### Document Statistics
- **Input Length:** {len(document_content)} characters
- **Processing Time:** Real-time
- **Agent Memory:** Active
                """
                
        else:
            # Default to summarization if no specific query
            result = agent.process_query("Summarize this document", document_content)
            
            main_result = getattr(result['result'], 'raw', str(result['result']))
            agents_used = result.get('agents_used', [])
            crew_type = result.get('crew_type', 'summarization')
            complexity = result.get('complexity', 'unknown')
            
            response = f"""
## Document Intelligence Agent - Auto Summary

**Source:** {source_info}
**Agent Type:** {agent_type}

### Summary
{main_result}

### Agent Information
**Crew Type:** {crew_type.replace('_', ' ').title()}
**Complexity:** {complexity.title()}
**Agents Used:** {', '.join(agents_used)}

### Document Statistics
- **Input Length:** {len(document_content)} characters
- **Agent Action:** {crew_type.upper()}
                """
        
        return response
        
    except Exception as e:
        return f"Error: {str(e)}"

def create_gradio_interface():
    """
    Create and launch the Gradio interface with CrewAI option
    """
    # Initialize document processor for format info
    doc_processor = DocumentProcessor()
    
    # Define the interface
    iface = gr.Interface(
        fn=intelligent_document_agent,
        inputs=[
            gr.Textbox(
                label="Document Content",
                placeholder="Enter or paste your document text here...",
                lines=6
            ),
            gr.File(
                label="Upload Document",
                file_types=[
                    ".pdf", ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp",
                    ".docx", ".doc", ".xlsx", ".xls", ".csv", ".txt", ".md", ".rtf"
                ]
            ),
            gr.Textbox(
                label="What would you like me to do?",
                placeholder="Ask me anything about your document!",
                lines=2
            ),
        ],
        outputs=[
            gr.Markdown(
                label="Agent Response"
            )
        ],
        title="AWS Agent Core - Document Intelligence Agent",
        description="An intelligent document processing agent that can understand your documents and answer questions, extract insights, translate content, and much more. Powered by Claude 3 Sonnet, AWS Agent Core, and CrewAI multi-agent system."
        # Removed theme and css for compatibility with Gradio 3.50.2
    )
    return iface

if __name__ == "__main__":
    # Launch the Gradio interface
    iface = create_gradio_interface()
    print("Starting Gradio interface for AWS Agent Core Document Intelligence Agent...")
    print("Make sure you have AWS credentials configured in your environment.")
    print("You can set them using: export AWS_ACCESS_KEY_ID=your_key && export AWS_SECRET_ACCESS_KEY=your_secret")
    iface.launch(share=False, server_name="0.0.0.0", server_port=7860)