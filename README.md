# 🤖 Document Intelligence Agent for AWS Agent Marketplace

An advanced document intelligence agent built with AWS AgentCore that can understand, analyze, and interact with documents in multiple formats. Capable of summarization, Q&A, entity extraction, translation, classification, sentiment analysis, and more using AWS Agent Core and Claude 3 Sonnet.

## What's Been Done

### **Core Implementation:**
- **Document Intelligence Agent** (`document_intelligence/agent_intelligence.py`) - Advanced agent with multiple capabilities
- **Lambda Function** (`document_intelligence/app.py`) - Intelligent agent interface with decision-making
- **Document Processor** (`document_intelligence/document_processor.py`) - Handles PDFs, images, Word docs, Excel files
- **OCR Integration** - Image text extraction using Tesseract
- **AWS Bedrock Integration** - Connected to Claude 3 Sonnet
- **Agent Decision Making** - Automatic intent analysis and action selection
- **Environment Setup** (`.env`) - AWS credentials configured
- **Local Testing** - Function tested and working
- **Error Handling** - Input validation and error responses

### **Configuration Files:**
- **Agent Config** (`agent-config.yaml`) - AgentCore configuration ready
- **SAM Template** (`template.yaml`) - AWS deployment template
- **Dependencies** (`requirements.txt`) - Python packages defined

### **Testing Results:**
- **Agent Intelligence** - Successfully analyzes user intent and chooses appropriate actions
- **Multi-Modal Processing** - Handles text, PDFs, images, Word docs, Excel files
- **Document Q&A** - Answers questions about document content
- **Entity Extraction** - Finds people, organizations, dates, locations
- **Document Translation** - Translates content to multiple languages
- **Document Classification** - Automatically categorizes document types
- **Sentiment Analysis** - Analyzes document tone and sentiment
- **Action Item Extraction** - Finds tasks, deadlines, and responsibilities
- **Large Input** - Processes 25,000+ character texts
- **Error Cases** - Validates input and returns proper errors

## Project Structure

```
DOCUMENT_INTELLIGENCE_AGENT/
├── .env                          # AWS credentials (configured)
├── agent-config.yaml             # AgentCore config (ready)
├── template.yaml                 # SAM deployment template
├── deploy.py                     # Python deployment script
├── run_gradio.py                 # Gradio interface launcher
├── test_function.py              # Test script (working)
└── document_intelligence/
    ├── app.py                    # Lambda function + Gradio interface
    ├── agent_intelligence.py     # Advanced document intelligence agent
    ├── document_processor.py     # Multi-format document processor
    └── requirements.txt          # Dependencies
```

## Next Steps

### **1. Test with Gradio Interface (Local Testing)**
```bash
# Install Python dependencies
pip install -r document_intelligence/requirements.txt

# Install Tesseract OCR (required for image text extraction)
# macOS: brew install tesseract
# Ubuntu/Debian: sudo apt-get install tesseract-ocr
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki

# Set up AWS credentials (create .env file or export variables)
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=your_region

# Run the Gradio interface
python run_gradio.py
```

The Gradio interface will be available at: http://localhost:7860

**Supported File Formats:**
- **PDFs**: .pdf
- **Images**: .png, .jpg, .jpeg, .gif, .bmp, .tiff, .webp
- **Word Documents**: .docx, .doc
- **Excel Files**: .xlsx, .xls
- **Data Files**: .csv
- **Text Files**: .txt, .md, .rtf

**Agent Capabilities:**
- **Smart Summarization**: Intelligent document summaries
- **Document Q&A**: Ask questions about your documents
- **Entity Extraction**: Find people, organizations, dates, locations
- **Document Translation**: Translate content to multiple languages
- **Document Classification**: Automatically categorize documents
- **Insight Extraction**: Find key insights and patterns
- **Sentiment Analysis**: Analyze document tone and sentiment
- **Action Item Extraction**: Find tasks, deadlines, and responsibilities
- **Information Search**: Find specific information in documents

### **2. Deploy to AWS (Production)**
```bash
python3 deploy.py
```

### **2. Update Configuration**
After deployment, update `agent-config.yaml`:
- Replace `REGION` and `ACCOUNT_ID` with actual values
- Update support email and documentation URL

### **3. Test Deployed Function**
```bash
curl -X POST https://your-api-gateway-url/Prod/summarize \
  -H "Content-Type: application/json" \
  -d '{"input": "Your text to summarize..."}'
```

### **4. Submit to Agent Marketplace**
- Package all files
- Submit through AWS Agent Marketplace console
- Set pricing and availability

## Costs
- **Lambda:** ~$0.20 per 1M requests
- **Bedrock:** ~$0.003 per 1K input tokens
- **API Gateway:** ~$3.50 per 1M requests
- **Document Processing:** Included in Lambda execution time
- **OCR Processing:** Included in Lambda execution time

## Current Status
- **Function:** Working locally
- **AWS Integration:** Credentials configured
- **Testing:** All tests passing
- **Deployment:** Ready to deploy
- **Marketplace:** Ready to submit

**Ready for deployment!** 