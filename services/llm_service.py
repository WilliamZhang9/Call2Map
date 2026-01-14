# services/llm_service.py - WORKING VERSION
import google.generativeai as genai
import json
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a helpful AI assistant that helps people find places and make reservations through phone calls.

When users ask about places, extract the query and location, then respond in JSON format:
{"action": "search", "query": "what they want", "location": "where"}

When users ask to book or reserve at a specific place:
{"action": "reserve", "place_name": "restaurant name", "location": "where"}

Examples:
- "Find sushi in New York" → {"action": "search", "query": "sushi restaurants", "location": "New York"}
- "Book a table at Kazu" → {"action": "reserve", "place_name": "Kazu", "location": "current or inferred"}
- "Make a reservation" → {"action": "reserve", "place_name": "from context", "location": "from context"}

Be concise - this is a phone call."""

class LLMService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name='models/gemini-2.5-flash',  # ← Updated model name
            system_instruction=SYSTEM_PROMPT
        )

    async def process_message(
        self,
        user_message: str,
        conversation_history: List[Dict],
        user_location: Optional[str] = None,
        session_id: str = "default"
    ) -> Dict:
        """Process user message"""

        try:
            # Generate response
            response = self.model.generate_content(user_message)
            text = response.text.strip()

            logger.info(f"Gemini response: {text}")

            # Try to parse as JSON for function call
            if '{' in text and '}' in text:
                # Extract JSON from response
                start = text.find('{')
                end = text.rfind('}') + 1
                json_str = text[start:end]

                try:
                    data = json.loads(json_str)
                    if data.get('action') == 'search':
                        return {
                            "type": "function_call",
                            "function_name": "search_places",
                            "function_args": {
                                "query": data.get('query', ''),
                                "location": data.get('location', '')
                            }
                        }
                    elif data.get('action') == 'reserve':
                        return {
                            "type": "function_call",
                            "function_name": "get_reservation_info",
                            "function_args": {
                                "place_name": data.get('place_name', ''),
                                "location": data.get('location', '')
                            }
                        }
                except json.JSONDecodeError as e:
                    logger.error(f"JSON parse error: {e}")

            # Fallback: direct text response
            return {"type": "text", "content": text}

        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return {
                "type": "text",
                "content": "I'm having trouble. Please try again."
            }

    async def format_function_result(
        self,
        function_name: str,
        function_result: Dict,
        session_id: str = "default"
    ) -> str:
        """Format results"""
        if function_name == "search_places" and "places" in function_result:
            places = function_result["places"]

            if not places:
                return "I couldn't find any places matching that search."

            if len(places) == 1:
                place = places[0]
                msg = f"I found {place['name']}"
                if place.get('address'):
                    msg += f" at {place['address']}"
                if place.get('rating'):
                    msg += f", rated {place['rating']} stars"
                return msg + "."

            # Multiple results
            place = places[0]
            msg = f"I found {len(places)} places. The top rated is {place['name']}"
            if place.get('rating'):
                msg += f" with {place['rating']} stars"
            msg += ". Would you like me to text you the full list?"
            return msg

        return "Here are the results I found."

    def clear_chat(self, session_id: str):
        """Clear chat history"""
        pass