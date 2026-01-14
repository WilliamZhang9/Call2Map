# ⚡ Quick Start Guide

Get Call2Map running in 10 minutes!

## Step 1: Install Dependencies (2 min)

```bash
# Navigate to project
cd call2map_complete

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

## Step 2: Get API Keys (5 min)

### Twilio (Required)
1. Go to: https://www.twilio.com/try-twilio
2. Sign up (free $15 credit)
3. Get:
   - Account SID
   - Auth Token
4. Buy a phone number ($1): Console → Phone Numbers → Buy

### Google Gemini (Required - FREE!)
1. Go to: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy it (starts with `AIza`)
4. **Note:** Gemini is completely FREE for development!

### Google Maps (Required)
1. Go to: https://console.cloud.google.com/
2. Create project
3. Enable: Places API, Geocoding API
4. Create API Key

## Step 3: Configure (1 min)

```bash
# Copy template
cp .env.example .env

# Edit .env file and add your keys
```

Your `.env` should look like:
```bash
TWILIO_ACCOUNT_SID=AC1234567890abcdef...
TWILIO_AUTH_TOKEN=1234567890abcdef...
TWILIO_PHONE_NUMBER=+15551234567
GEMINI_API_KEY=AIzaSyAbc123...
GOOGLE_MAPS_API_KEY=AIzaSyAbc123...
BASE_URL=http://localhost:8000
```

## Step 4: Start Server (30 sec)

```bash
python main.py
```

You should see:
```
🚀 Starting Call2Map Server
📞 Phone Number: +15551234567
```

## Step 5: Start ngrok (30 sec)

**In a NEW terminal:**
```bash
ngrok http 8000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

## Step 6: Update Configuration (30 sec)

1. **Update .env**
   ```bash
   BASE_URL=https://abc123.ngrok.io
   ```

2. **Restart server** (Ctrl+C, then `python main.py`)

3. **Configure Twilio**
   - Go to: https://console.twilio.com/
   - Phone Numbers → Your Number
   - "A CALL COMES IN" → Webhook
   - URL: `https://abc123.ngrok.io/voice/incoming`
   - Save

## Step 7: Test! (30 sec)

**Call your Twilio phone number!**

Try saying:
- "Find me coffee shops in Seattle"
- "Where's the nearest gas station?"
- "I'm looking for Italian restaurants"

## 🎉 Success Checklist

- [ ] Server running without errors
- [ ] ngrok showing forwarding URL
- [ ] .env has all API keys filled in
- [ ] Twilio webhook configured
- [ ] Test call connects and AI responds

## 🆘 Common Issues

**Issue: "Module not found"**
```bash
pip install -r requirements.txt
```

**Issue: "Field required" error**
```bash
# Make sure .env exists and has all required fields
python tests/test_config.py
```

**Issue: Call connects but no response**
- Check server logs for errors
- Verify ngrok URL matches Twilio webhook
- Check Twilio console for error logs

**Issue: Port 8000 in use**
```bash
# Change port in .env
PORT=8001
# Update ngrok: ngrok http 8001
```

## 📞 What to Say

Good test phrases:
- ✅ "Find sushi restaurants near downtown Seattle"
- ✅ "I need a gas station"
- ✅ "Where can I get coffee in San Francisco?"
- ✅ "Search for pharmacies near me" (AI will ask for location)

## 🎯 Next Steps

Once working:
1. Try different searches
2. Test SMS delivery
3. Experiment with conversation flow
4. Review logs to debug issues
5. Customize prompts in `services/llm_service.py`

---

**You're ready! Pick up your phone and call! 🚀**
