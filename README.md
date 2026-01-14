# Call2Map

AI-powered voice mapping service using Twilio, OpenAI, and Google Maps.

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables**
   ```bash
   # Copy the example file and add your actual credentials
   cp .env.example .env
   ```

   Then edit `.env` with your actual API keys (this file is gitignored and won't be committed)

3. **Run the server**
   ```bash
   python main.py
   ```

4. **Configure Twilio webhook** to `https://your-server-url.com/voice`

## Features

- Voice call handling with Twilio
- Natural language processing with OpenAI
- Location services via Google Maps
- Real-time WebSocket communication

## Project Structure

```
Call2Map/
├── main.py          # Entry point
├── config.py        # Settings
├── agents/          # AI logic
├── services/        # External APIs
├── models/          # Data schemas
└── utils/           # Helpers
```

## Requirements

- Python 3.8+
- Twilio account
- OpenAI API key
- Google Maps API key
# 🎙️ Call2Map - AI Voice Assistant via Phone Call

Call a phone number, get instant AI-powered place recommendations and information through natural conversation. No app required!

## 🌟 Features

- **📞 Phone-Based Interface**: Call a number, talk to AI - no app installation needed
- **🗺️ Google Maps Integration**: Find restaurants, stores, and services nearby
- **💬 Natural Conversation**: Powered by Google Gemini with context awareness
- **📱 SMS Follow-up**: Get detailed results sent to your phone
- **🎯 Location-Aware**: Searches based on your location
- **🚀 Real-time Processing**: Fast response times using Twilio's speech recognition

## 🏗️ Architecture

```
User's Phone → Twilio → FastAPI Backend → Google Gemini AI
                                        ↓
                                   Google Maps API
                                        ↓
                                   Response → SMS (optional)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Twilio account (free trial available)
- Google Gemini API key (FREE!)
- Google Maps API key
- ngrok (for local development)

### Installation

1. **Clone and setup**
```bash
cd call2Map
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

2. **Configure environment**
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your API keys
# - Twilio Account SID, Auth Token, Phone Number
# - OpenAI API Key
# - Google Maps API Key
```

3. **Test configuration**
```bash
python tests/test_installation.py
python tests/test_config.py
```

4. **Start server**
```bash
python main.py
```

5. **Start ngrok (in another terminal)**
```bash
ngrok http 8000
```

6. **Configure Twilio webhook**
- Go to Twilio Console → Phone Numbers
- Click your number
- Set "A CALL COMES IN" webhook to:
  `https://your-ngrok-url.ngrok.io/voice/incoming`

## 📱 Usage Examples

### Example 1: Find Restaurants
```
You: "Find me Italian restaurants nearby"
AI: "I'd be happy to help! What's your location?"
You: "San Francisco"
AI: "I found 3 Italian restaurants. The top-rated is Bella Vita..."
```

### Example 2: Quick Search
```
You: "Where's the nearest gas station?"
AI: "The nearest gas station is Shell on Main Street, 0.3 miles away."
```

### Example 3: Get Details via SMS
```
You: "Find coffee shops in Seattle"
AI: "I found 5 coffee shops. Would you like me to text you the details?"
You: "Yes"
AI: "I've sent the list to your phone!"
[SMS arrives with formatted results]
```

## 🔧 Configuration

### Required Environment Variables

```bash
# Twilio
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Google Gemini (FREE!)
GEMINI_API_KEY=your_gemini_key_here

# Google Maps
GOOGLE_MAPS_API_KEY=your_maps_key

# Server
BASE_URL=https://your-ngrok-url.ngrok.io
PORT=8000
```

### Optional Configuration

```bash
# Deepgram (for advanced STT - not implemented in basic version)
DEEPGRAM_API_KEY=your_deepgram_key

# Redis (for session management - not implemented in basic version)
REDIS_URL=redis://localhost:6379
```

## 📂 Project Structure

```
call2Map/
├── main.py                 # FastAPI application
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
│
├── services/              # Business logic
│   ├── llm_service.py    # OpenAI integration
│   ├── maps_service.py   # Google Maps integration
│   └── sms_service.py    # SMS sending
│
├── models/                # Data models
│   └── conversation.py   # Call session models
│
├── utils/                 # Utilities
│   └── audio_processing.py  # Audio format conversion
│
└── tests/                 # Test scripts
    ├── test_config.py
    └── test_installation.py
```

## 🧪 Testing

```bash
# Test package installation
python tests/test_installation.py

# Test configuration
python tests/test_config.py

# Test server locally
curl http://localhost:8000
```

## 🐛 Troubleshooting

### Server won't start
- Check that all environment variables are set in `.env`
- Verify Python version: `python --version` (needs 3.11+)
- Check port 8000 is not in use: `netstat -ano | findstr :8000`

### Twilio webhook not working
- Ensure ngrok is running: `ngrok http 8000`
- Update BASE_URL in `.env` with ngrok URL
- Update Twilio webhook with correct ngrok URL
- Check server logs for incoming requests

### No audio/speech recognition
- Twilio's speech recognition is automatic
- Check Twilio console for call logs
- Verify webhook URL is correct
- Check server logs for errors

### API errors
- Verify all API keys are correct
- Check API quotas (OpenAI, Google Maps)
- Review server logs for detailed error messages

## 💰 Cost Estimates

### Development/Testing
- Twilio: ~$2-5 (50 test calls)
- Google Gemini: **$0 (FREE!)**
- Google Maps: $0 (under free tier)
- **Total: ~$2-5**

### Production (1000 calls/month)
- Twilio: ~$45
- Google Gemini: **$0 (FREE up to 15 RPM)**
- Google Maps: ~$35
- **Total: ~$80/month**

## 🎯 API Keys Setup

### Twilio
1. Sign up: https://www.twilio.com/try-twilio
2. Get Account SID and Auth Token from dashboard
3. Buy a phone number with Voice capability

### Google Gemini (FREE!)
1. Go to: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key (starts with `AIza`)
4. No payment method required!

### Google Maps
1. Go to: https://console.cloud.google.com/
2. Create new project
3. Enable "Places API" and "Geocoding API"
4. Create credentials → API Key

## 📝 Features Roadmap

- [x] Basic phone call handling
- [x] Speech-to-text via Twilio
- [x] LLM integration with function calling
- [x] Google Maps place search
- [x] SMS results delivery
- [ ] Real-time audio streaming (LiveKit)
- [ ] Advanced STT with Deepgram
- [ ] Multi-turn conversation memory
- [ ] User preferences storage
- [ ] Voice customization

## 🤝 Contributing

This is a hackathon project. Feel free to fork and extend!

## 📄 License

MIT License - feel free to use for your own projects

## 🙏 Acknowledgments

- Twilio for phone infrastructure
- Google Gemini for free AI capabilities
- Google Maps for location data
- FastAPI for the web framework

## 📧 Support

For issues, please check:
1. Server logs: `python main.py` output
2. Twilio console: Call logs and errors
3. ngrok dashboard: http://127.0.0.1:4040

---

Built with ❤️ for voice-first AI interactions
