# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### "Module not found" errors
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --upgrade
```

#### "Cannot install pydantic" / Rust errors
```bash
# Solution: Install with pre-built wheels
pip install --only-binary=:all: pydantic==2.5.0
pip install --only-binary=:all: pydantic-settings==2.1.0
```

#### "pyaudioop not found"
```bash
# Solution: Install pyaudioop separately
pip install pyaudioop

# If that fails, it's optional - the project will work without it
```

---

### Configuration Issues

#### "Field required" error when starting server
**Problem:** `.env` file missing or incomplete

**Solution:**
```bash
# 1. Check if .env exists
ls -la .env  # Unix/Mac
dir .env     # Windows

# 2. If missing, copy from example
cp .env.example .env  # Unix/Mac
copy .env.example .env  # Windows

# 3. Fill in all required fields
# 4. Test configuration
python tests/test_config.py
```

#### "Could not load .env file"
**Problem:** File encoding or location issue

**Solution:**
- Ensure .env is in project root (same folder as main.py)
- Check file encoding is UTF-8
- Remove any BOM markers
- Make sure no spaces around = signs

---

### Server Issues

#### "Port 8000 already in use"
**Problem:** Another process using port 8000

**Solution (Windows):**
```bash
# Find process
netstat -ano | findstr :8000

# Kill process (replace PID with actual number)
taskkill /PID <PID> /F

# Or change port in .env
PORT=8001
```

**Solution (Unix/Mac):**
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9

# Or change port in .env
PORT=8001
```

#### Server starts but shows errors in logs
**Check:**
1. All API keys are correct
2. API keys have no extra spaces
3. Phone number includes country code (+1...)
4. Run test_config.py to verify

---

### ngrok Issues

#### "ngrok: command not found"
**Problem:** ngrok not installed or not in PATH

**Solution (Windows):**
```bash
# Install via chocolatey
choco install ngrok

# Or download manually from https://ngrok.com/download
# Extract and add to PATH
```

**Solution (Mac):**
```bash
brew install ngrok
```

**Solution (Linux):**
```bash
sudo snap install ngrok
```

#### ngrok tunnel dies/disconnects
**Problem:** Free tier timeout (2 hours)

**Solution:**
- Sign up for ngrok account
- Authenticate: `ngrok config add-authtoken YOUR_TOKEN`
- Free authenticated accounts have 8-hour sessions

#### Can't access ngrok URL
**Check:**
1. Server is running (`python main.py`)
2. ngrok is pointing to correct port (8000)
3. URL format is https:// (not http://)
4. No firewall blocking connections

---

### Twilio Issues

#### Webhook returns 404 or 500
**Check:**
1. ngrok URL is correct in Twilio console
2. URL includes /voice/incoming endpoint
3. Server is actually running
4. Check server logs for errors

**Correct format:**
```
https://abc123.ngrok.io/voice/incoming
```

**Not:**
```
http://abc123.ngrok.io/voice/incoming  ❌ (http not https)
https://abc123.ngrok.io                ❌ (missing endpoint)
https://abc123.ngrok.io/voice          ❌ (wrong endpoint)
```

#### Call connects but no speech recognition
**Problem:** Twilio configuration issue

**Solution:**
- Check TwiML includes `<Gather input="speech">`
- Verify webhook is set to POST (not GET)
- Check Twilio call logs for errors
- Test with simple phrase: "hello"

#### "Invalid phone number" errors
**Check:**
- Number includes country code: `+15551234567` ✅
- Number doesn't have spaces or dashes
- Number doesn't start with just `1` (needs `+1`)

---

### API Issues

#### Google Gemini API errors
**Problem:** Rate limit or invalid key

**Solution:**
```bash
# Check quota: https://aistudio.google.com/app/apikey
# Verify key: should start with AIza
# Check key has no extra spaces in .env
# Free tier: 15 requests per minute
# If you need more: Enable billing for 1000 RPM
```

#### Google Maps returns no results
**Problem:** API not enabled or quota exceeded

**Solution:**
1. Go to Google Cloud Console
2. Enable "Places API" and "Geocoding API"
3. Check API key restrictions
4. Verify $200 free credit available

#### "API key not valid"
**Solution:**
- Copy key again (don't type it)
- Check for invisible characters
- Ensure no quotes around key in .env
- Verify key is for correct project

---

### Call Quality Issues

#### High latency (>5 seconds)
**Possible causes:**
- Slow internet connection
- Google Gemini API slow response
- Google Maps API slow response

**Solutions:**
- Check internet speed
- Gemini 1.5 Flash is already optimized for speed
- Reduce conversation history size
- Cache common searches

#### Speech not recognized accurately
**Solutions:**
- Speak clearly and slowly
- Reduce background noise
- Use specific terms ("sushi restaurant" not "place to eat")
- Check Twilio console for transcription

#### Robot-sounding voice
**Normal:** Twilio's built-in TTS is basic

**To improve (future):**
- Integrate ElevenLabs
- Use OpenAI TTS
- Customize voice parameters

---

### Development Issues

#### Changes not taking effect
**Solution:**
```bash
# Restart server (it should auto-reload with uvicorn)
# If not, stop (Ctrl+C) and restart
python main.py
```

#### Can't test locally (no ngrok)
**Alternative:**
- Deploy to Railway/Render/Heroku
- Use localtunnel: `npm install -g localtunnel`
- Use serveo: `ssh -R 80:localhost:8000 serveo.net`

#### Virtual environment issues
**Solution:**
```bash
# Deactivate and recreate
deactivate
rm -rf venv  # Unix/Mac
Remove-Item -Recurse -Force venv  # Windows

python -m venv venv
source venv/bin/activate  # Unix/Mac
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

---

## Debugging Tips

### Enable detailed logging
```python
# In main.py, change:
logging.basicConfig(level=logging.DEBUG)  # Instead of INFO
```

### Check Twilio logs
1. Go to https://console.twilio.com/
2. Monitor → Logs → Calls
3. Click on your call
4. Check for errors and warnings

### Check ngrok requests
- Open: http://127.0.0.1:4040
- See all requests/responses
- Replay requests for debugging

### Test API keys individually
```python
# test_apis.py
from config import get_settings
from google import genai
from google.genai import types
import googlemaps

settings = get_settings()

# Test Google Gemini
try:
    client = genai.Client(api_key=settings.gemini_api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents="Say hello"
    )
    print("✅ Gemini working:", response.text)
except Exception as e:
    print("❌ Gemini error:", e)

# Test Google Maps
try:
    gmaps = googlemaps.Client(key=settings.google_maps_api_key)
    result = gmaps.geocode("San Francisco")
    print("✅ Google Maps working:", result[0]['formatted_address'])
except Exception as e:
    print("❌ Google Maps error:", e)
```

---

## Still Having Issues?

### Check These Resources:
1. Server logs: `python main.py` output
2. Twilio console: https://console.twilio.com/
3. ngrok dashboard: http://127.0.0.1:4040
4. Project README.md
5. QUICKSTART.md guide

### Gather Debug Info:
```bash
# Python version
python --version

# Installed packages
pip list

# Environment check
python tests/test_installation.py
python tests/test_config.py

# Server test
curl http://localhost:8000
```

### Report Issue:
Include:
- Error message (full traceback)
- Server logs
- Twilio call logs
- Steps to reproduce
- Python version
- Operating system

---

**Most issues are configuration-related. Double-check your .env file!** 🔍
