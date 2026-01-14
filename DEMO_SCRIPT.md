# 🎬 Demo Script for Call2Map

## Pre-Demo Checklist

### 1. System Setup
- [ ] Server running: `python main.py`
- [ ] ngrok running: `ngrok http 8000`
- [ ] .env configured with all API keys
- [ ] Twilio webhook updated with ngrok URL
- [ ] Test call completed successfully

### 2. Presentation Setup
- [ ] Phone on speaker mode
- [ ] Screen sharing server logs
- [ ] Browser tab with ngrok dashboard (http://127.0.0.1:4040)
- [ ] Browser tab with Twilio console (for backup)
- [ ] Backup phone for redundancy

### 3. Materials Ready
- [ ] Printed phone number (large font)
- [ ] Presentation slides (if any)
- [ ] Backup video recording (in case live demo fails)

## 📱 Demo Flow (3-5 minutes)

### Opening (30 seconds)
**Say to audience:**
> "Call2Map is an AI voice assistant accessible via phone call. No app installation, no screen required - just dial a number and talk. Let me show you."

**Action:**
- Display phone number on screen
- Call the number on speaker

### Demo 1: Restaurant Search (90 seconds)

**Call connects, AI greets**

**You say:**
> "Find me sushi restaurants in Palo Alto"

**Expected AI response:**
> "I'll search for sushi restaurants in Palo Alto."
> [pause]
> "I found several options. The top-rated is Sushi Sam, with 4.7 stars..."

**You say:**
> "Send me the list"

**Expected AI response:**
> "I've sent the details to your phone."

**Show to audience:**
- Display SMS arrival on screen
- Show formatted list with names, ratings, addresses

### Demo 2: Quick Query (45 seconds)

**You say:**
> "Where's the nearest Starbucks?"

**Expected AI response:**
> "The nearest Starbucks is at 123 University Avenue, about 0.5 miles away, currently open."

### Demo 3: Location-Based Search (45 seconds)

**You say:**
> "I need a pharmacy"

**Expected AI response:**
> "I'd be happy to help! What's your location?"

**You say:**
> "San Francisco 94102"

**Expected AI response:**
> "I found 3 pharmacies nearby. The closest is Walgreens on Market Street..."

### Closing (30 seconds)

**Hang up the call**

**Say to audience:**
> "That's Call2Map - AI-powered location intelligence accessible from any phone. It uses Twilio for telephony, GPT-4 for conversation, and Google Maps for real-time data. Perfect for hands-free navigation, elderly users, or anyone without a smartphone."

## 🎯 Key Points to Emphasize

1. **Accessibility**: Works on any phone, no app needed
2. **Conversational**: Natural language, context-aware
3. **Practical**: Real-time data from Google Maps
4. **Multi-modal**: Voice + SMS for best experience
5. **Fast**: Sub-3 second response times

## 📊 Architecture Slide (if presenting)

Show diagram:
```
Phone → Twilio → FastAPI Backend → OpenAI GPT-4
                                   ↓
                              Google Maps API
                                   ↓
                              SMS Response
```

## 💡 Use Cases to Mention

1. **Elderly users** without smartphones
2. **Driving scenarios** (hands-free)
3. **Low connectivity** areas (voice-only)
4. **Emergency situations** (dead phone battery)
5. **Quick lookups** without opening apps

## 🆘 Backup Plan (If Live Demo Fails)

### Plan A: Use pre-recorded video
- Have a 2-minute video of successful demo
- Explain technical difficulties
- Show logs/architecture instead

### Plan B: Show different part
- Walk through code architecture
- Show server logs from previous successful calls
- Demonstrate webhook configuration

### Plan C: Focus on concept
- Explain the innovation
- Show mock flow diagrams
- Discuss technical challenges solved

## 📝 Q&A Preparation

### Expected Questions:

**Q: How do you handle multiple concurrent calls?**
A: Each call gets its own session in memory, identified by Twilio's CallSid. For production, we'd use Redis for distributed session management.

**Q: What about privacy/security?**
A: No conversation data is stored. Sessions are cleared when calls end. For production, we'd add encryption and compliance features.

**Q: How accurate is the speech recognition?**
A: We use Twilio's built-in STT which has 95%+ accuracy. For production, we could integrate Deepgram for even better results.

**Q: What's the latency?**
A: Typically 1.5-3 seconds from speech to response. Breakdown: STT (300ms) + LLM (800ms) + TTS (400ms) + network (200ms).

**Q: Can it handle complex conversations?**
A: Yes! The LLM maintains context for the entire call session. It can handle follow-up questions and multi-turn dialogues.

**Q: What if the user's location is unknown?**
A: The AI will politely ask for it: "I'd be happy to help! What's your location or zip code?"

**Q: Does it work internationally?**
A: Yes! Twilio supports 100+ countries. Just need to buy a local number and configure it.

**Q: How much does it cost to run?**
A: Development: ~$5. Production (1000 calls): ~$110/month. Breakdown in README.

## 🎬 Timing

- Setup: 30 seconds
- Demo 1 (Restaurant): 90 seconds
- Demo 2 (Quick query): 45 seconds
- Demo 3 (Location-based): 45 seconds
- Closing: 30 seconds
- **Total: 4 minutes**
- Leave 1 minute buffer for technical issues

## ✅ Success Metrics

Demo is successful if:
- [ ] Call connects immediately
- [ ] AI responds clearly and accurately
- [ ] Maps search returns relevant results
- [ ] SMS is received
- [ ] No errors in server logs
- [ ] Audience engagement (questions, interest)

## 🎤 Speaking Tips

1. **Speak clearly** into the phone (AI is listening!)
2. **Pause** after AI asks questions
3. **Maintain energy** - this should be exciting!
4. **Handle errors gracefully** - "Let me try that again"
5. **Engage audience** - "Notice how it understood..."

## 📞 Emergency Contact

If demo fails completely:
1. Stay calm
2. Switch to backup plan
3. Acknowledge the issue honestly
4. Focus on concept and technical achievement
5. Offer to show working version later

---

**Practice this flow 2-3 times before presenting!** 🚀

Good luck! You've built something awesome! 🎉