# models/conversation.py
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class CallSession(BaseModel):
    """Represents an active phone call session"""
    call_sid: str
    caller_number: str
    started_at: datetime
    location: Optional[Dict] = None
    conversation_history: List[Dict] = []
    user_context: Dict = {}

class UserIntent(BaseModel):
    """Parsed user intent from speech"""
    intent_type: str  # 'places_search', 'directions', 'info', 'unknown'
    query: str
    requires_location: bool = False
    extracted_location: Optional[Dict] = None
    confidence: float = 0.0

class PlaceResult(BaseModel):
    """Google Maps place result"""
    name: str
    address: str
    rating: Optional[float] = None
    user_ratings_total: Optional[int] = None
    place_id: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    open_now: Optional[bool] = None
