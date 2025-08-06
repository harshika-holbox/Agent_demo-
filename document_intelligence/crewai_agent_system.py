import os
import json
import boto3
from typing import Dict, Any, List
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from document_processor import DocumentProcessor
import litellm

class DocumentIntelligenceCrew:
    """
    Unified Document Intelligence System using CrewAI - handles both simple and complex tasks
    """
    
    def __init__(self):
        # Configure litellm for AWS Bedrock
        litellm.set_verbose = False
        self.bedrock_llm = litellm.completion(
            model="bedrock/anthropic.claude-3-sonnet-20240229-v1:0",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=10,
            temperature=0.1
        )
        self.doc_processor = DocumentProcessor()
        self.agents = self._create_agents()
        
    def _create_agents(self) -> Dict[str, Agent]:
        """Create specialized agents for different document processing tasks"""
        
        # Document Analyzer Agent - Main coordinator
        document_analyzer = Agent(
            role="Document Analysis Coordinator",
            goal="Coordinate document analysis tasks and ensure comprehensive understanding",
            backstory="""You are an expert document analysis coordinator with years of experience
            in understanding complex documents and coordinating specialized analysis teams.
            You excel at breaking down complex document analysis requests into manageable tasks
            and ensuring all aspects are thoroughly covered.

            IMPORTANT: When you need help from a coworker, always use the 'Ask question to coworker' tool.
            Do NOT use 'Delegate work to coworker'.
            Formulate your request as a clear question and send it to the appropriate specialist.
            """,
            verbose=True,
            tools=[],
            llm="bedrock/anthropic.claude-3-sonnet-20240229-v1:0"
        )
        
        # Content Summarizer Agent
        content_summarizer = Agent(
            role="Content Summarization Specialist",
            goal="Create comprehensive, accurate summaries of document content",
            backstory="""You are a specialized content summarization expert with deep expertise 
            in distilling complex information into clear, concise summaries. You understand 
            the importance of maintaining key details while making content accessible and 
            actionable for different audiences.""",
            verbose=True,
            tools=[],
            llm="bedrock/anthropic.claude-3-sonnet-20240229-v1:0"
        )
        
        # Entity Extraction Agent
        entity_extractor = Agent(
            role="Entity Extraction Specialist",
            goal="Extract and categorize named entities from documents with high accuracy",
            backstory="""You are an expert in named entity recognition and extraction. 
            You have extensive experience identifying people, organizations, locations, 
            dates, and other important entities from various document types. Your 
            precision and attention to detail ensure no important entities are missed.""",
            verbose=True,
            tools=[],
            llm="bedrock/anthropic.claude-3-sonnet-20240229-v1:0"
        )
        
        # Question Answering Agent
        question_answerer = Agent(
            role="Document Q&A Specialist",
            goal="Answer specific questions about document content with high accuracy",
            backstory="""You are a specialized question-answering expert who excels at 
            understanding complex queries and finding precise answers within document content. 
            You have a deep understanding of various document types and can provide 
            contextually relevant, accurate responses to user questions.""",
            verbose=True,
            tools=[],
            llm="bedrock/anthropic.claude-3-sonnet-20240229-v1:0"
        )
        
        # Sentiment Analysis Agent
        sentiment_analyzer = Agent(
            role="Sentiment Analysis Specialist",
            goal="Analyze document tone, sentiment, and emotional content",
            backstory="""You are an expert in sentiment analysis and tone detection. 
            You can identify subtle emotional nuances, writing styles, and underlying 
            attitudes in document content. Your analysis helps understand the context 
            and implications of document communication.""",
            verbose=True,
            tools=[],
            llm="bedrock/anthropic.claude-3-sonnet-20240229-v1:0"
        )
        
        # Translation Agent
        translator = Agent(
            role="Document Translation Specialist",
            goal="Translate document content while preserving meaning and context",
            backstory="""You are a professional translator with expertise in multiple 
            languages and document types. You understand the importance of maintaining 
            the original meaning, tone, and context while making content accessible 
            to different language speakers.""",
            verbose=True,
            tools=[],
            llm="bedrock/anthropic.claude-3-sonnet-20240229-v1:0"
        )
        
        # Action Item Extractor Agent
        action_extractor = Agent(
            role="Action Item Extraction Specialist",
            goal="Identify and extract action items, tasks, and responsibilities from documents",
            backstory="""You are an expert in identifying actionable content within documents. 
            You excel at finding tasks, deadlines, responsibilities, and recommendations 
            that require follow-up action. Your analysis helps teams understand what 
            needs to be done and by whom.""",
            verbose=True,
            tools=[],
            llm="bedrock/anthropic.claude-3-sonnet-20240229-v1:0"
        )
        
        # Document Classifier Agent
        document_classifier = Agent(
            role="Document Classification Specialist",
            goal="Classify documents by type, purpose, and category",
            backstory="""You are an expert in document classification and categorization. 
            You can identify document types, purposes, and appropriate categories based 
            on content, structure, and context. Your classification helps organize 
            and understand document collections.""",
            verbose=True,
            tools=[],
            llm="bedrock/anthropic.claude-3-sonnet-20240229-v1:0"
        )
        
        return {
            "analyzer": document_analyzer,
            "summarizer": content_summarizer,
            "entity_extractor": entity_extractor,
            "question_answerer": question_answerer,
            "sentiment_analyzer": sentiment_analyzer,
            "translator": translator,
            "action_extractor": action_extractor,
            "classifier": document_classifier
        }
    
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
    
    def create_simple_summarization_crew(self, document_content: str, summary_language: str = None) -> Crew:
        """Create a simple crew for basic summarization (fast processing)"""
        summary_instruction = f"Create a concise summary of the following document:"
        if summary_language and summary_language.lower() != "english":
            summary_instruction = f"Create a concise summary of the following document in {summary_language}:"
        summarize_task = Task(
            description=f"""
            {summary_instruction}
            
            Document Content:
            {document_content[:4000]}
            
            Provide a clear, brief summary that captures the main points.""",
            agent=self.agents["summarizer"],
            expected_output=f"Concise document summary in {summary_language or 'English'}"
        )
        return Crew(
            agents=[self.agents["summarizer"]],
            tasks=[summarize_task],
            process=Process.sequential,
            verbose=False
        )
    
    def create_simple_qa_crew(self, document_content: str, question: str, concise: bool = False) -> Crew:
        """Create a simple crew for basic Q&A (fast processing)"""
        if concise:
            answer_instruction = "Provide a brief but informative answer (2-4 sentences or a short bullet list). Focus only on what the user is asking."
        else:
            answer_instruction = "Provide a focused, relevant answer that directly addresses the user's question. Avoid unnecessary detail or excessive length."
        answer_task = Task(
            description=f"""
            Answer the following question about the document:
            
            Question: {question}
            
            Document Content:
            {document_content[:4000]}
            
            {answer_instruction}
            """,
            agent=self.agents["question_answerer"],
            expected_output="Concise, focused answer to the question"
        )
        return Crew(
            agents=[self.agents["question_answerer"]],
            tasks=[answer_task],
            process=Process.sequential,
            verbose=False
        )
    
    def create_simple_entity_extraction_crew(self, document_content: str) -> Crew:
        """Create a simple crew for basic entity extraction (fast processing)"""
        
        # Single task for simple entity extraction
        extract_task = Task(
            description=f"""
            Extract key entities from the document:
            
            Document Content:
            {document_content[:4000]}
            
            Extract people, organizations, dates, and locations in a simple format.
            """,
            agent=self.agents["entity_extractor"],
            expected_output="Simple list of extracted entities"
        )
        
        return Crew(
            agents=[self.agents["entity_extractor"]],
            tasks=[extract_task],
            process=Process.sequential,
            verbose=False
        )
    
    def create_summarization_crew(self, document_content: str, summary_language: str = None) -> Crew:
        """Create a comprehensive crew for detailed summarization"""
        
        # Task 1: Initial document analysis
        analyze_task = Task(
            description=f"""
            Analyze the following document to understand its structure, key themes, and main points:
            
            Document Content:
            {document_content[:4000]}
            
            Provide a comprehensive analysis including:
            1. Document type and purpose
            2. Main themes and topics
            3. Key sections and structure
            4. Important findings or conclusions
            5. Target audience
            """,
            agent=self.agents["analyzer"],
            expected_output="Detailed document analysis with structure and key themes identified"
        )
        
        # Task 2: Create comprehensive summary
        summary_instruction = "Based on the document analysis, create a comprehensive summary of the document."
        if summary_language and summary_language.lower() != "english":
            summary_instruction = f"Based on the document analysis, create a comprehensive summary of the document in {summary_language}."
        summarize_task = Task(
            description=f"""
            {summary_instruction}
            
            Document Content:
            {document_content[:4000]}
            
            Provide a detailed, well-structured summary that covers all key points and findings.""",
            agent=self.agents["summarizer"],
            expected_output=f"Comprehensive document summary in {summary_language or 'English'}"
        )
        
        return Crew(
            agents=[self.agents["analyzer"], self.agents["summarizer"]],
            tasks=[analyze_task, summarize_task],
            process=Process.sequential,
            verbose=True
        )
    
    def create_qa_crew(self, document_content: str, question: str, concise: bool = False) -> Crew:
        """Create a comprehensive crew for detailed Q&A"""
        # Task 1: Analyze the question and document
        analysis_task = Task(
            description=f"""
            Analyze the following document and the user's question to understand the context and what is being asked:
            
            Question: {question}
            
            Document Content:
            {document_content[:4000]}
            
            Identify the key information needed to answer the question accurately and concisely.
            """,
            agent=self.agents["analyzer"],
            expected_output="Key information and context for answering the question"
        )
        # Task 2: Answer the question
        if concise:
            answer_instruction = "Provide a brief but informative answer (2-4 sentences or a short bullet list). Focus only on what the user is asking."
        else:
            answer_instruction = "Provide a focused, relevant answer that directly addresses the user's question. Avoid unnecessary detail or excessive length."
        answer_task = Task(
            description=f"""
            Based on the analysis, answer the user's question:
            
            Question: {question}
            
            Document Content:
            {document_content[:4000]}
            
            {answer_instruction}
            """,
            agent=self.agents["question_answerer"],
            expected_output="Concise, focused answer to the question"
        )
        return Crew(
            agents=[self.agents["analyzer"], self.agents["question_answerer"]],
            tasks=[analysis_task, answer_task],
            process=Process.sequential,
            verbose=True
        )
    
    def create_entity_extraction_crew(self, document_content: str, entity_types: List[str] = None) -> Crew:
        """Create a comprehensive crew for detailed entity extraction"""
        
        if entity_types is None:
            entity_types = ["PERSON", "ORGANIZATION", "DATE", "LOCATION"]
        
        # Task 1: Analyze document for entity extraction
        analysis_task = Task(
            description=f"""
            Analyze the document to identify potential entities for extraction:
            
            Document Content:
            {document_content[:4000]}
            
            Entity types to focus on: {', '.join(entity_types)}
            
            Identify:
            1. Potential entities in the document
            2. Context around each entity
            3. Relationships between entities
            4. Any ambiguous or unclear entities
            """,
            agent=self.agents["analyzer"],
            expected_output="Analysis of potential entities in the document"
        )
        
        # Task 2: Extract entities
        extraction_task = Task(
            description=f"""
            Extract named entities from the document with high accuracy.
            
            Document Content:
            {document_content[:6000]}
            
            Entity types to extract: {', '.join(entity_types)}
            
            Extract entities and return them in this JSON format:
            {{
                "people": ["Full Name 1", "Full Name 2"],
                "organizations": ["Organization Name 1", "Organization Name 2"],
                "dates": ["Date 1", "Date 2"],
                "locations": ["Location 1", "Location 2"]
            }}
            
            Guidelines:
            1. Be precise and avoid duplicates
            2. Include full names and titles when available
            3. Only extract entities clearly mentioned in the document
            4. Provide context for important entities
            """,
            agent=self.agents["entity_extractor"],
            expected_output="Structured entity extraction results in JSON format",
            context=[analysis_task]
        )
        
        return Crew(
            agents=[self.agents["analyzer"], self.agents["entity_extractor"]],
            tasks=[analysis_task, extraction_task],
            process=Process.sequential,
            verbose=True
        )
    
    def create_comprehensive_analysis_crew(self, document_content: str) -> Crew:
        """Create a crew for comprehensive document analysis"""
        
        # Task 1: Document classification
        classify_task = Task(
            description=f"""
            Classify the document by type, purpose, and category.
            
            Document Content:
            {document_content[:4000]}
            
            Provide classification for:
            1. Document type (e.g., report, letter, manual, etc.)
            2. Purpose and intent
            3. Target audience
            4. Industry or domain
            5. Confidence level in classification
            """,
            agent=self.agents["classifier"],
            expected_output="Document classification with type, purpose, and audience"
        )
        
        # Task 2: Sentiment analysis
        sentiment_task = Task(
            description=f"""
            Analyze the sentiment, tone, and emotional content of the document.
            
            Document Content:
            {document_content[:6000]}
            
            Analyze:
            1. Overall sentiment (positive/negative/neutral)
            2. Tone and writing style
            3. Emotional content and implications
            4. Author's attitude and perspective
            5. Potential biases or subjective elements
            """,
            agent=self.agents["sentiment_analyzer"],
            expected_output="Comprehensive sentiment and tone analysis"
        )
        
        # Task 3: Action item extraction
        action_task = Task(
            description=f"""
            Extract action items, tasks, and responsibilities from the document.
            
            Document Content:
            {document_content[:6000]}
            
            Identify:
            1. Action items and tasks
            2. Deadlines and due dates
            3. Responsible parties
            4. Priority levels
            5. Dependencies between tasks
            6. Recommendations and suggestions
            """,
            agent=self.agents["action_extractor"],
            expected_output="Comprehensive list of action items and responsibilities"
        )
        
        # Task 4: Synthesize comprehensive analysis
        synthesis_task = Task(
            description=f"""
            Synthesize all the analysis results into a comprehensive document report.
            
            Combine the results from:
            1. Document classification
            2. Sentiment analysis
            3. Action item extraction
            
            Create a comprehensive report that includes:
            1. Executive summary
            2. Document overview and classification
            3. Key findings and insights
            4. Sentiment and tone analysis
            5. Action items and recommendations
            6. Overall assessment and implications
            """,
            agent=self.agents["analyzer"],
            expected_output="Comprehensive document analysis report",
            context=[classify_task, sentiment_task, action_task]
        )
        
        return Crew(
            agents=[self.agents["classifier"], self.agents["sentiment_analyzer"], 
                   self.agents["action_extractor"], self.agents["analyzer"]],
            tasks=[classify_task, sentiment_task, action_task, synthesis_task],
            process=Process.sequential,
            verbose=True
        )
    
    def process_query(self, user_query: str, document_content: str, document_id: str = "") -> Dict[str, Any]:
        """
        Main method to process user query using CrewAI agents with smart complexity detection
        """
        try:
            print(f"CrewAI Processing query: '{user_query}'")
            print(f"Document content length: {len(document_content)} characters")
            
            # Analyze query complexity
            complexity = self._analyze_query_complexity(user_query, document_content)
            print(f"Query complexity: {complexity}")
            
            # Determine the type of processing needed based on user query
            query_lower = user_query.lower()

            # Detect language request in summarization
            language_map = {
                "french": "French",
                "spanish": "Spanish",
                "german": "German",
                "chinese": "Chinese",
                "japanese": "Japanese"
            }
            requested_language = None
            for lang_key, lang_val in language_map.items():
                if f"in {lang_key}" in query_lower or f"to {lang_key}" in query_lower:
                    requested_language = lang_val
                    break

            # Detect conciseness request in Q&A
            concise_request = any(word in user_query.lower() for word in ['concise', 'short', 'brief', 'summary', 'summarize', 'in a few sentences', 'not too long'])

            if any(word in query_lower for word in ['summarize', 'summary', 'overview']):
                if complexity == "simple":
                    crew = self.create_simple_summarization_crew(document_content, requested_language)
                    result = crew.kickoff()
                    agents_used = ["Content Summarization Specialist"]
                else:
                    crew = self.create_summarization_crew(document_content, requested_language)
                    result = crew.kickoff()
                    agents_used = ["Document Analysis Coordinator", "Content Summarization Specialist"]
                return {
                    "user_query": user_query,
                    "crew_type": "summarization",
                    "complexity": complexity,
                    "result": result,
                    "agents_used": agents_used,
                    "summary_language": requested_language or "English"
                }
                
            elif any(word in query_lower for word in ['who', 'what', 'when', 'where', 'why', 'how', 'question']):
                if complexity == "simple":
                    crew = self.create_simple_qa_crew(document_content, user_query, concise_request)
                    result = crew.kickoff()
                    agents_used = ["Document Q&A Specialist"]
                else:
                    crew = self.create_qa_crew(document_content, user_query, concise_request)
                    result = crew.kickoff()
                    agents_used = ["Document Analysis Coordinator", "Document Q&A Specialist"]
                
                return {
                    "user_query": user_query,
                    "crew_type": "question_answering",
                    "complexity": complexity,
                    "result": result,
                    "agents_used": agents_used
                }
                
            elif any(word in query_lower for word in ['person', 'people', 'organization', 'company', 'date', 'location', 'entity']):
                if complexity == "simple":
                    # Use simple entity extraction for fast processing
                    crew = self.create_simple_entity_extraction_crew(document_content)
                    result = crew.kickoff()
                    agents_used = ["Entity Extraction Specialist"]
                else:
                    # Use comprehensive entity extraction for complex documents
                    crew = self.create_entity_extraction_crew(document_content)
                    result = crew.kickoff()
                    agents_used = ["Document Analysis Coordinator", "Entity Extraction Specialist"]
                
                return {
                    "user_query": user_query,
                    "crew_type": "entity_extraction",
                    "complexity": complexity,
                    "result": result,
                    "agents_used": agents_used
                }
                
            elif any(word in query_lower for word in ['translate', 'spanish', 'french', 'german', 'chinese', 'japanese']):
                # Translation is always simple (single agent)
                target_lang = "Spanish"
                if "french" in query_lower:
                    target_lang = "French"
                elif "german" in query_lower:
                    target_lang = "German"
                elif "chinese" in query_lower:
                    target_lang = "Chinese"
                elif "japanese" in query_lower:
                    target_lang = "Japanese"
                
                # Create translation task
                translate_task = Task(
                    description=f"""
                    Translate the following document to {target_lang} while preserving meaning and context:
                    
                    Document Content:
                    {document_content[:6000]}
                    
                    Provide the translation in {target_lang}.
                    """,
                    agent=self.agents["translator"],
                    expected_output=f"Document translation to {target_lang}"
                )
                
                crew = Crew(
                    agents=[self.agents["translator"]],
                    tasks=[translate_task],
                    process=Process.sequential,
                    verbose=False
                )
                result = crew.kickoff()
                
                return {
                    "user_query": user_query,
                    "crew_type": "translation",
                    "complexity": "simple",
                    "result": result,
                    "agents_used": ["Document Translation Specialist"],
                    "target_language": target_lang
                }
                
            else:
                # Use comprehensive analysis crew for complex queries
                crew = self.create_comprehensive_analysis_crew(document_content)
                result = crew.kickoff()
                
                return {
                    "user_query": user_query,
                    "crew_type": "comprehensive_analysis",
                    "complexity": "complex",
                    "result": result,
                    "agents_used": ["Document Classification Specialist", "Sentiment Analysis Specialist", 
                                   "Action Item Extraction Specialist", "Document Analysis Coordinator"]
                }
                
        except Exception as e:
            print(f"Error in CrewAI process_query: {str(e)}")
            return {
                "user_query": user_query,
                "crew_type": "error",
                "complexity": "unknown",
                "result": f"Processing error: {str(e)}",
                "agents_used": []
            } 