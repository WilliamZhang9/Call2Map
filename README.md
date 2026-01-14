# Call2Map

Voice-first AI assistant accessible via phone call. Find places, make reservations, get directions - no app required.

## Features

- **Universal Access** - Works on any phone (flip phone, landline, smartphone)
- **Google Maps** - Real-time place search with ratings, hours, and reviews
- **Restaurant Reservations** - Detects OpenTable, Resy, and other booking platforms
- **Google Gemini AI** - Natural conversation with context awareness
- **SMS Integration** - Booking links, directions, and details sent via text
- **Fast** - Sub-3 second response times

## Architecture

```
Phone → Twilio → FastAPI → Gemini AI → Google Maps → SMS
```

## Quick Start

```bash
# 1. Clone and install
git clone <your-repo>
cd Call2Map
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 3. Start server
python main.py

# 4. Start ngrok (separate terminal)
ngrok http 8000

# 5. Update Twilio webhook
# Set to: https://your-ngrok-url.ngrok.io/voice/incoming
```

### Required API Keys

| Service | Cost | Get Key |
|---------|------|---------|
| **Twilio** | ~$2/month | [twilio.com/try-twilio](https://twilio.com/try-twilio) |
| **Google Gemini** | FREE | [aistudio.google.com](https://aistudio.google.com/app/apikey) |
| **Google Maps** | Free tier | [console.cloud.google.com](https://console.cloud.google.com) |

## Usage Examples

**Find restaurants:**
```
You: "Find sushi near McGill University"
AI:  "I found Kazu, rated 4.5 stars, open until 10 PM..."
```

**Make reservations:**
```
You: "Book a table there"
AI:  "You can book online through OpenTable. I've texted you the link."
[SMS with booking URL arrives]
```

**Multi-request:**
```
You: "Where's the nearest ATM?"
AI:  "TD Bank, 1410 Rue Peel, 2 blocks away, open 24/7."
```

## Project Structure

```
Call2Map/
├── main.py              # FastAPI server
├── config.py            # Environment config
├── requirements.txt     # Dependencies
├── .env.example         # Config template
├── services/
│   ├── llm_service.py   # Google Gemini AI
│   ├── maps_service.py  # Google Maps + Reservations
│   └── sms_service.py   # Twilio SMS
├── models/
│   └── conversation.py  # Session management
├── agents/              # AI agent logic
├── utils/               # Helpers
└── demo/                # Demo scripts & documentation
    ├── HACKATHON_DEMO.md
    ├── demo_test.py
    └── README.md
```

## Key Features

### Intelligent Search
- Multi-turn conversations with context
- Natural language understanding via Gemini
- Filters by ratings, hours, distance

### Restaurant Reservations
- Detects OpenTable, Resy, Tock, SevenRooms
- Sends booking URLs via SMS
- Phone fallback for restaurants without online booking

### Smart SMS
- Formatted place lists with ratings
- Direct booking links
- Google Maps directions

## Cost Estimate

**Monthly (1000 calls):**
- Twilio: ~$45
- Gemini: FREE
- Maps API: ~$35
- **Total: ~$80**

## Troubleshooting

**Server won't start:**
```bash
python demo/demo_test.py  # Test all APIs
```

**Twilio webhook fails:**
- Check ngrok is running: `ngrok http 8000`
- Update BASE_URL in `.env`
- Check Twilio webhook URL matches ngrok

**View logs:**
- Server: Console output from `python main.py`
- Twilio: [console.twilio.com/monitor/logs/calls](https://console.twilio.com/monitor/logs/calls)
- ngrok: [http://127.0.0.1:4040](http://127.0.0.1:4040)

## Documentation

- **[demo/HACKATHON_DEMO.md](demo/HACKATHON_DEMO.md)** - Complete demo script
- **[demo/RESERVATION_FEATURE.md](demo/RESERVATION_FEATURE.md)** - Reservation system docs
- **[QUICKSTART.md](QUICKSTART.md)** - Detailed setup guide
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues

## Tech Stack

- **Backend:** FastAPI (Python 3.11+)
- **AI:** Google Gemini 2.5 Flash
- **Maps:** Google Maps Places API
- **Voice:** Twilio Voice + Speech Recognition
- **SMS:** Twilio Messaging

## Contributing

Hackathon project - feel free to fork and extend!

## License

MIT License

---

**Built for voice-first AI accessibility**
