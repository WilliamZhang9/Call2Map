# config.py (for Pydantic v2)
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # Twilio
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str
    
    # APIs
    openai_api_key: str
    deepgram_api_key: str = ""
    google_maps_api_key: str
    
    # Server
    port: int = 8000
    host: str = "0.0.0.0"
    base_url: str
    
    model_config = SettingsConfigDict(env_file=".env")

@lru_cache()
def get_settings():
    return Settings()