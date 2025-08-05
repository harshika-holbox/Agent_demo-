# 🤖 AWS Agent Core - Document Intelligence Agent

## 📋 Project Overview

This project demonstrates the development of an **intelligent document processing agent** using **AWS Agent Core** framework, designed to showcase advanced AI capabilities beyond simple summarization. The agent can understand user intent, process multiple document formats, and perform intelligent analysis based on natural language queries.

## 🎯 What I Did in This Project

### 1. **Intelligent Agent Architecture Design**
- Designed a multi-capability document intelligence agent using AWS Agent Core
- Implemented intent analysis system that understands user queries in natural language
- Created action-based execution framework for different document processing tasks
- Built intelligent decision-making logic that chooses appropriate actions based on user intent

### 2. **Advanced Document Processing Capabilities**
- **Multi-Format Support**: PDF, Images (with OCR), Word documents, Excel files, CSV, Text files
- **Intelligent Query Processing**: The agent understands what users want and executes appropriate actions
- **Context-Aware Responses**: Maintains context and provides relevant, structured responses

### 3. **Comprehensive Feature Implementation**
- **Question Answering**: Direct answers to specific questions about documents
- **Entity Extraction**: Extract people, organizations, dates, locations
- **Document Classification**: Automatically classify document types
- **Sentiment Analysis**: Analyze tone and emotional content
- **Translation Services**: Multi-language document translation
- **Insight Extraction**: Identify patterns, trends, and key findings
- **Action Item Detection**: Find tasks, deadlines, and responsibilities
- **Information Search**: Locate specific information within documents

### 4. **Technical Infrastructure Development**
- **AWS Integration**: Full integration with AWS Bedrock (Claude 3 Sonnet)
- **Serverless Architecture**: Deployed using AWS Lambda and API Gateway
- **Gradio Web Interface**: User-friendly web UI for testing and demonstration
- **Python Deployment Scripts**: Automated deployment and configuration management

### 5. **Quality Assurance & Testing**
- Comprehensive debugging and testing framework
- Intent analysis validation and optimization
- Response formatting and error handling
- Multi-format document processing validation

## 🚀 What Makes This Agent Different from Other Tools

### **1. Intelligent Intent Recognition**
Unlike traditional summarization tools that only provide summaries, this agent:
- **Understands User Intent**: Analyzes what the user actually wants (summary, Q&A, entity extraction, etc.)
- **Context-Aware Processing**: Chooses the most appropriate action based on the query
- **Natural Language Understanding**: Processes queries like "Who are the key people mentioned?" or "What are the main findings?"

### **2. Multi-Capability Framework**
Most document tools are single-purpose. This agent provides:
- **10+ Different Capabilities** in one unified interface
- **Seamless Switching** between different analysis types
- **Comprehensive Document Intelligence** beyond just text processing

### **3. AWS Agent Core Integration**
- **Enterprise-Grade Framework**: Built on AWS's official agent framework
- **Scalable Architecture**: Can handle multiple users and large documents
- **Professional Deployment**: Ready for production use in enterprise environments

### **4. Advanced Document Processing**
- **OCR Integration**: Can extract text from images and scanned documents
- **Multi-Format Support**: Handles PDFs, Word docs, Excel files, images, etc.
- **Structured Data Extraction**: Can extract tables, charts, and formatted data

### **5. Intelligent Response Formatting**
- **Action-Specific Responses**: Different response formats for different actions
- **Structured Output**: Organized, readable responses with clear sections
- **Confidence Scoring**: Shows how confident the agent is in its analysis

## 🏗️ Technical Architecture

### **Framework: AWS Agent Core**
- **Purpose**: AWS's official framework for building intelligent agents for the AWS Agent Marketplace
- **Benefits**: Enterprise-grade scalability, security, and integration
- **Components**: 
  - **Agent Configuration**: Defines agent behavior, capabilities, and instructions
  - **Action Groups**: Modular functions that the agent can execute
  - **API Schema**: OpenAPI specification for agent interactions
  - **Marketplace Integration**: Deployment and discovery through AWS Agent Marketplace
  - **Agent Management**: Lifecycle management, versioning, and monitoring

### **Core Technologies**

#### **1. AWS Services**
- **AWS Bedrock**: Foundation model access (Claude 3 Sonnet)
- **AWS Lambda**: Serverless compute for agent logic
- **API Gateway**: REST API endpoints for agent interaction
- **IAM**: Security and permissions management
- **CloudFormation/SAM**: Infrastructure as code deployment

#### **2. AI/ML Components**
- **Claude 3 Sonnet**: Advanced language model for document understanding
- **Intent Analysis Engine**: Custom logic for understanding user queries
- **Action Execution Framework**: Modular system for different document tasks
- **Response Generation**: Intelligent formatting based on action type

#### **3. Document Processing**
- **PyPDF2 & pdfplumber**: PDF text extraction
- **Pillow & pytesseract**: Image processing and OCR
- **python-docx**: Word document processing
- **openpyxl & pandas**: Excel and CSV processing
- **Document Processor**: Unified interface for all formats

#### **4. Web Interface**
- **Gradio**: Modern web UI for testing and demonstration
- **Real-time Processing**: Live document analysis
- **Multi-format Upload**: Support for various file types
- **Interactive Query Interface**: Natural language input

### **System Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Gradio UI     │    │  AWS Agent Core │    │  AWS Lambda     │    │  AWS Bedrock    │
│                 │    │                 │    │                 │    │                 │
│ • File Upload   │───▶│ • Agent         │───▶│ • Intent        │───▶│ • Claude 3      │
│ • Query Input   │    │   Configuration │    │   Analysis      │    │   Sonnet        │
│ • Response      │    │ • Action Groups │    │ • Action        │    │ • Document      │
│   Display       │    │ • API Schema    │    │   Execution     │    │   Processing    │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │                       │
         │                       │                       ▼                       │
         │                       │              ┌─────────────────┐              │
         │                       │              │ Document        │              │
         └───────────────────────┼──────────────▶│ Processor       │◀─────────────┘
                                 │              │                 │
                                 │              │ • PDF/Image     │
                                 │              │ • Word/Excel    │
                                 │              │ • OCR Support   │
                                 │              └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ AWS Marketplace │
                        │                 │
                        │ • Agent         │
                        │   Discovery     │
                        │ • Integration   │
                        │ • Management    │
                        └─────────────────┘
```

## 🔧 Technical Implementation Details

### **1. Intent Analysis System**
```python
def _fallback_intent_analysis(self, user_query: str) -> Dict[str, Any]:
    """Intelligent intent detection using keyword matching"""
    query_lower = user_query.lower()
    
    # Prioritize specific queries over general ones
    if any(word in query_lower for word in ['what', 'how', 'why', 'when', 'where', 'which']):
        return {"action": "answer_question", "confidence": 0.8}
    elif any(word in query_lower for word in ['who', 'person', 'people']):
        return {"action": "extract_entities", "confidence": 0.7}
    # ... more intent patterns
```

### **2. Action Execution Framework**
```python
def execute_action(self, action: str, document_content: str, parameters: Dict) -> Dict[str, Any]:
    """Modular action execution system"""
    if action == "answer_question":
        return self._answer_question(document_content, parameters)
    elif action == "extract_entities":
        return self._extract_entities(document_content, parameters)
    elif action == "summarize":
        return self._summarize_document(document_content)
    # ... more actions
```

### **3. Multi-Format Document Processing**
```python
class DocumentProcessor:
    """Unified document processing interface"""
    
    def process_file(self, file_content: bytes, filename: str) -> Tuple[str, str]:
        """Process any supported file format"""
        if filename.lower().endswith('.pdf'):
            return self.extract_text_from_pdf(file_content), 'pdf'
        elif filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            return self.extract_text_from_image(file_content), 'image'
        # ... more formats
```

### **4. AWS Bedrock Integration**
```python
def _call_bedrock(self, prompt: str) -> str:
    """Advanced AI model integration"""
    response = self.bedrock_client.invoke_model(
        modelId=self.model_id,
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2000,
            "temperature": 0.1,
            "messages": [{"role": "user", "content": prompt}]
        })
    )
```

## 📊 Project Structure

```
DOCUMENT_INTELLIGENCE_AGENT/
├── .env                          # AWS credentials configuration
├── agent-config.yaml             # AWS Agent Core configuration
├── template.yaml                 # AWS SAM deployment template
├── deploy.py                     # Python deployment automation
├── run_gradio.py                 # Gradio interface launcher
├── debug_test.py                 # Testing and debugging utilities
└── document_intelligence/
    ├── app.py                    # Lambda function + Gradio interface
    ├── agent_intelligence.py     # Core agent logic and intelligence
    ├── document_processor.py     # Multi-format document processing
    └── requirements.txt          # Python dependencies
```

## 🎯 Key Features & Capabilities

### **Document Intelligence Actions**
1. **📋 Summarization**: Comprehensive document summaries
2. **❓ Question Answering**: Direct answers to specific questions
3. **👥 Entity Extraction**: People, organizations, dates, locations
4. **🌐 Translation**: Multi-language document translation
5. **🏷️ Classification**: Document type classification
6. **💡 Insight Extraction**: Key findings and patterns
7. **😊 Sentiment Analysis**: Tone and emotional analysis
8. **✅ Action Item Detection**: Tasks, deadlines, responsibilities
9. **📊 Document Comparison**: Compare multiple documents
10. **🔍 Information Search**: Find specific information

### **Supported Document Formats**
- **PDF Documents**: Text extraction and analysis
- **Images**: OCR-powered text extraction
- **Word Documents**: .docx and .doc files
- **Excel Files**: .xlsx and .xls spreadsheets
- **CSV Files**: Tabular data processing
- **Text Files**: Plain text and markdown
- **RTF Files**: Rich text format documents

## 🚀 Deployment & Usage

### **Prerequisites**
```bash
# Install Python dependencies
pip install -r document_intelligence/requirements.txt

# Install Tesseract OCR (for image processing)
# macOS: brew install tesseract
# Ubuntu: sudo apt-get install tesseract-ocr
# Windows: Download from GitHub releases

# Configure AWS credentials
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=your_region
```

### **Local Development**
```bash
# Run the Gradio interface
python3 run_gradio.py

# Test the agent
python3 debug_test.py

# Deploy to AWS
python3 deploy.py
```

### **AWS Deployment**
```bash
# Automated deployment using Python script
python3 deploy.py

# Manual deployment using SAM
sam build
sam deploy --guided
```

## 🔍 Testing & Validation

### **Test Scenarios**
1. **Intent Recognition**: Verify agent correctly identifies user intent
2. **Action Execution**: Test all 10+ document intelligence actions
3. **Multi-Format Processing**: Test PDF, image, Word, Excel files
4. **Response Quality**: Validate response accuracy and formatting
5. **Error Handling**: Test edge cases and error scenarios

### **Sample Test Queries**
- "What is this document about?"
- "Who are the key people mentioned?"
- "Extract action items from this document"
- "Translate this to Spanish"
- "What are the main findings?"
- "Analyze the sentiment of this document"

## 🎓 Learning Outcomes

### **Technical Skills Developed**
- **AWS Agent Core**: Understanding of enterprise agent frameworks
- **Serverless Architecture**: Lambda, API Gateway, CloudFormation
- **AI/ML Integration**: Bedrock, Claude 3, prompt engineering
- **Document Processing**: OCR, multi-format text extraction
- **Intent Analysis**: Natural language understanding and classification
- **Python Development**: Advanced Python programming and debugging

### **Project Management Skills**
- **Requirements Analysis**: Understanding complex project requirements
- **Architecture Design**: System design and component integration
- **Testing & Debugging**: Comprehensive testing strategies
- **Documentation**: Technical documentation and user guides
- **Deployment**: Production-ready deployment automation

## 🔮 Future Enhancements

### **Planned Improvements**
1. **Multi-Document Processing**: Handle multiple documents simultaneously
2. **Advanced OCR**: Better image and table recognition
3. **Custom Training**: Fine-tune models for specific domains
4. **Real-time Collaboration**: Multi-user document analysis
5. **API Integration**: Connect with external data sources
6. **Mobile Interface**: Native mobile app development

### **Scalability Considerations**
- **Horizontal Scaling**: Multiple Lambda instances
- **Caching**: Redis for frequently accessed documents
- **Database Integration**: Document storage and retrieval
- **Load Balancing**: Handle high traffic scenarios
- **Monitoring**: CloudWatch integration for performance tracking

## 📞 Support & Contact

For questions about this project or technical implementation details, please refer to the code comments and documentation within each file. The project demonstrates advanced AI agent development using AWS Agent Core and showcases the potential of intelligent document processing systems.

---

**Project Status**: ✅ Complete and Functional  
**Last Updated**: December 2024  
**Framework**: AWS Agent Core  
**AI Model**: Claude 3 Sonnet  
**Deployment**: AWS Lambda + API Gateway 