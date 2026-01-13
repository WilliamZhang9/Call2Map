# check_install.py
def test_installation():
    print("Testing installation...\n")
    
    try:
        print("1. Testing Pydantic...")
        import pydantic
        print(f"   ✅ Pydantic {pydantic.__version__}")
        
        print("2. Testing FastAPI...")
        from fastapi import FastAPI
        print(f"   ✅ FastAPI imported")
        
        print("3. Testing Uvicorn...")
        import uvicorn
        print(f"   ✅ Uvicorn imported")
        
        print("4. Testing Twilio...")
        import twilio
        print(f"   ✅ Twilio {twilio.__version__}")
        
        print("5. Testing OpenAI...")
        import openai
        print(f"   ✅ OpenAI {openai.__version__}")
        
        print("6. Testing Google Maps...")
        import googlemaps
        print(f"   ✅ Google Maps imported")
        
        print("7. Testing other packages...")
        import websockets
        import aiohttp
        print(f"   ✅ WebSockets and AioHTTP imported")
        
        print("8. Testing pydub (optional)...")
        try:
            import pydub
            print(f"   ✅ Pydub imported")
        except ImportError:
            print(f"   ⚠️  Pydub not available (using alternative audio processing)")
        
        print("\n9. Testing config loading...")
        try:
            from config import get_settings
            settings = get_settings()
            print(f"   ✅ Config loaded")
            print(f"   📞 Phone: {settings.twilio_phone_number}")
        except Exception as e:
            print(f"   ⚠️  Config error: {e}")
            print("   (Make sure .env file is properly configured)")
        
        print("\n🎉 Core packages installed successfully!")
        print("\n✅ You're ready to start building!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_installation()