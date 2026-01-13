# services/sms_service.py
from twilio.rest import Client
import logging
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class SMSService:
    def __init__(self):
        self.client = Client(
            settings.twilio_account_sid,
            settings.twilio_auth_token
        )
        self.from_number = settings.twilio_phone_number
    
    def send_sms(self, to_number: str, message: str) -> bool:
        """Send SMS to a phone number"""
        try:
            msg = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            logger.info(f"SMS sent to {to_number}, SID: {msg.sid}")
            return True
        except Exception as e:
            logger.error(f"Error sending SMS: {e}")
            return False
    
    def format_places_sms(self, places: list) -> str:
        """Format places into SMS-friendly text"""
        if not places:
            return "No places found."
        
        message = "🔍 Places I found:\n\n"
        
        for i, place in enumerate(places[:3], 1):
            message += f"{i}. {place['name']}\n"
            if place.get('rating'):
                message += f"   ⭐ {place['rating']}"
                if place.get('user_ratings_total'):
                    message += f" ({place['user_ratings_total']} reviews)"
                message += "\n"
            if place.get('address'):
                message += f"   📍 {place['address']}\n"
            if place.get('phone'):
                message += f"   📞 {place['phone']}\n"
            message += "\n"
        
        return message.strip()

# Global instance
sms_service = SMSService()
