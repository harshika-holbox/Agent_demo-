# Multi-Format Document Summarization Agent for AWS Agent Marketplace

A comprehensive document summarization agent built with AWS AgentCore that creates concise summaries from PDFs, images, Word docs, Excel files, and text content using Amazon Bedrock, Claude 3 Sonnet, and OCR technology.

## What's Been Done

### **Core Implementation:**
- **Lambda Function** (`summarizer/app.py`) - Working summarization logic with multi-format support
- **Document Processor** (`summarizer/document_processor.py`) - Handles PDFs, images, Word docs, Excel files
- **OCR Integration** - Image text extraction using Tesseract
- **AWS Bedrock Integration** - Connected to Claude 3 Sonnet
- **Environment Setup** (`.env`) - AWS credentials configured
- **Local Testing** - Function tested and working
- **Error Handling** - Input validation and error responses

### **Configuration Files:**
- **Agent Config** (`agent-config.yaml`) - AgentCore configuration ready
- **SAM Template** (`template.yaml`) - AWS deployment template
- **Dependencies** (`requirements.txt`) - Python packages defined

### **Testing Results:**
- **Main Function** - Successfully generates summaries from text and files
- **PDF Processing** - Extracts and summarizes PDF documents
- **Image OCR** - Extracts text from images and summarizes
- **Office Documents** - Processes Word and Excel files
- **Empty Input** - Properly handles empty requests
- **Large Input** - Processes 25,000+ character texts
- **Error Cases** - Validates input and returns proper errors

## Project Structure

```
SUMMARIZATION_AGENT/
├── .env                          # AWS credentials (configured)
├── agent-config.yaml             # AgentCore config (ready)
├── template.yaml                 # SAM deployment template
├── deploy.sh                     # Deployment script
├── run_gradio.py                 # Gradio interface launcher
├── test_function.py              # Test script (working)
└── summarizer/
    ├── app.py                    # Lambda function + Gradio interface
    ├── document_processor.py     # Multi-format document processor
    └── requirements.txt          # Dependencies
```

## Next Steps

### **1. Test with Gradio Interface (Local Testing)**
```bash
# Install Python dependencies
pip install -r summarizer/requirements.txt

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

### **2. Deploy to AWS (Production)**
```bash
chmod +x deploy.sh
./deploy.sh
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