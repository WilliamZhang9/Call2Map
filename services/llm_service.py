# services/llm_service.py
from google import genai
from google.genai import types
import json
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTION = """You are a helpful AI assistant that helps people find places and get information through phone calls.

You have access to Google Maps to search for nearby locations. When users ask about places, restaurants, services, etc., use the search_places function.

Guidelines:
- Be concise and natural (this is a phone call, keep responses under 50 words)
- Always confirm the user's location before searching
- Provide only the top 2-3 results to avoid overwhelming the user
- Offer to send details via SMS if there are multiple results
- Be friendly and conversational
- If you don't have the user's location, ask for it politely"""

# Define function declarations
TOOLS = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="search_places",
                description="Search for places near a location using Google Maps",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "query": types.Schema(
                            type=types.Type.STRING,
                            description="What to search for (e.g., 'sushi restaurants', 'gas stations')"
                        ),
                        "location": types.Schema(
                            type=types.Type.STRING,
                            description="City, address, or zip code to search near"
                        )
                    },
                    required=["query", "location"]
                )
            ),
            types.FunctionDeclaration(
                name="send_sms",
                description="Send details via SMS to the caller's phone",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "message": types.Schema(
                            type=types.Type.STRING,
                            description="The message content to send"
                        )
                    },
                    required=["message"]
                )
            )
        ]
    )
]

class LLMService:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.0-flash-exp"
        self.chats = {}
    
    async def process_message(
        self,
        user_message: str,
        conversation_history: List[Dict],
        user_location: Optional[str] = None,
        session_id: str = "default"
    ) -> Dict:
        """Process user message with function calling"""
        
        try:
            # Add location context if available
            message = user_message
            if user_location:
                message = f"[User's location: {user_location}]\n{user_message}"
            
            # Build conversation history for Gemini
            contents = []
            for msg in conversation_history[-10:]:  # Last 10 messages
                role = "user" if msg["role"] == "user" else "model"
                contents.append(types.Content(
                    role=role,
                    parts=[types.Part(text=msg["content"])]
                ))
            
            # Add current message
            contents.append(types.Content(
                role="user",
                parts=[types.Part(text=message)]
            ))
            
            # Generate response
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    tools=TOOLS,
                    temperature=0.7,
                    max_output_tokens=150
                )
            )
            
            # Check for function calls
            if response.candidates[0].content.parts[0].function_call:
                func_call = response.candidates[0].content.parts[0].function_call
                
                return {
                    "type": "function_call",
                    "function_name": func_call.name,
                    "function_args": dict(func_call.args),
                    "response": response
                }
            else:
                # Regular text response
                return {
                    "type": "text",
                    "content": response.text
                }
                
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return {
                "type": "text",
                "content": "I apologize, I'm having trouble right now. Could you try again?"
            }
    
    async def format_function_result(
        self,
        function_name: str,
        function_result: Dict,
        session_id: str = "default"
    ) -> str:
        """Format function results into natural language"""
        
        try:
            # Create function response
            function_response = types.FunctionResponse(
                name=function_name,
                response=function_result
            )
            
            # Get natural language description
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=[
                    types.Content(
                        role="user",
                        parts=[types.Part(text="Describe the search results naturally")]
                    ),
                    types.Content(
                        role="model",
                        parts=[types.Part(function_call=types.FunctionCall(
                            name=function_name,
                            args={}
                        ))]
                    ),
                    types.Content(
                        role="user",
                        parts=[types.Part(function_response=function_response)]
                    )
                ],
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.7,
                    max_output_tokens=150
                )
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error formatting result: {e}")
            # Fallback: format manually
            if function_name == "search_places" and "places" in function_result:
                places = function_result["places"]
                if places:
                    top = places[0]
                    return f"I found {len(places)} results. The top option is {top['name']}, rated {top.get('rating', 'N/A')} stars."
            return "I found some results for you."
    
    def clear_chat(self, session_id: str):
        """Clear chat history for a session"""
        if session_id in self.chats:
            del self.chats[session_id]