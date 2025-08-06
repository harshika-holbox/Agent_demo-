# 🤖 AWS Agent Core - Document Intelligence Agent

## 📋 Project Overview

This project demonstrates the development of an **intelligent document processing agent** using **AWS Agent Core** framework, designed to showcase advanced AI capabilities beyond simple summarization. The agent can understand user intent, process multiple document formats, and perform intelligent analysis based on natural language queries.

## 🎯 What I Did in This Project

### 1. **CrewAI Multi-Agent Architecture Design**
- Designed a sophisticated multi-agent document intelligence system using CrewAI
- Implemented smart complexity detection that automatically chooses optimal processing approach
- Created specialized agent teams with specific expertise for different document tasks
- Built intelligent workflow orchestration that coordinates multiple agents for complex analysis

### 2. **Advanced Document Processing Capabilities**
- **Multi-Format Support**: PDF, Images (with OCR), Word documents, Excel files, CSV, Text files
- **Smart Complexity Detection**: Automatically detects query complexity and chooses optimal processing
- **Multi-Agent Collaboration**: Specialized agents work together for comprehensive analysis

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
- **CrewAI Framework**: Multi-agent orchestration and collaboration system
- **Serverless Architecture**: Deployed using AWS Lambda and API Gateway
- **Gradio Web Interface**: User-friendly web UI for testing and demonstration
- **Python Deployment Scripts**: Automated deployment and configuration management

### 5. **Quality Assurance & Testing**
- Comprehensive debugging and testing framework
- Multi-agent collaboration validation and optimization
- Response formatting and error handling
- Multi-format document processing validation
- Complexity detection accuracy testing

## 🚀 What Makes This Agent Different from Other Tools

### **1. Smart Complexity Detection & Multi-Agent Collaboration**
Unlike traditional summarization tools that only provide summaries, this system:
- **Automatic Complexity Detection**: Analyzes query complexity and document length to choose optimal processing
- **Specialized Agent Teams**: Uses expert agents for specific tasks (summarization, entity extraction, Q&A, etc.)
- **Intelligent Workflow Orchestration**: Coordinates multiple agents for comprehensive analysis
- **Natural Language Understanding**: Processes queries like "Who are the key people mentioned?" or "What are the main findings?"

### **2. Multi-Capability Framework**
Most document tools are single-purpose. This system provides:
- **10+ Different Capabilities** in one unified interface
- **Seamless Switching** between different analysis types
- **Comprehensive Document Intelligence** beyond just text processing
- **Specialized Agent Expertise** for each capability

### **3. AWS Agent Core + CrewAI Integration**
- **Enterprise-Grade Framework**: Built on AWS's official agent framework
- **Multi-Agent Orchestration**: CrewAI provides sophisticated agent collaboration
- **Scalable Architecture**: Can handle multiple users and large documents
- **Professional Deployment**: Ready for production use in enterprise environments
- **Agent Collaboration**: Agents collaborate using the "Ask question to coworker" tool for all teamwork. The "Delegate work to coworker" tool is disabled due to CrewAI's internal bug (see below).

### **4. Advanced Document Processing**
- **OCR Integration**: Can extract text from images and scanned documents
- **Multi-Format Support**: Handles PDFs, Word docs, Excel files, images, etc.
- **Structured Data Extraction**: Can extract tables, charts, and formatted data

### **5. Intelligent Response Formatting**
- **Action-Specific Responses**: Different response formats for different actions
- **Structured Output**: Organized, readable responses with clear sections
- **Multi-Agent Insights**: Shows which agents participated and their contributions
- **Complexity Analysis**: Displays processing approach and optimization details

## 🏗️ Technical Architecture

### **Framework: AWS Agent Core + CrewAI**
- **Purpose**: AWS's official framework combined with CrewAI for building sophisticated multi-agent systems
- **Benefits**: Enterprise-grade scalability, security, and advanced multi-agent collaboration
- **Components**: 
  - **Agent Configuration**: Defines agent behavior, capabilities, and instructions
  - **CrewAI Multi-Agent System**: Specialized agents with specific expertise
  - **Smart Complexity Detection**: Automatic optimization of processing approach
  - **Action Groups**: Modular functions that agents can execute
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
- **CrewAI Multi-Agent System**: Specialized agents for different document tasks
- **Smart Complexity Detection**: Automatic analysis of query and document complexity
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
│ • File Upload   │───▶│ • Agent         │───▶│ • CrewAI        │───▶│ • Claude 3      │
│ • Query Input   │    │   Configuration │    │   Multi-Agent   │    │   Sonnet        │
│ • Response      │    │ • Action Groups │    │   System        │    │ • Document      │
│   Display       │    │ • API Schema    │    │ • Complexity    │    │   Processing    │
└─────────────────┘    └─────────────────┘    │   Detection     │    └─────────────────┘
         │                       │            │ • Agent         │              │
         │                       │            │   Orchestration │              │
         │                       │            └─────────────────┘              │
         │                       │                       │                     │
         │                       │                       ▼                     │
         │                       │              ┌─────────────────┐            │
         │                       │              │ Document        │            │
         └───────────────────────┼──────────────▶│ Processor       │◀───────────┘
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

### **1. Smart Complexity Detection System**
```python
def _analyze_query_complexity(self, user_query: str, document_content: str) -> str:
    """Analyze query complexity to determine processing approach"""
    query_lower = user_query.lower()
    doc_length = len(document_content)
    
    # Simple queries (fast processing)
    simple_keywords = ['summarize', 'summary', 'translate', 'classify']
    complex_keywords = ['analyze', 'compare', 'insights', 'comprehensive', 'detailed']
    
    # Check for simple vs complex patterns
    if any(word in query_lower for word in simple_keywords) and doc_length < 2000:
        return "simple"
    elif any(word in query_lower for word in complex_keywords) or doc_length > 5000:
        return "complex"
    else:
        return "moderate"
```

### **2. Multi-Agent Crew Creation**
```python
def create_summarization_crew(self, document_content: str) -> Crew:
    """Create a crew for document summarization"""
    
    # Task 1: Initial document analysis
    analyze_task = Task(
        description="Analyze document structure and key themes",
        agent=self.agents["analyzer"],
        expected_output="Detailed document analysis"
    )
    
    # Task 2: Create comprehensive summary
    summarize_task = Task(
        description="Create comprehensive summary based on analysis",
        agent=self.agents["summarizer"],
        expected_output="Comprehensive document summary",
        context=[analyze_task]
    )
    
    return Crew(
        agents=[self.agents["analyzer"], self.agents["summarizer"]],
        tasks=[analyze_task, summarize_task],
        process=Process.sequential,
        verbose=True
    )
```

### **3. Specialized Agent Creation**
```python
def _create_agents(self) -> Dict[str, Agent]:
    """Create specialized agents for different document processing tasks"""
    
    # Document Analysis Coordinator - Main coordinator
    document_analyzer = Agent(
        role="Document Analysis Coordinator",
        goal="Coordinate document analysis tasks and ensure comprehensive understanding",
        backstory="Expert document analysis coordinator with years of experience...",
        verbose=True,
        allow_delegation=True,
        tools=[self.bedrock_tool],
        llm=self.bedrock_tool
    )
    
    # Content Summarization Specialist
    content_summarizer = Agent(
        role="Content Summarization Specialist",
        goal="Create comprehensive, accurate summaries of document content",
        backstory="Specialized content summarization expert with deep expertise...",
        verbose=True,
        tools=[self.bedrock_tool],
        llm=self.bedrock_tool
    )
    
    # ... more specialized agents
```

### **4. Multi-Agent Processing with Complexity Detection**
```python
def process_query(self, user_query: str, document_content: str) -> Dict[str, Any]:
    """Main method to process user query using CrewAI agents with smart complexity detection"""
    
    # Analyze query complexity
    complexity = self._analyze_query_complexity(user_query, document_content)
    
    if complexity == "simple":
        # Use simple crew for fast processing
        crew = self.create_simple_summarization_crew(document_content)
        agents_used = ["Content Summarization Specialist"]
    else:
        # Use comprehensive crew for complex documents
        crew = self.create_summarization_crew(document_content)
        agents_used = ["Document Analysis Coordinator", "Content Summarization Specialist"]
    
    result = crew.kickoff()
    
    return {
        "user_query": user_query,
        "crew_type": "summarization",
        "complexity": complexity,
        "result": result,
        "agents_used": agents_used
    }
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
    ├── crewai_agent_system.py    # CrewAI multi-agent system with smart complexity detection
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
1. **Complexity Detection**: Verify system correctly detects query complexity
2. **Multi-Agent Collaboration**: Test agent coordination and task delegation
3. **Action Execution**: Test all 10+ document intelligence actions
4. **Multi-Format Processing**: Test PDF, image, Word, Excel files
5. **Response Quality**: Validate response accuracy and formatting
6. **Error Handling**: Test edge cases and error scenarios

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
- **CrewAI Framework**: Multi-agent orchestration and collaboration
- **Serverless Architecture**: Lambda, API Gateway, CloudFormation
- **AI/ML Integration**: Bedrock, Claude 3, prompt engineering
- **Document Processing**: OCR, multi-format text extraction
- **Multi-Agent Systems**: Agent specialization and workflow orchestration
- **Complexity Detection**: Intelligent query analysis and optimization
- **Python Development**: Advanced Python programming and debugging

### **Project Management Skills**
- **Requirements Analysis**: Understanding complex project requirements
- **Architecture Design**: Multi-agent system design and component integration
- **Testing & Debugging**: Comprehensive testing strategies for multi-agent systems
- **Documentation**: Technical documentation and user guides
- **Deployment**: Production-ready deployment automation

## 🔮 Future Enhancements

### **Planned Improvements**
1. **Advanced Multi-Agent Orchestration**: Dynamic agent creation and task delegation
2. **Multi-Document Processing**: Handle multiple documents simultaneously
3. **Advanced OCR**: Better image and table recognition
4. **Custom Training**: Fine-tune models for specific domains
5. **Real-time Collaboration**: Multi-user document analysis
6. **API Integration**: Connect with external data sources
7. **Mobile Interface**: Native mobile app development
8. **Agent Learning**: Agents that improve based on feedback and usage patterns

### **Scalability Considerations**
- **Horizontal Scaling**: Multiple Lambda instances
- **Agent Pool Management**: Dynamic agent allocation and scaling
- **Caching**: Redis for frequently accessed documents
- **Database Integration**: Document storage and retrieval
- **Load Balancing**: Handle high traffic scenarios
- **Monitoring**: CloudWatch integration for performance tracking
- **Multi-Agent Optimization**: Efficient agent coordination and resource allocation

## 📞 Support & Contact

For questions about this project or technical implementation details, please refer to the code comments and documentation within each file. The project demonstrates advanced AI agent development using AWS Agent Core and showcases the potential of intelligent document processing systems.

---

**Project Status**: ✅ Complete and Functional  
**Last Updated**: December 2024  
**Framework**: AWS Agent Core + CrewAI  
**AI Model**: Claude 3 Sonnet  
**Architecture**: Multi-Agent System with Smart Complexity Detection  
**Deployment**: AWS Lambda + API Gateway 

### **Agent Collaboration: 'Ask question to coworker' Only**

By design, CrewAI provides two main ways for agents to collaborate:
- **Ask question to coworker**: One agent asks another for help or clarification.
- **Delegate work to coworker**: One agent delegates a sub-task to another.

**In this project, we use only "Ask question to coworker" for all agent collaboration.**
- The "Delegate work to coworker" tool was disabled because it caused errors in CrewAI (related to argument handling).
- This ensures smooth, reliable teamwork between agents for all complex document tasks.

**How agents work together:**
- The Document Analysis Coordinator breaks down complex queries and asks specialists (summarizer, Q&A, entity extraction, etc.) for their input using "Ask question to coworker".
- All collaboration is question-based, not delegation-based, for maximum reliability.

### **Known CrewAI Issue: Why 'Delegate work to coworker' is Disabled**
- CrewAI's "Delegate work to coworker" tool currently has a bug: it expects arguments as separate strings, but sometimes receives a dictionary, causing errors like `unhashable type: 'dict'`.
- To avoid this, we removed `allow_delegation=True` from all agent definitions and updated agent backstories to instruct them to use only "Ask question to coworker".
- This workaround is robust and recommended until CrewAI fixes the bug.

### **Agent Roles in the CrewAI System**
- **Document Analysis Coordinator**: Orchestrates the workflow, breaks down complex queries, and coordinates with specialists.
- **Content Summarization Specialist**: Creates summaries in the requested language.
- **Entity Extraction Specialist**: Extracts people, organizations, dates, and locations.
- **Document Q&A Specialist**: Answers user questions about the document.
- **Sentiment Analysis Specialist**: Analyzes tone and sentiment.
- **Document Translation Specialist**: Translates content to/from multiple languages.
- **Action Item Extraction Specialist**: Finds tasks, deadlines, and responsibilities.
- **Document Classification Specialist**: Categorizes document types.

**All agents collaborate using "Ask question to coworker" for teamwork.** 