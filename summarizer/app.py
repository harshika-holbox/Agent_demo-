import boto3
import json
import os
from dotenv import load_dotenv
import gradio as gr
from document_processor import DocumentProcessor

# Load environment variables from .env file
load_dotenv()

def lambda_handler(event, context):
    """
    Lambda function for text summarization using Amazon Bedrock
    """
    try:
        # Extract input from the event
        input_text = event.get("input", "")
        file_content = event.get("file_content", "")  # Base64 encoded file content
        filename = event.get("filename", "")
        
        # Initialize document processor
        doc_processor = DocumentProcessor()
        
        # Determine input source
        if file_content and filename:
            try:
                # Decode base64 file content
                import base64
                file_bytes = base64.b64decode(file_content)
                
                # Process file
                extracted_text, file_type = doc_processor.process_file(file_bytes, filename)
                text_to_summarize = extracted_text
                source_info = f"File: {filename} ({file_type.upper()})"
                
            except Exception as e:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": f"Error processing file: {str(e)}"})
                }
        elif input_text:
            text_to_summarize = input_text
            source_info = "Direct text input"
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No input text or file provided"})
            }

        # Initialize Bedrock client (credentials from environment)
        bedrock = boto3.client("bedrock-runtime")
        
        # Get model ID from environment or use default
        model_id = os.getenv('BEDROCK_MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0')
        
        # Use the correct format for Claude 3 in Bedrock
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 300,
            "messages": [
                {
                    "role": "user",
                    "content": f"Please provide a concise summary of the following text. Focus on the main points and key information:\n\n{text_to_summarize}"
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
                "source": source_info,
                "input_length": len(text_to_summarize),
                "summary_length": len(summary)
            })
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Error processing request: {str(e)}"})
        }

def summarize_text_gradio(input_text, uploaded_file):
    """
    Gradio interface function for text summarization with file support
    """
    try:
        # Initialize document processor
        doc_processor = DocumentProcessor()
        
        # Determine input source
        if uploaded_file is not None:
            # Process uploaded file
            try:
                # Debug: Print the type and attributes of uploaded_file
                print(f"Debug: uploaded_file type: {type(uploaded_file)}")
                print(f"Debug: uploaded_file attributes: {dir(uploaded_file)}")
                
                # Handle Gradio file object format - it might be a tuple (file_path, file_name)
                if isinstance(uploaded_file, tuple) and len(uploaded_file) >= 2:
                    file_path = uploaded_file[0]
                    filename = uploaded_file[1]
                    with open(file_path, 'rb') as f:
                        file_content = f.read()
                elif hasattr(uploaded_file, 'read'):
                    # Standard file-like object
                    file_content = uploaded_file.read()
                    filename = uploaded_file.name
                elif hasattr(uploaded_file, 'name'):
                    # Object with name attribute
                    with open(uploaded_file.name, 'rb') as f:
                        file_content = f.read()
                    filename = uploaded_file.name
                else:
                    # Try to get file content from the object
                    file_content = uploaded_file
                    filename = getattr(uploaded_file, 'name', 'uploaded_file')
                
                # Extract text from file
                extracted_text, file_type = doc_processor.process_file(file_content, filename)
                
                # Use extracted text for summarization
                text_to_summarize = extracted_text
                source_info = f"File: {filename} ({file_type.upper()})"
                
            except Exception as e:
                return f"Error processing file: {str(e)}"
        elif input_text and input_text.strip():
            # Use provided text
            text_to_summarize = input_text
            source_info = "Direct text input"
        else:
            return "Error: Please provide either text input or upload a file."
        
        # Check if AWS credentials are available
        if not os.getenv('AWS_ACCESS_KEY_ID') or not os.getenv('AWS_SECRET_ACCESS_KEY'):
            return "Error: AWS credentials not configured. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
        
        # Initialize Bedrock client
        bedrock = boto3.client("bedrock-runtime")
        
        # Get model ID from environment or use default
        model_id = os.getenv('BEDROCK_MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0')
        
        # Prepare request for Claude 3
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 300,
            "messages": [
                {
                    "role": "user",
                    "content": f"Please provide a concise summary of the following text. Focus on the main points and key information:\n\n{text_to_summarize}"
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
        
        # Return formatted result
        return f"**Source:** {source_info}\n\n**Summary:**\n{summary.strip()}\n\n**Input Length:** {len(text_to_summarize)} characters\n**Summary Length:** {len(summary)} characters"
        
    except Exception as e:
        return f"Error: {str(e)}"

def create_gradio_interface():
    """
    Create and launch the Gradio interface
    """
    # Initialize document processor for format info
    doc_processor = DocumentProcessor()
    
    # Define the interface
    iface = gr.Interface(
        fn=summarize_text_gradio,
        inputs=[
            gr.Textbox(
                label="Text to Summarize",
                placeholder="Enter or paste your text here...",
                lines=8,
                max_lines=15
            ),
            gr.File(
                label="Upload Document",
                file_types=[
                    ".pdf", ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp",
                    ".docx", ".doc", ".xlsx", ".xls", ".csv", ".txt", ".md", ".rtf"
                ],
                file_count="single"
            )
        ],
        outputs=[
            gr.Markdown(
                label="Summary Result"
            )
        ],
        title="AWS Agent Core - Multi-Format Document Summarizer",
        description="An intelligent document summarization agent that supports PDFs, images, Word docs, Excel files, and more. Powered by Claude 3 Sonnet and Amazon Bedrock.",
        examples=[
            [
                "Artificial Intelligence (AI) has emerged as one of the most transformative technologies of the 21st century. It encompasses a wide range of capabilities including machine learning, natural language processing, computer vision, and robotics. AI systems can now perform tasks that traditionally required human intelligence, such as recognizing speech, making decisions, and solving complex problems. The applications of AI are vast and growing rapidly. In healthcare, AI is being used for disease diagnosis, drug discovery, and personalized treatment plans. In finance, it powers fraud detection, algorithmic trading, and risk assessment. In transportation, AI enables autonomous vehicles and smart traffic management systems.",
                None
            ],
            [
                "Climate change represents one of the most pressing challenges facing humanity today. The Earth's average temperature has risen by approximately 1.1 degrees Celsius since pre-industrial times, primarily due to human activities such as burning fossil fuels, deforestation, and industrial processes. This warming has led to more frequent and severe weather events, including hurricanes, droughts, heatwaves, and heavy rainfall. The consequences of climate change are far-reaching, affecting ecosystems, agriculture, water resources, and human health. Rising sea levels threaten coastal communities, while changing precipitation patterns impact food production. Addressing climate change requires global cooperation, technological innovation, and policy changes to reduce greenhouse gas emissions and adapt to changing conditions.",
                None
            ]
        ],
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 900px;
            margin: auto;
        }
        .file-upload {
            border: 2px dashed #ccc;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }
        """,
        article=f"""
        ## Supported File Formats
        
        {doc_processor.get_supported_formats_info()}
        
        ## How to Use
        
        1. **Text Input**: Simply paste or type your text in the text box
        2. **File Upload**: Upload any supported document format
        3. **OCR Support**: Images with text will be processed using OCR
        4. **Multi-page Support**: PDFs and documents with multiple pages are fully supported
        
        ## Features
        
        - **PDF Processing**: Extract text from PDF documents
        - **Image OCR**: Extract text from images using optical character recognition
        - **Office Documents**: Support for Word (.docx, .doc) and Excel (.xlsx, .xls) files
        - **Data Files**: CSV and text file processing
        - **AI-Powered Summarization**: Uses Claude 3 Sonnet for intelligent summarization
        """
    )
    
    return iface

if __name__ == "__main__":
    # Launch the Gradio interface
    iface = create_gradio_interface()
    print("Starting Gradio interface for AWS Agent Core Summarizer...")
    print("Make sure you have AWS credentials configured in your environment.")
    print("You can set them using: export AWS_ACCESS_KEY_ID=your_key && export AWS_SECRET_ACCESS_KEY=your_secret")
    iface.launch(share=False, server_name="0.0.0.0", server_port=7860)
