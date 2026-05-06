# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pydantic import SecretStr

class Settings(BaseSettings):
    """Application settings loaded from .env file"""
    
    # Twilio Configuration
    twilio_account_sid: SecretStr
    twilio_auth_token: SecretStr
    twilio_phone_number: SecretStr
    
    # Google Gemini Configuration (changed from OpenAI)
    gemini_api_key: SecretStr
    
    # Google Maps Configuration
    google_maps_api_key: SecretStr
    
    # Deepgram (Optional)
    deepgram_api_key: SecretStr = SecretStr("")
    
    # Server Configuration
    port: int = 8000
    host: str = "0.0.0.0"
    base_url: str = "http://localhost:8000"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
