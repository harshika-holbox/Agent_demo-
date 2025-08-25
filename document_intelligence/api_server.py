#!/usr/bin/env python3
"""
FastAPI Server for CrewAI Document Intelligence Agent
Provides REST API endpoints for AWS Marketplace integration
"""

import os
import base64
import tempfile
import json
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
import boto3
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Import with error handling
try:
    from document_processor import DocumentProcessor
    from crewai_agent_system import DocumentIntelligenceCrew
except ImportError as e:
    print(f"Warning: Could not import some modules: {e}")
    # We'll handle this gracefully in initialization

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global instances (initialized once)
doc_processor = None
crew_agent = None

def initialize_components():
    """Initialize document processor and agent system"""
    global doc_processor, crew_agent
    
    try:
        if doc_processor is None:
            logger.info("Initializing document processor...")
            doc_processor = DocumentProcessor()
        
        if crew_agent is None:
            logger.info("Initializing CrewAI agent system...")
            crew_agent = DocumentIntelligenceCrew()
            
        logger.info("✅ All components initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Error initializing components: {e}")
        raise

# FastAPI app with proper startup event
app = FastAPI(
    title="CrewAI Document Intelligence Agent API",
    description="Advanced document processing with multi-agent AI system using CrewAI, AWS Bedrock Claude 3 Sonnet, and comprehensive document intelligence capabilities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class DocumentProcessRequest(BaseModel):
    """Request model for document processing"""
    input_text: Optional[str] = Field(None, description="Raw text content to process")
    file_content: Optional[str] = Field(None, description="Base64 encoded file content")
    filename: Optional[str] = Field(None, description="Name of the uploaded file")
    user_query: str = Field(..., min_length=1, max_length=1000, description="Query or instruction for the agent")
    
    class Config:
        json_schema_extra = {
            "example": {
                "input_text": "This is a sample document text to analyze...",
                "user_query": "Summarize the key points and extract any action items"
            }
        }

class AgentInfo(BaseModel):
    """Agent information model"""
    crew_type: str
    complexity: str
    agents_used: List[str]

class DocumentProcessResponse(BaseModel):
    """Response model for document processing"""
    status: str = Field(..., description="Processing status")
    agent_response: str = Field(..., description="AI agent's response")
    source: str = Field(..., description="Source of input (text/file)")
    user_query: str = Field(..., description="Original user query")
    agent_info: AgentInfo = Field(..., description="Information about agents used")
    processing_time_ms: int = Field(..., description="Processing time in milliseconds")
    input_length: int = Field(..., description="Length of input text")
    timestamp: str = Field(..., description="Processing timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "agent_response": "Based on my analysis of the document, here are the key findings...",
                "source": "Direct text input",
                "user_query": "Summarize the key points",
                "agent_info": {
                    "crew_type": "summarization",
                    "complexity": "simple",
                    "agents_used": ["Content Summarization Specialist"]
                },
                "processing_time_ms": 2350,
                "input_length": 456,
                "timestamp": "2025-01-07T10:30:00Z"
            }
        }

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: str
    version: str
    components: Dict[str, str]

async def process_document_service(
    input_text: Optional[str] = None,
    file_content: Optional[bytes] = None,
    filename: Optional[str] = None,
    user_query: str = ""
) -> DocumentProcessResponse:
    """Shared service for document processing"""
    start_time = datetime.utcnow()
    
    # Initialize components if not already done
    if not doc_processor or not crew_agent:
        initialize_components()
    
    # Validate input
    if not user_query:
        raise HTTPException(status_code=400, detail="user_query is required")
    
    if not input_text and not (file_content and filename):
        raise HTTPException(status_code=400, detail="Either input_text or (file_content + filename) must be provided")
    
    if input_text:
        validate_text_length(input_text)
    
    if file_content:
        validate_file_size(len(file_content))

    document_content = input_text
    source_info = "Direct text input"
    filename_for_agent = "text_input"
    
    # Handle file content if provided
    if file_content and filename:
        try:
            # Process file to extract text (direct bytes, no base64)
            extracted_text, file_type = doc_processor.process_file(file_content, filename)
            document_content = extracted_text
            source_info = f"File: {filename} ({file_type.upper()})"
            filename_for_agent = filename
            
        except Exception as e:
            logger.error(f"Error processing file content: {e}")
            raise HTTPException(status_code=400, detail=f"Invalid file content: {str(e)}")
    
    if not document_content:
        raise HTTPException(status_code=400, detail="No processable content found in request")

    # Process with intelligent agent
    logger.info(f"Processing request - Query: '{user_query[:100]}...', Input length: {len(document_content)}")
    
    result_data = crew_agent.process_query(user_query, document_content, filename_for_agent)
    
    # Extract the main response
    result = getattr(result_data.get('result'), 'raw', str(result_data.get('result')))
    agents_used = result_data.get('agents_used', ["CrewAI Multi-Agent System"])
    crew_type = result_data.get('crew_type', 'multi_agent_processing')
    complexity = result_data.get('complexity', 'auto_detected')
    
    # Calculate processing time
    end_time = datetime.utcnow()
    processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
    
    agent_info = AgentInfo(
        crew_type=crew_type,
        complexity=complexity, 
        agents_used=agents_used
    )
    
    return DocumentProcessResponse(
        status="success",
        agent_response=result,
        source=source_info,
        user_query=user_query,
        agent_info=agent_info,
        processing_time_ms=processing_time_ms,
        input_length=len(document_content),
        timestamp=end_time.isoformat() + "Z"
    )

# Add these constants near the top of your file
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes
MAX_TEXT_LENGTH = 10000  # characters

# Add this validation function
def validate_file_size(file_size: int, max_size: int = MAX_FILE_SIZE):
    """Validate file size against maximum allowed size"""
    if file_size > max_size:
        raise HTTPException(
            status_code=413,
            detail=f"File size {file_size} bytes exceeds maximum allowed size of {max_size} bytes"
        )
    if file_size == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

def validate_text_length(text: str, max_length: int = MAX_TEXT_LENGTH):
    """Validate text length against maximum allowed length"""
    if text and len(text) > max_length:
        raise HTTPException(
            status_code=413,
            detail=f"Text length {len(text)} characters exceeds maximum allowed length of {max_length} characters"
        )

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        initialize_components()
        logger.info("🚀 CrewAI Document Intelligence Agent API started successfully")
    except Exception as e:
        logger.error(f"❌ Failed to start API: {e}")    
    yield

# Update your FastAPI app initialization
app = FastAPI(
    title="CrewAI Document Intelligence Agent API",
    description="Advanced document processing with multi-agent AI system using CrewAI, AWS Bedrock Claude 3 Sonnet, and comprehensive document intelligence capabilities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan  # Add lifespan handler here
)

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint - health check and info"""
    try:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>CrewAI Document Intelligence Agent</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                .endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }
                .method { color: #0066cc; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 CrewAI Document Intelligence Agent API</h1>
                <p>Advanced document processing with multi-agent AI system</p>
                
                <h2>🔗 Available Endpoints</h2>
                <div class="endpoint">
                    <span class="method">GET</span> <a href="/health">/health</a> - Health check
                </div>
                <div class="endpoint">
                    <span class="method">POST</span> /api/process - Process documents
                </div>
                <div class="endpoint">
                    <span class="method">POST</span> /api/upload - Upload and process files
                </div>
                <div class="endpoint">
                    <span class="method">GET</span> <a href="/api/capabilities">/api/capabilities</a> - Agent capabilities
                </div>
                <div class="endpoint">
                    <span class="method">GET</span> <a href="/docs">/docs</a> - Interactive API documentation
                </div>
                
                <h2>🧪 Quick Test</h2>
                <p>Use curl to test the API:</p>
                <pre style="background: #f0f0f0; padding: 15px; border-radius: 5px;">
curl -X POST http://localhost:7860/api/process \
  -H "Content-Type: application/json" \
  -d '{ 
    "input_text": "This is a test document for analysis.",
    "user_query": "Summarize this document"
  }'</pre>
            </div>
        </body>
        </html>
        """
    except Exception as e:
        logger.error(f"Error serving root endpoint: {e}")
        return HTMLResponse(content=f"<h1>Service Error</h1><p>{str(e)}</p>", status_code=500)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for load balancer"""
    try:
        # Test component availability
        components = {}
        
        # Test document processor
        try:
            if doc_processor:
                components["document_processor"] = "healthy"
            else:
                components["document_processor"] = "not_initialized"
        except Exception as e:
            components["document_processor"] = f"error: {str(e)[:100]}"
        
        # Test CrewAI agent
        try:
            if crew_agent and hasattr(crew_agent, 'agents') and crew_agent.agents:
                components["crewai_agent"] = "healthy"
            else:
                components["crewai_agent"] = "not_initialized"
        except Exception as e:
            components["crewai_agent"] = f"error: {str(e)[:100]}"
        
        # Test AWS Bedrock connection (simple check)
        try:
            session = boto3.Session()
            credentials = session.get_credentials()
            if credentials:
                components["aws_bedrock"] = "credentials_available"
            else:
                components["aws_bedrock"] = "no_credentials"
        except Exception as e:
            components["aws_bedrock"] = f"error: {str(e)[:100]}"
        
        return HealthResponse(
            status="healthy" if all("error" not in status for status in components.values()) else "degraded",
            timestamp=datetime.utcnow().isoformat() + "Z",
            version="1.0.0",
            components=components
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.post("/api/process", response_model=DocumentProcessResponse)
async def process_document(request: DocumentProcessRequest):
    """Process document with CrewAI multi-agent system"""
    try:
        file_content = None
        if request.file_content:
            file_content = base64.b64decode(request.file_content)
        
        return await process_document_service(
            input_text=request.input_text,
            file_content=file_content,
            filename=request.filename,
            user_query=request.user_query
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing document: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal processing error: {str(e)}")

@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    query: str = Form(..., description="Query or instruction for processing the uploaded file")
):
    """Upload and process a file directly"""
    try:
        file_content = await file.read()
        
        return await process_document_service(
            file_content=file_content,
            filename=file.filename,
            user_query=query
        )
        
    except Exception as e:
        logger.error(f"Error in file upload: {e}")
        raise HTTPException(status_code=500, detail=f"File upload error: {str(e)}")

@app.get("/api/capabilities")
async def get_capabilities():
    """
    Get agent capabilities and supported formats
    
    Useful for AWS Marketplace documentation
    """
    try:
        if not doc_processor:
            initialize_components()
        
        capabilities = {
            "agent_type": "CrewAI Multi-Agent System",
            "model": "AWS Bedrock Claude 3 Sonnet",
            "capabilities": [
                "Document Summarization",
                "Question Answering", 
                "Entity Extraction",
                "Language Translation",
                "Document Classification",
                "Sentiment Analysis",
                "Action Item Detection",
                "Information Search",
                "Insight Extraction",
                "Document Comparison"
            ],
            "supported_formats": {
                "pdf": [".pdf"],
                "image": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"],
                "word": [".docx", ".doc"],
                "excel": [".xlsx", ".xls"],
                "csv": [".csv"],
                "text": [".txt", ".md", ".rtf"]
            },
            "features": [
                "Multi-agent collaboration",
                "Smart complexity detection",
                "OCR for images", 
                "Multi-format document processing",
                "Intelligent workflow orchestration",
                "Real-time processing"
            ],
            "limits": {
                "max_file_size": "10MB",
                "max_text_length": "10000 characters",
                "processing_timeout": "300 seconds"
            }
        }
        
        return capabilities
        
    except Exception as e:
        logger.error(f"Error getting capabilities: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting capabilities: {str(e)}")

@app.get("/api/pricing")
async def get_pricing():
    """Get pricing information for AWS Marketplace"""
    return {
        "model": "per-request",
        "base_cost": 0.001,
        "currency": "USD",
        "billing_unit": "request",
        "tiers": [
            {
                "name": "Basic",
                "requests_per_month": 1000,
                "price_per_request": 0.001,
                "features": ["All document formats", "Multi-agent processing", "Basic support"]
            },
            {
                "name": "Professional",
                "requests_per_month": 10000,
                "price_per_request": 0.0008,
                "features": ["Priority processing", "Advanced analytics", "Email support"]
            },
            {
                "name": "Enterprise",
                "requests_per_month": "unlimited",
                "price_per_request": 0.0005,
                "features": ["Custom integrations", "Dedicated support", "SLA guarantee"]
            }
        ]
    }

if __name__ == "__main__":
    # For local development
    uvicorn.run(
        "api_server:app",
        reload=True,
        log_level="info"
    )