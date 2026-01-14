# list_models.py
import google.generativeai as genai
from config import get_settings

settings = get_settings()
genai.configure(api_key=settings.gemini_api_key)

print("Listing all available models...\n")

try:
    models = genai.list_models()
    
    generate_models = []
    
    for model in models:
        print(f"Model: {model.name}")
        print(f"  Display name: {model.display_name}")
        print(f"  Supported methods: {model.supported_generation_methods}")
        print()
        
        if 'generateContent' in model.supported_generation_methods:
            generate_models.append(model.name)
    
    print("\n" + "="*50)
    print("Models that support generateContent:")
    print("="*50)
    for m in generate_models:
        print(f"✅ {m}")
    
    if not generate_models:
        print("❌ No models found that support generateContent!")
        print("\nThis means:")
        print("1. Your API key might be invalid")
        print("2. You need to enable the Gemini API")
        print("3. The API key is from the wrong Google service")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Get API key from: https://aistudio.google.com/app/apikey")
    print("2. Make sure you're signed into the right Google account")
    print("3. Check if Gemini API is available in your region")