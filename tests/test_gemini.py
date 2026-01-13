# test_gemini_new.py
from google import genai
from google.genai import types
from config import get_settings

settings = get_settings()

print("Testing new Google GenAI package...\n")

try:
    # Create client
    client = genai.Client(api_key=settings.gemini_api_key)
    
    # Test simple generation
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents="Say hello in 5 words"
    )
    
    print("✅ Gemini API working!")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nMake sure:")
    print("1. GEMINI_API_KEY is set in .env")
    print("2. pip install google-genai")
    print("3. You have internet connection")