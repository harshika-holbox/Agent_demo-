import boto3
import json
import os
from dotenv import load_dotenv
import gradio as gr
from document_processor import DocumentProcessor
from agent_intelligence import DocumentIntelligenceAgent

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
        agent = DocumentIntelligenceAgent()
        
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
        
        # Extract the main response
        action_result = result['action_result']
        main_response = action_result.get('result', 
                                        action_result.get('answer', 
                                        action_result.get('insights', 
                                        action_result.get('classification', 
                                        action_result.get('translation', 
                                        action_result.get('sentiment_analysis', 
                                        action_result.get('action_items', 
                                        action_result.get('entities', 
                                        action_result.get('analysis', 'No response generated')))))))))
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "agent_response": main_response,
                "source": source_info,
                "user_query": user_query,
                "agent_action": result['intent_analysis']['action'],
                "confidence": result['intent_analysis']['confidence'],
                "reasoning": result['agent_reasoning'],
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
    Advanced Document Intelligence Agent interface
    """
    try:
        # Initialize document processor and agent
        doc_processor = DocumentProcessor()
        agent = DocumentIntelligenceAgent()
        
        # Determine input source
        if uploaded_file is not None:
            # Process uploaded file
            try:
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
                document_content = extracted_text
                source_info = f"File: {filename} ({file_type.upper()})"
                
            except Exception as e:
                return f"Error processing file: {str(e)}"
        elif input_text and input_text.strip():
            # Use provided text
            document_content = input_text
            source_info = "Direct text input"
        else:
            return "Error: Please provide either text input or upload a file."
        
        # Check if AWS credentials are available
        if not os.getenv('AWS_ACCESS_KEY_ID') or not os.getenv('AWS_SECRET_ACCESS_KEY'):
            return "Error: AWS credentials not configured. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
        
        # Test AWS Bedrock connection
        try:
            test_bedrock = boto3.client("bedrock-runtime")
            print("✅ AWS Bedrock client created successfully")
        except Exception as e:
            return f"Error: Cannot create AWS Bedrock client: {str(e)}"
        
        # Process user query with the intelligent agent
        if user_query and user_query.strip():
            # Use the intelligent agent to process the query
            result = agent.process_query(user_query, document_content, filename if 'filename' in locals() else "text_input")
                
            # Debug: Print the full result structure
            print(f"🔍 Debug - Full result: {result}")
            print(f"🔍 Debug - Action result: {result.get('action_result', {})}")
            
            # Extract the main result from action_result
            action_result = result.get('action_result', {})
            action_type = result['intent_analysis']['action']
                
            # Get the appropriate result based on action type
            if action_type == "summarize":
                main_result = action_result.get('result', 'No summary generated')
                result_title = "📋 Summary"
            elif action_type == "answer_question":
                main_result = action_result.get('answer', 'No answer generated')
                result_title = "❓ Answer"
            elif action_type == "extract_entities":
                entities = action_result.get('entities', {})
                if isinstance(entities, dict):
                    main_result = "\n".join([f"**{k.title()}:** {', '.join(v) if isinstance(v, list) else str(v)}" for k, v in entities.items()])
                else:
                    main_result = str(entities)
                result_title = "👥 Extracted Entities"
            elif action_type == "translate":
                main_result = action_result.get('translation', 'No translation generated')
                result_title = f"🌐 Translation ({action_result.get('target_language', 'Unknown')})"
            elif action_type == "classify":
                main_result = action_result.get('classification', 'No classification generated')
                result_title = "🏷️ Document Classification"
            elif action_type == "extract_insights":
                main_result = action_result.get('insights', 'No insights generated')
                result_title = "💡 Key Insights"
            elif action_type == "analyze_sentiment":
                main_result = action_result.get('sentiment_analysis', 'No sentiment analysis generated')
                result_title = "😊 Sentiment Analysis"
            elif action_type == "extract_action_items":
                main_result = action_result.get('action_items', 'No action items found')
                result_title = "✅ Action Items"
            elif action_type == "compare_documents":
                main_result = action_result.get('analysis', 'No comparison analysis generated')
                result_title = "📊 Document Comparison"
            elif action_type == "ask_clarification":
                main_result = action_result.get('message', 'Please clarify what you would like me to do.')
                result_title = "❓ Clarification Needed"
            else:
                main_result = (action_result.get('result') or 
                              action_result.get('answer') or 
                              action_result.get('insights') or 
                              action_result.get('classification') or 
                              action_result.get('translation') or 
                              action_result.get('sentiment_analysis') or 
                              action_result.get('action_items') or 
                              action_result.get('entities') or 
                              action_result.get('analysis') or 
                              action_result.get('message') or 
                              'No results available')
                result_title = "📋 Results"
            
            print(f"🔍 Debug - Action type: {action_type}")
            print(f"🔍 Debug - Main result: {main_result[:200]}...")
            
            # Format the response
            response = f"""
## 🤖 Document Intelligence Agent Response

**Source:** {source_info}
**User Query:** {result['user_query']}

### 🧠 Agent Reasoning
**Action Chosen:** {result['intent_analysis']['action'].upper()}
**Confidence:** {result['intent_analysis']['confidence']:.2f}
**Reasoning:** {result['agent_reasoning']}

### {result_title}
{main_result}

### 📊 Document Statistics
- **Input Length:** {len(document_content)} characters
- **Processing Time:** Real-time
- **Agent Memory:** Active
            """
                
        else:
            # Default to summarization if no specific query
            result = agent.process_query("Summarize this document", document_content)
            response = f"""
## 🤖 Document Intelligence Agent - Auto Summary

**Source:** {source_info}

### 📋 Summary
{result['action_result'].get('result', 'No summary generated')}

### 📊 Document Statistics
- **Input Length:** {len(document_content)} characters
- **Agent Action:** {result['intent_analysis']['action'].upper()}
- **Confidence:** {result['intent_analysis']['confidence']:.2f}
            """
        
        return response
        
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
        fn=intelligent_document_agent,
        inputs=[
            gr.Textbox(
                label="Document Content",
                placeholder="Enter or paste your document text here...",
                lines=6,
                max_lines=12
            ),
            gr.File(
                label="Upload Document",
                file_types=[
                    ".pdf", ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp",
                    ".docx", ".doc", ".xlsx", ".xls", ".csv", ".txt", ".md", ".rtf"
                ],
                file_count="single"
            ),
            gr.Textbox(
                label="What would you like me to do?",
                placeholder="Ask me anything about your document! Examples: 'Summarize this', 'Who are the key people mentioned?', 'What are the main conclusions?', 'Translate to Spanish', 'Extract action items'",
                lines=2
            )
        ],
        outputs=[
            gr.Markdown(
                label="Agent Response"
            )
        ],
        title="🤖 AWS Agent Core - Document Intelligence Agent",
        description="An intelligent document processing agent that can understand your documents and answer questions, extract insights, translate content, and much more. Powered by Claude 3 Sonnet and AWS Agent Core.",
        examples=[
            [
                "Artificial Intelligence (AI) has emerged as one of the most transformative technologies of the 21st century. It encompasses a wide range of capabilities including machine learning, natural language processing, computer vision, and robotics. AI systems can now perform tasks that traditionally required human intelligence, such as recognizing speech, making decisions, and solving complex problems. The applications of AI are vast and growing rapidly. In healthcare, AI is being used for disease diagnosis, drug discovery, and personalized treatment plans. In finance, it powers fraud detection, algorithmic trading, and risk assessment. In transportation, AI enables autonomous vehicles and smart traffic management systems.",
                None,
                "Summarize the key applications of AI mentioned in this text"
            ],
            [
                "Climate change represents one of the most pressing challenges facing humanity today. The Earth's average temperature has risen by approximately 1.1 degrees Celsius since pre-industrial times, primarily due to human activities such as burning fossil fuels, deforestation, and industrial processes. This warming has led to more frequent and severe weather events, including hurricanes, droughts, heatwaves, and heavy rainfall. The consequences of climate change are far-reaching, affecting ecosystems, agriculture, water resources, and human health. Rising sea levels threaten coastal communities, while changing precipitation patterns impact food production. Addressing climate change requires global cooperation, technological innovation, and policy changes to reduce greenhouse gas emissions and adapt to changing conditions.",
                None,
                "What are the main causes and consequences of climate change?"
            ],
            [
                "",
                None,
                "Who are the key people mentioned in this document?"
            ],
            [
                "",
                None,
                "Extract all action items and deadlines"
            ],
            [
                "",
                None,
                "Translate this document to Spanish"
            ]
        ],
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1000px;
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
        ## 🚀 Advanced Document Intelligence Agent

        This agent can understand your documents and perform multiple intelligent tasks:

        ### 🧠 Agent Capabilities
        - **Smart Summarization**: Intelligent document summaries
        - **Document Q&A**: Ask questions about your documents
        - **Entity Extraction**: Find people, organizations, dates, locations
        - **Document Translation**: Translate content to multiple languages
        - **Document Classification**: Automatically categorize documents
        - **Insight Extraction**: Find key insights and patterns
        - **Sentiment Analysis**: Analyze document tone and sentiment
        - **Action Item Extraction**: Find tasks, deadlines, and responsibilities
        - **Information Search**: Find specific information in documents

        ### 📄 Supported File Formats
        {doc_processor.get_supported_formats_info()}

        ### 💡 Example Queries
        - "Summarize this document"
        - "Who are the key people mentioned?"
        - "What are the main conclusions?"
        - "Extract all action items and deadlines"
        - "Translate this to Spanish"
        - "What type of document is this?"
        - "Find all dates mentioned"
        - "What are the key insights?"
        - "Analyze the sentiment of this document"
        - "Compare this with other documents"

        ### 🎯 Agent Intelligence
        The agent automatically decides the best action based on your query and provides reasoning for its decisions. It can handle complex requests and maintain context across multiple interactions.

        ### 🔧 Technical Features
        - **Multi-Modal Processing**: Text, images, documents
        - **Real-time Analysis**: Instant processing and responses
        - **Context Awareness**: Remembers previous interactions
        - **Confidence Scoring**: Shows how confident the agent is in its analysis
        - **AWS Integration**: Full cloud-native architecture
        """
    )
    
    return iface

if __name__ == "__main__":
    # Launch the Gradio interface
    iface = create_gradio_interface()
    print("Starting Gradio interface for AWS Agent Core Document Intelligence Agent...")
    print("Make sure you have AWS credentials configured in your environment.")
    print("You can set them using: export AWS_ACCESS_KEY_ID=your_key && export AWS_SECRET_ACCESS_KEY=your_secret")
    iface.launch(share=False, server_name="0.0.0.0", server_port=7860)
