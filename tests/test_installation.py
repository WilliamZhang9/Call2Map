# tests/test_installation.py
"""Test that all required packages are installed"""

def test_installation():
    print("Testing package installation...\n")
    
    packages = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'pydantic': 'Pydantic',
        'dotenv': 'Python-dotenv',
        'twilio': 'Twilio',
        'openai': 'OpenAI',
        'googlemaps': 'Google Maps',
        'aiohttp': 'AioHTTP',
        'websockets': 'WebSockets'
    }
    
    success = True
    
    for package, name in packages.items():
        try:
            if package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"✅ {name}")
        except ImportError as e:
            print(f"❌ {name}: Not installed")
            success = False
    
    if success:
        print("\n🎉 All packages installed successfully!")
        print("\nNext steps:")
        print("1. Copy .env.example to .env")
        print("2. Fill in your API keys")
        print("3. Run: python main.py")
    else:
        print("\n❌ Some packages are missing")
        print("Run: pip install -r requirements.txt")
    
    return success

if __name__ == "__main__":
    test_installation()
