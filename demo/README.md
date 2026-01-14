# 🎯 Call2Map Demo Resources

All demo-related files for your hackathon presentation.

## 📁 Files in This Folder

### Main Demo Guides
- **[HACKATHON_DEMO.md](HACKATHON_DEMO.md)** - Complete hackathon demo script with 4 acts and technical breakdown
- **[DEMO_SCRIPT.md](DEMO_SCRIPT.md)** - Original demo script with timing and flow
- **[DEMO_CHEATSHEET.py](DEMO_CHEATSHEET.py)** - Quick reference queries and pro tips

### Presentation Materials
- **[PRESENTATION_DECK.md](PRESENTATION_DECK.md)** - Full slide deck content for your presentation
- **[record_demo.py](record_demo.py)** - Scripts for recording backup demo videos

### Feature Documentation
- **[RESERVATION_FEATURE.md](RESERVATION_FEATURE.md)** - Detailed technical docs on reservation system
- **[RESERVATION_SUMMARY.md](RESERVATION_SUMMARY.md)** - Quick summary of reservation integration

### Testing
- **[demo_test.py](demo_test.py)** - Test script to verify all APIs work before demo

## 🚀 Quick Start

### 1. Review Demo Script
```bash
cat HACKATHON_DEMO.md
```

### 2. Test Your System
```bash
python3 demo_test.py
```

### 3. Practice Queries
Check `DEMO_CHEATSHEET.py` for tested queries that work well.

## 🎤 Demo Flow (3 minutes)

1. **Act 1** (60s): Find restaurants near McGill
2. **Act 2** (30s): Context-aware follow-up (outdoor seating)
3. **Act 3** (30s): Multi-request (ATM + SMS)
4. **Act 4** (45s): Restaurant reservation booking

## 📞 Test Queries for Montreal/McGill

```
✅ "Find sushi restaurants near McGill University"
✅ "What about something with outdoor seating?"
✅ "Book a table at Kazu"
✅ "Where's the nearest ATM?"
✅ "Find pizza places in Montreal downtown"
```

## 🏆 Key Features to Highlight

1. **Voice-First Interface** - Works on any phone
2. **Context Awareness** - Remembers previous searches
3. **Google Integration** - Gemini + Maps APIs
4. **Smart Reservations** - Detects OpenTable, Resy, etc.
5. **Multi-Modal** - Voice + SMS responses

## 💡 Pro Tips

- Test your demo at least 3 times before presenting
- Have backup video ready (use `record_demo.py`)
- Show SMS arriving on screen during demo
- Speak clearly for Twilio's speech recognition
- Emphasize the accessibility angle

## 📊 Files by Purpose

**Before Demo:**
- `demo_test.py` - Verify everything works
- `DEMO_CHEATSHEET.py` - Review query options

**During Demo:**
- `HACKATHON_DEMO.md` - Follow this script
- `PRESENTATION_DECK.md` - Slide content

**For Judges:**
- `RESERVATION_FEATURE.md` - Technical deep dive
- `RESERVATION_SUMMARY.md` - Quick feature overview

## 🎬 Recording Backup

If you want to record a backup demo video:

```bash
python3 record_demo.py
```

This will print detailed recording instructions.

---

**Good luck with your demo! 🚀**
