import json
import re
from typing import Dict, List, Tuple, Any, Optional
from enum import Enum
import boto3
import os

class AgentAction(Enum):
    """Enumeration of possible agent actions"""
    SUMMARIZE = "summarize"
    EXTRACT_ENTITIES = "extract_entities"
    ANSWER_QUESTION = "answer_question"
    COMPARE_DOCUMENTS = "compare_documents"
    TRANSLATE = "translate"
    CLASSIFY = "classify"
    EXTRACT_INSIGHTS = "extract_insights"
    FIND_INFORMATION = "find_information"
    ANALYZE_SENTIMENT = "analyze_sentiment"
    EXTRACT_ACTION_ITEMS = "extract_action_items"

class DocumentIntelligenceAgent:
    """
    Advanced Document Intelligence Agent that can perform multiple tasks
    based on user queries and document content
    """
    
    def __init__(self):
        self.bedrock_client = boto3.client("bedrock-runtime")
        self.model_id = os.getenv('BEDROCK_MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0')
        self.context = {}
        self.document_memory = {}
        
    def analyze_user_intent(self, user_query: str, document_content: str = "") -> Dict[str, Any]:
        """
        Analyze user query to determine intent and required action
        """
        # For now, use fallback to ensure it works
        return self._fallback_intent_analysis(user_query)
    
    def _fallback_intent_analysis(self, user_query: str) -> Dict[str, Any]:
        """Enhanced intent analysis using keyword matching with better accuracy"""
        query_lower = user_query.lower()
        
        print(f"Analyzing query: '{user_query}' -> '{query_lower}'")
        
        # More specific and accurate intent detection
        # Check for conclusion-related queries first
        if any(word in query_lower for word in ['conclusion', 'conclude', 'concluding', 'final', 'ending', 'summary of findings']):
            print(f"Detected: ANSWER_QUESTION (CONCLUSION)")
            return {
                "action": "answer_question",
                "confidence": 0.9,
                "reasoning": "User asking about the conclusion of the document",
                "parameters": {"question": "What is the conclusion of this document?"},
                "requires_multiple_docs": False
            }
        
        # Check for author-related queries (MUST come before general "who" queries)
        elif any(word in query_lower for word in ['author', 'writer', 'who wrote', 'who is the author', 'who created', 'who is author']):
            print(f"Detected: ANSWER_QUESTION (AUTHOR)")
            return {
                "action": "answer_question",
                "confidence": 0.9,
                "reasoning": "User asking about the author of the document",
                "parameters": {"question": "Who is the author of this document?"},
                "requires_multiple_docs": False
            }
        
        # Check for findings-related queries (prioritize over insights)
        elif any(word in query_lower for word in ['finding', 'findings', 'main finding', 'key finding', 'result']):
            print(f"Detected: ANSWER_QUESTION (FINDINGS)")
            return {
                "action": "answer_question",
                "confidence": 0.8,
                "reasoning": "User asking about specific findings in the document",
                "parameters": {"question": user_query},
                "requires_multiple_docs": False
            }
        
        # Check for people/entities queries (but NOT author queries)
        elif any(word in query_lower for word in ['person', 'people', 'personnel', 'individuals', 'names']) and 'author' not in query_lower:
            print(f"Detected: EXTRACT_ENTITIES")
            return {
                "action": "extract_entities",
                "confidence": 0.8,
                "reasoning": "User asking about people or individuals mentioned",
                "parameters": {"entity_types": ["PERSON", "ORGANIZATION"]},
                "requires_multiple_docs": False
            }
        
        # Check for general "who" queries (but NOT author queries)
        elif 'who' in query_lower and 'author' not in query_lower:
            print(f"Detected: EXTRACT_ENTITIES")
            return {
                "action": "extract_entities",
                "confidence": 0.8,
                "reasoning": "User asking about people or individuals mentioned",
                "parameters": {"entity_types": ["PERSON", "ORGANIZATION"]},
                "requires_multiple_docs": False
            }
        
        # Check for organization queries
        elif any(word in query_lower for word in ['organization', 'company', 'institution', 'university', 'college', 'school']):
            print(f"Detected: EXTRACT_ENTITIES")
            return {
                "action": "extract_entities",
                "confidence": 0.8,
                "reasoning": "User asking about organizations or institutions",
                "parameters": {"entity_types": ["ORGANIZATION"]},
                "requires_multiple_docs": False
            }
        
        # Check for action items
        elif any(word in query_lower for word in ['action item', 'task', 'todo', 'deadline', 'responsibility', 'recommendation', 'suggestion']):
            print(f"Detected: EXTRACT_ACTION_ITEMS")
            return {
                "action": "extract_action_items",
                "confidence": 0.8,
                "reasoning": "User wants action items and tasks",
                "parameters": {},
                "requires_multiple_docs": False
            }
        
        # Check for translation requests
        elif any(word in query_lower for word in ['translate', 'spanish', 'french', 'german', 'chinese', 'japanese', 'language']):
            print(f"Detected: TRANSLATE")
            target_lang = "Spanish"
            if "french" in query_lower:
                target_lang = "French"
            elif "german" in query_lower:
                target_lang = "German"
            elif "chinese" in query_lower:
                target_lang = "Chinese"
            elif "japanese" in query_lower:
                target_lang = "Japanese"
            return {
                "action": "translate",
                "confidence": 0.9,
                "reasoning": f"User requested translation to {target_lang}",
                "parameters": {"target_language": target_lang},
                "requires_multiple_docs": False
            }
        
        # Check for classification requests
        elif any(word in query_lower for word in ['classify', 'type', 'category', 'what kind', 'document type']):
            print(f"Detected: CLASSIFY")
            return {
                "action": "classify",
                "confidence": 0.8,
                "reasoning": "User wants to classify the document type",
                "parameters": {},
                "requires_multiple_docs": False
            }
        
        # Check for insights and findings
        elif any(word in query_lower for word in ['insight', 'pattern', 'trend', 'discovery']):
            print(f"Detected: EXTRACT_INSIGHTS")
            return {
                "action": "extract_insights",
                "confidence": 0.8,
                "reasoning": "User wants key insights and patterns",
                "parameters": {},
                "requires_multiple_docs": False
            }
        
        # Check for sentiment analysis
        elif any(word in query_lower for word in ['sentiment', 'tone', 'emotion', 'mood', 'attitude', 'feeling']):
            print(f"Detected: ANALYZE_SENTIMENT")
            return {
                "action": "analyze_sentiment",
                "confidence": 0.8,
                "reasoning": "User wants sentiment analysis",
                "parameters": {},
                "requires_multiple_docs": False
            }
        
        # Check for comparison requests
        elif any(word in query_lower for word in ['compare', 'difference', 'similar', 'versus', 'vs', 'against']):
            print(f"Detected: COMPARE_DOCUMENTS")
            return {
                "action": "compare_documents",
                "confidence": 0.7,
                "reasoning": "User wants to compare documents",
                "parameters": {},
                "requires_multiple_docs": True
            }
        
        # Check for summarization requests
        elif any(word in query_lower for word in ['summarize', 'summary', 'summarize', 'overview', 'brief']):
            print(f"Detected: SUMMARIZE")
            return {
                "action": "summarize",
                "confidence": 0.8,
                "reasoning": "User requested summarization",
                "parameters": {},
                "requires_multiple_docs": False
            }
        
        # General question detection (catch-all for what/how/why/when/where/which)
        elif any(word in query_lower for word in ['what', 'how', 'why', 'when', 'where', 'which', 'question']):
            print(f"Detected: ANSWER_QUESTION")
            return {
                "action": "answer_question",
                "confidence": 0.7,
                "reasoning": "User asking a general question about the document",
                "parameters": {"question": user_query},
                "requires_multiple_docs": False
            }
        elif any(word in query_lower for word in ['action item', 'task', 'todo', 'deadline', 'responsibility']):
            print(f"Detected: EXTRACT_ACTION_ITEMS")
            return {
                "action": "extract_action_items",
                "confidence": 0.7,
                "reasoning": "User wants action items and tasks",
                "parameters": {},
                "requires_multiple_docs": False
            }
        elif any(word in query_lower for word in ['who', 'person', 'people', 'organization', 'company']):
            print(f"Detected: EXTRACT_ENTITIES")
            return {
                "action": "extract_entities",
                "confidence": 0.7,
                "reasoning": "User asking about people or organizations",
                "parameters": {"entity_types": ["PERSON", "ORGANIZATION"]},
                "requires_multiple_docs": False
            }
        elif any(word in query_lower for word in ['translate', 'spanish', 'french', 'german', 'chinese', 'japanese']):
            print(f"Detected: TRANSLATE")
            target_lang = "Spanish"
            if "french" in query_lower:
                target_lang = "French"
            elif "german" in query_lower:
                target_lang = "German"
            elif "chinese" in query_lower:
                target_lang = "Chinese"
            elif "japanese" in query_lower:
                target_lang = "Japanese"
            return {
                "action": "translate",
                "confidence": 0.8,
                "reasoning": f"User requested translation to {target_lang}",
                "parameters": {"target_language": target_lang},
                "requires_multiple_docs": False
            }
        elif any(word in query_lower for word in ['classify', 'type', 'category', 'what kind']):
            print(f"Detected: CLASSIFY")
            return {
                "action": "classify",
                "confidence": 0.7,
                "reasoning": "User wants to classify the document type",
                "parameters": {},
                "requires_multiple_docs": False
            }
        elif any(word in query_lower for word in ['insight', 'pattern', 'trend', 'key finding']):
            print(f"Detected: EXTRACT_INSIGHTS")
            return {
                "action": "extract_insights",
                "confidence": 0.7,
                "reasoning": "User wants key insights and patterns",
                "parameters": {},
                "requires_multiple_docs": False
            }
        elif any(word in query_lower for word in ['sentiment', 'tone', 'emotion', 'mood']):
            print(f"Detected: ANALYZE_SENTIMENT")
            return {
                "action": "analyze_sentiment",
                "confidence": 0.7,
                "reasoning": "User wants sentiment analysis",
                "parameters": {},
                "requires_multiple_docs": False
            }
        elif any(word in query_lower for word in ['compare', 'difference', 'similar', 'versus']):
            print(f"Detected: COMPARE_DOCUMENTS")
            return {
                "action": "compare_documents",
                "confidence": 0.7,
                "reasoning": "User wants to compare documents",
                "parameters": {},
                "requires_multiple_docs": True
            }
        elif any(word in query_lower for word in ['summarize', 'summary', 'summarize']):
            print(f"Detected: SUMMARIZE")
            return {
                "action": "summarize",
                "confidence": 0.8,
                "reasoning": "User requested summarization",
                "parameters": {},
                "requires_multiple_docs": False
            }
        else:
            print(f"Detected: NO SPECIFIC INTENT - ASK USER")
            return {
                "action": "ask_clarification",
                "confidence": 0.3,
                "reasoning": "User query unclear - need clarification on what they want",
                "parameters": {"suggestions": [
                    "What is this document about?",
                    "Who is the author?",
                    "What is the conclusion?",
                    "Who are the key people mentioned?",
                    "What organizations are mentioned?",
                    "What are the main findings?",
                    "Extract action items",
                    "Summarize this document",
                    "Classify document type",
                    "Analyze sentiment"
                ]},
                "requires_multiple_docs": False
            }
    
    def execute_action(self, action: str, document_content: str, parameters: Dict = None) -> Dict[str, Any]:
        """
        Execute the determined action on the document content
        """
        if parameters is None:
            parameters = {}
            
        try:
            if action == "summarize":
                return self._summarize_document(document_content)
            elif action == "extract_entities":
                return self._extract_entities(document_content, parameters)
            elif action == "answer_question":
                return self._answer_question(document_content, parameters)
            elif action == "compare_documents":
                return self._compare_documents(document_content, parameters)
            elif action == "translate":
                return self._translate_document(document_content, parameters)
            elif action == "classify":
                return self._classify_document(document_content)
            elif action == "extract_insights":
                return self._extract_insights(document_content)
            elif action == "find_information":
                return self._find_information(document_content, parameters)
            elif action == "analyze_sentiment":
                return self._analyze_sentiment(document_content)
            elif action == "extract_action_items":
                return self._extract_action_items(document_content)
            elif action == "ask_clarification":
                return self._ask_clarification(parameters)
            else:
                return {"error": f"Unknown action: {action}"}
                
        except Exception as e:
            return {"error": f"Error executing action {action}: {str(e)}"}
    
    def _summarize_document(self, content: str) -> Dict[str, Any]:
        """Create a comprehensive summary of the document"""
        print(f"_summarize_document called with content length: {len(content)}")
        
        prompt = f"""
        Create a comprehensive summary of the following document. Include:
        1. Main topic and purpose
        2. Key points and findings
        3. Important conclusions
        4. Any recommendations or action items
        
        Document:
        {content[:8000]}  # Limit content length
        
        Provide the summary in a structured format.
        """
        
        print(f"Calling Bedrock with summarization prompt...")
        response = self._call_bedrock(prompt)
        print(f"Summary response received: {response[:200]}...")
        
        result = {
            "action": "summarize",
            "result": response,
            "content_length": len(content),
            "summary_length": len(response)
        }
        
        print(f"Returning result: {result}")
        return result
    
    def _extract_entities(self, content: str, parameters: Dict) -> Dict[str, Any]:
        """Extract named entities from the document with enhanced accuracy"""
        entity_types = parameters.get("entity_types", ["PERSON", "ORGANIZATION", "DATE", "LOCATION"])
        
        print(f"_extract_entities called with entity types: {entity_types}")
        print(f"Content length: {len(content)} characters")
        
        # Enhanced prompt for better entity extraction
        prompt = f"""
        You are an expert entity extraction specialist. Extract the following types of entities from the document with high accuracy.
        
        IMPORTANT INSTRUCTIONS:
        1. Extract ONLY entities that are clearly mentioned in the document
        2. For people: Include full names, titles, and affiliations when available
        3. For organizations: Include full organization names and any relevant details
        4. For dates: Include specific dates, years, time periods mentioned
        5. For locations: Include cities, countries, institutions, addresses mentioned
        6. Be precise and avoid duplicates
        7. If no entities of a type are found, return an empty list
        
        Entity types to extract: {', '.join(entity_types)}
        
        Document Content:
        {content[:6000]}
        
        Return the results in this exact JSON format:
        {{
            "people": ["Full Name 1", "Full Name 2"],
            "organizations": ["Organization Name 1", "Organization Name 2"],
            "dates": ["Date 1", "Date 2"],
            "locations": ["Location 1", "Location 2"]
        }}
        
        Ensure the JSON is valid and properly formatted.
        """
        
        print(f"Calling Bedrock with enhanced entity extraction prompt...")
        response = self._call_bedrock(prompt)
        print(f"Entity extraction response received: {response[:200]}...")
        
        try:
            entities = json.loads(response)
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            # Fallback: try to extract entities from the raw response
            entities = {"raw_response": response, "error": "JSON parsing failed"}
            
        result = {
            "action": "extract_entities",
            "entities": entities,
            "entity_types": entity_types
        }
        
        print(f"Returning entity result: {result}")
        return result
    
    def _answer_question(self, content: str, parameters: Dict) -> Dict[str, Any]:
        """Answer specific questions about the document with enhanced accuracy"""
        question = parameters.get("question", "What is this document about?")
        
        print(f"_answer_question called with question: '{question}'")
        print(f"Content length: {len(content)} characters")
        
        # Enhanced prompt for better accuracy
        prompt = f"""
        You are an expert document analyst. Answer the following question about the document with high accuracy and detail.
        
        IMPORTANT INSTRUCTIONS:
        1. Answer ONLY based on the information present in the document
        2. If the information is not in the document, clearly state "This information is not mentioned in the document"
        3. Be specific and provide exact details when available
        4. For author questions, provide the exact name and affiliation
        5. For conclusion questions, provide the actual conclusion from the document
        6. Use direct quotes from the document when appropriate
        7. Structure your answer clearly and logically
        8. Keep answers concise and focused on what was asked
        
        Question: {question}
        
        Document Content:
        {content[:8000]}
        
        Provide a focused, accurate answer based solely on the document content. Do not include extra information.
        """
        
        print(f"Calling Bedrock with enhanced question-answering prompt...")
        response = self._call_bedrock(prompt)
        print(f"Question answer response received: {response[:200]}...")
        
        result = {
            "action": "answer_question",
            "question": question,
            "answer": response
        }
        
        print(f"Returning answer result: {result}")
        return result
    
    def _compare_documents(self, content: str, parameters: Dict) -> Dict[str, Any]:
        """Compare multiple documents"""
        # This would need multiple documents - for now, analyze single document
        prompt = f"""
        Analyze this document and provide insights about:
        1. Document type and purpose
        2. Key themes and topics
        3. Writing style and tone
        4. Potential areas for comparison with other documents
        
        Document:
        {content[:6000]}
        """
        
        response = self._call_bedrock(prompt)
        return {
            "action": "compare_documents",
            "analysis": response,
            "note": "Multiple document comparison requires additional documents"
        }
    
    def _translate_document(self, content: str, parameters: Dict) -> Dict[str, Any]:
        """Translate document content"""
        target_language = parameters.get("target_language", "Spanish")
        
        prompt = f"""
        Translate the following document to {target_language}. Maintain the original meaning and tone.
        
        Document:
        {content[:6000]}
        
        Provide the translation in {target_language}.
        """
        
        response = self._call_bedrock(prompt)
        return {
            "action": "translate",
            "target_language": target_language,
            "translation": response,
            "original_length": len(content)
        }
    
    def _classify_document(self, content: str) -> Dict[str, Any]:
        """Classify the document type"""
        prompt = f"""
        Classify this document into one of the following categories:
        - Business Report
        - Legal Document
        - Academic Paper
        - News Article
        - Technical Manual
        - Financial Statement
        - Meeting Minutes
        - Policy Document
        - Research Paper
        - Other
        
        Document:
        {content[:4000]}
        
        Provide the classification and confidence level.
        """
        
        response = self._call_bedrock(prompt)
        return {
            "action": "classify",
            "classification": response
        }
    
    def _extract_insights(self, content: str) -> Dict[str, Any]:
        """Extract key insights from the document"""
        prompt = f"""
        Extract key insights from this document:
        
        Document:
        {content[:8000]}
        
        Provide insights in these categories:
        1. Key Findings
        2. Important Trends
        3. Critical Issues
        4. Recommendations
        5. Implications
        """
        
        response = self._call_bedrock(prompt)
        return {
            "action": "extract_insights",
            "insights": response
        }
    
    def _find_information(self, content: str, parameters: Dict) -> Dict[str, Any]:
        """Find specific information in the document"""
        search_terms = parameters.get("search_terms", ["key", "important", "main"])
        
        prompt = f"""
        Find information related to these terms in the document:
        {', '.join(search_terms)}
        
        Document:
        {content[:8000]}
        
        Provide relevant excerpts and context for each term.
        """
        
        response = self._call_bedrock(prompt)
        return {
            "action": "find_information",
            "search_terms": search_terms,
            "results": response
        }
    
    def _analyze_sentiment(self, content: str) -> Dict[str, Any]:
        """Analyze the sentiment and tone of the document"""
        prompt = f"""
        Analyze the sentiment and tone of this document:
        
        Document:
        {content[:6000]}
        
        Provide analysis of:
        1. Overall sentiment (positive/negative/neutral)
        2. Tone (formal/informal, objective/subjective)
        3. Emotional content
        4. Writing style
        """
        
        response = self._call_bedrock(prompt)
        return {
            "action": "analyze_sentiment",
            "sentiment_analysis": response
        }
    
    def _extract_action_items(self, content: str) -> Dict[str, Any]:
        """Extract action items, tasks, and deadlines"""
        prompt = f"""
        Extract action items, tasks, deadlines, and responsibilities from this document:
        
        Document:
        {content[:8000]}
        
        Identify:
        1. Action items and tasks
        2. Deadlines and due dates
        3. Responsible parties
        4. Priority levels
        5. Dependencies
        """
        
        response = self._call_bedrock(prompt)
        return {
            "action": "extract_action_items",
            "action_items": response
        }
    
    def _ask_clarification(self, parameters: Dict) -> Dict[str, Any]:
        """Ask user for clarification when intent is unclear"""
        suggestions = parameters.get("suggestions", [])
        
        clarification_text = f"""
I'm not sure what you'd like me to do with this document. Here are some common questions you can ask:

"""
        for i, suggestion in enumerate(suggestions, 1):
            clarification_text += f"{i}. {suggestion}\n"
        
        clarification_text += f"""
You can also ask me to:
- Translate the document to another language
- Extract specific information
- Compare with other documents
- Find patterns or insights

Just tell me what you're looking for, and I'll help you find it!
"""
        
        return {
            "action": "ask_clarification",
            "message": clarification_text,
            "suggestions": suggestions
        }
    
    def _call_bedrock(self, prompt: str) -> str:
        """Make a call to Bedrock model"""
        try:
            print(f"Calling Bedrock with model: {self.model_id}")
            print(f"Prompt length: {len(prompt)} characters")
            
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 4000,  # Increased for better responses
                    "temperature": 0.1,   # Lower temperature for more consistent answers
                    "messages": [{"role": "user", "content": prompt}]
                }),
                contentType="application/json",
                accept="application/json"
            )
            
            result = json.loads(response['body'].read())
            print(f"Bedrock response received: {len(str(result))} characters")
            
            if 'content' in result and len(result['content']) > 0:
                return result['content'][0]['text']
            else:
                print(f"Unexpected Bedrock response format: {result}")
                return f"Error: Unexpected response format from Bedrock"
            
        except Exception as e:
            print(f"Bedrock error: {str(e)}")
            return f"Error calling Bedrock: {str(e)}"
    
    def process_query(self, user_query: str, document_content: str = "", document_id: str = "") -> Dict[str, Any]:
        """
        Main method to process user query and execute appropriate action
        """
        try:
            print(f"Processing query: '{user_query}'")
            print(f"Document content length: {len(document_content)} characters")
            
            # Store document in memory
            if document_id and document_content:
                self.document_memory[document_id] = document_content
            
            # Analyze user intent
            intent = self.analyze_user_intent(user_query, document_content)
            print(f"Intent analysis: {intent['action']} (confidence: {intent['confidence']})")
            
            # Execute the action
            result = self.execute_action(intent["action"], document_content, intent["parameters"])
            print(f"Action executed: {intent['action']}")
            
            # Combine results
            return {
                "user_query": user_query,
                "intent_analysis": intent,
                "action_result": result,
                "agent_reasoning": intent["reasoning"],
                "confidence": intent["confidence"]
            }
        except Exception as e:
            print(f"Error in process_query: {str(e)}")
            return {
                "user_query": user_query,
                "intent_analysis": {"action": "error", "confidence": 0.0, "reasoning": "Error occurred"},
                "action_result": {"error": f"Processing error: {str(e)}"},
                "agent_reasoning": f"Error occurred: {str(e)}",
                "confidence": 0.0
            } 