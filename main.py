# main.py
"""
Call2Map - AI Voice Assistant via Phone Call
Simplified architecture using Twilio's built-in speech recognition
"""
from fastapi import FastAPI, Request, Form  # ← Make sure this line is here
from fastapi.responses import Response
import uvicorn
from config import get_settings
import logging
from typing import Dict
import asyncio
from services.llm_service import LLMService
from services.maps_service import MapsService
from services.sms_service import sms_service

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()
app = FastAPI(title="Call2Map")

# Initialize services
# llm_service = LLMService(settings.openai_api_key)
llm_service = LLMService(settings.gemini_api_key)
maps_service = MapsService(settings.google_maps_api_key)

# Store active call sessions
call_sessions: Dict[str, dict] = {}

@app.get("/")
async def root():
    return {
        "status": "Call2Map is running! 🎉",
        "phone": settings.twilio_phone_number,
        "active_calls": len(call_sessions),
        "message": "Call this number to talk to the AI assistant!"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/voice/incoming")
async def handle_incoming_call(request: Request):
    """Handle incoming Twilio voice calls"""
    form_data = await request.form()
    caller_number = form_data.get('From')
    call_sid = form_data.get('CallSid')

    logger.info(f"📞 Incoming call from {caller_number}, SID: {call_sid}")

    # Initialize session
    call_sessions[call_sid] = {
        "caller": caller_number,
        "messages": [],
        "location": None
    }

    # TwiML with speech recognition
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">Hello! Welcome to Call 2 Live. I'm your A I assistant. I can help you find restaurants, stores, and other places near you.</Say>
    <Gather input="speech" timeout="3" speechTimeout="auto" action="{settings.base_url}/voice/process-speech" method="POST">
        <Say voice="Polly.Joanna">How can I help you today?</Say>
    </Gather>
    <Say voice="Polly.Joanna">I didn't hear anything. Please call back if you need assistance. Goodbye!</Say>
</Response>"""

    return Response(content=twiml, media_type="application/xml")

@app.post("/voice/process-speech")
async def process_speech(request: Request):
    """Process speech input from user"""
    form_data = await request.form()
    speech_result = form_data.get('SpeechResult', '')
    call_sid = form_data.get('CallSid')

    logger.info(f"🗣️  User said: {speech_result}")

    if not speech_result or call_sid not in call_sessions:
        return await respond_and_hangup("I didn't catch that. Please try again.")

    # Get session
    session = call_sessions[call_sid]
    session['call_sid'] = call_sid

    # Add to conversation history
    session['messages'].append({
        "role": "user",
        "content": speech_result
    })

    try:
        # Process with LLM
        response = await llm_service.process_message(
            speech_result,
            session['messages'],
            session.get('location'),
            session_id=call_sid
        )

        if response['type'] == 'function_call':
            # Handle function call
            result_text = await handle_function_call(response, session)
        else:
            # Direct text response
            result_text = response['content']

        # Add AI response to history
        session['messages'].append({
            "role": "assistant",
            "content": result_text
        })

        # Create TwiML response
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">{result_text}</Say>
    <Gather input="speech" timeout="3" speechTimeout="auto" action="{settings.base_url}/voice/process-speech" method="POST">
        <Say voice="Polly.Joanna">Is there anything else I can help you with?</Say>
    </Gather>
    <Say voice="Polly.Joanna">Thank you for using Call 2 Live. Goodbye!</Say>
</Response>"""

        return Response(content=twiml, media_type="application/xml")

    except Exception as e:
        logger.error(f"Error processing speech: {e}")
        return await respond_and_hangup("I'm sorry, I encountered an error. Please try again.")

async def handle_function_call(response: Dict, session: Dict) -> str:
    """Execute function calls from LLM"""
    function_name = response['function_name']
    function_args = response['function_args']

    logger.info(f"Executing function: {function_name} with args: {function_args}")

    try:
        if function_name == 'search_places':
            query = function_args.get('query')
            location = function_args.get('location')

            # Validate inputs
            if not query or not location or query == 'None' or location == 'None':
                return "I need both what you're looking for and a location. Could you try again?"

            # Store location in session
            session['location'] = location

            # Search places
            places = maps_service.search_places(query, location)

            if not places:
                return f"I couldn't find any {query} near {location}. Could you try a different search?"

            # Format result
            session_id = session.get('call_sid', 'default')
            result_text = await llm_service.format_function_result(
                function_name,
                {'places': places, 'count': len(places)},
                session_id=session_id
            )

            # Send SMS with details if multiple results
            if len(places) > 1:
                try:
                    sms_text = sms_service.format_places_sms(places)
                    sms_service.send_sms(session['caller'], sms_text)
                    result_text += " I've also sent the details to your phone."
                except Exception as e:
                    logger.error(f"SMS error: {e}")

            return result_text

        elif function_name == 'get_reservation_info':
            place_name = function_args.get('place_name')
            location = function_args.get('location') or session.get('location')

            if not place_name or not location:
                return "Which restaurant would you like to book at?"

            # First search for the place
            places = maps_service.search_places(place_name, location)

            if not places:
                return f"I couldn't find {place_name} near {location}."

            # Get reservation info for the top result
            place = places[0]
            place_id = place.get('place_id')

            if not place_id:
                return "I found the restaurant but couldn't get booking details."

            res_info = maps_service.get_reservation_info(place_id)

            # Build response
            response = f"For {place['name']}, "

            if res_info.get('booking_url'):
                platform = res_info.get('platform', 'their website')
                response += f"you can book online through {platform}. "
                # Send SMS with booking link
                try:
                    sms_text = f"Book a table at {place['name']}:\n\n"
                    sms_text += f"📱 {res_info['booking_url']}\n\n"
                    if place.get('phone'):
                        sms_text += f"Or call: {place['phone']}\n\n"
                    sms_text += f"View on map: {res_info.get('maps_url', '')}"
                    sms_service.send_sms(session['caller'], sms_text)
                    response += "I've texted you the booking link."
                except Exception as e:
                    logger.error(f"SMS error: {e}")
            elif res_info.get('phone'):
                response += f"please call them at {res_info['phone']} to make a reservation. "
                # Send SMS with phone number
                try:
                    sms_text = f"Call {place['name']} to reserve:\n\n"
                    sms_text += f"📞 {res_info['phone']}\n\n"
                    if place.get('address'):
                        sms_text += f"📍 {place['address']}\n\n"
                    sms_text += f"View on map: {res_info.get('maps_url', '')}"
                    sms_service.send_sms(session['caller'], sms_text)
                    response += "I've texted you their phone number."
                except Exception as e:
                    logger.error(f"SMS error: {e}")
            else:
                response += "I don't have booking information, but "
                if place.get('website'):
                    response += f"you can check their website. I'll text you the details."
                    try:
                        sms_text = f"{place['name']}:\n\n"
                        sms_text += f"🌐 {place['website']}\n\n"
                        if place.get('phone'):
                            sms_text += f"📞 {place['phone']}"
                        sms_service.send_sms(session['caller'], sms_text)
                    except Exception as e:
                        logger.error(f"SMS error: {e}")
                else:
                    response += "I couldn't find booking information for this restaurant."

            return response

        elif function_name == 'send_sms':
            message = function_args.get('message')
            if message:
                success = sms_service.send_sms(session['caller'], message)
                return "I've sent the information to your phone." if success else "I had trouble sending the text."
            return "I need a message to send."

        else:
            return "I'm not sure how to help with that."

    except Exception as e:
        logger.error(f"Error executing function: {e}")
        import traceback
        traceback.print_exc()
        return "I encountered an issue. Please try again."

async def respond_and_hangup(message: str) -> Response:
    """Create a TwiML response that says something and hangs up"""
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Joanna">{message}</Say>
    <Hangup/>
</Response>"""
    return Response(content=twiml, media_type="application/xml")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on server shutdown"""
    logger.info("🔄 Shutting down Call2Live...")
    call_sessions.clear()

if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("🚀 Starting Call2Live Server")
    logger.info("=" * 50)
    logger.info(f"📞 Phone Number: {settings.twilio_phone_number}")
    logger.info(f"🌐 Base URL: {settings.base_url}")
    logger.info(f"🔌 Port: {settings.port}")
    logger.info("=" * 50)

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )
