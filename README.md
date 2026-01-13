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
