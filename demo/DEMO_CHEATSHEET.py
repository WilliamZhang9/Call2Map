"""
Quick Demo Queries - Copy/paste these for consistent results
"""

# 🎯 WINNING DEMO QUERIES
# Copy these exact phrases for your demo

DEMO_QUERIES = {
    "Act 1 - The Hook": [
        "Find highly rated sushi restaurants near McGill University",
        # Expected: Shows top results with ratings, open status
        # Impressive: Multi-criteria filtering (location + cuisine + quality)
    ],

    "Act 2 - Context Awareness": [
        "What about something with outdoor seating?",
        # Expected: AI remembers "sushi" and "McGill" from previous query
        # Impressive: No need to repeat - shows context intelligence
    ],

    "Act 3 - Complex Query": [
        "I need a 24-hour pharmacy and the nearest ATM in San Francisco downtown",
        # Expected: Handles multiple requests in one query
        # Impressive: Parallel processing of different place types
    ],

    "Act 4 - The Show-Stopper": [
        "Book a table at Kazu",
        # Expected: Provides OpenTable link + phone number via SMS
        # Impressive: Intelligent reservation routing (online vs phone)
    ],

    "Act 5 - Multi-Request" : [
        "Find me the best coffee shop in Montreal downtown with WiFi, good for meetings, send me directions",
        # Expected: Search + filter + SMS + directions
        # Impressive: Multi-modal response (voice + text)
    ],

    "Bonus - Emergency Scenario": [
        "My car broke down on Highway 15 near Montreal, I need a tow truck",
        # Expected: 24/7 towing services with phone numbers
        # Impressive: Real-world emergency use case
    ]
}

# 🎬 BACKUP QUERIES (if primary fails)
BACKUP_QUERIES = [
    "Where's the nearest Tim Hortons?",
    "Find pizza places in Montreal downtown",
    "Book a table at Jun I",
    "I need a gas station",
    "Show me gyms near McGill",
]

# 📍 TESTED LOCATIONS (known to return good results)
GOOD_LOCATIONS = [
    "Montreal, QC",
    "McGill University",
    "Montreal downtown",
    "Old Montreal",
    "Plateau Mont-Royal",
]

# 🔥 JUDGE-IMPRESSING FEATURES TO HIGHLIGHT

"""
During your demo, casually mention these technical achievements:

1. "Notice it remembered my location from the previous question"
   → Shows: Context preservation across conversation turns

2. "The AI extracted 'open now' even though I didn't say it explicitly"
   → Shows: Intelligent inference (it's evening, so filter by open_now=true)

3. "It automatically detected this restaurant uses OpenTable for bookings"
   → Shows: Smart platform detection from Google Maps data

4. "It's using Google's Gemini 2.5 Flash - which is actually free"
   → Shows: Cost-efficient architecture

5. "Response time under 3 seconds including Maps API call"
   → Shows: Performance optimization

6. "Works on any phone - flip phone, landline, anything"
   → Shows: True accessibility, low barrier to entry

7. "The SMS includes a direct booking link, phone number, AND map"
   → Shows: Multi-modal user experience

8. "All conversation is stored in-session, so follow-ups work naturally"
   → Shows: Stateful design for better UX

9. "It can handle both online reservations and phone-based booking"
   → Shows: Intelligent routing based on availability
"""

# 💡 PRO TIPS FOR DEMO

"""
1. PHONE SETUP:
   - Use speaker mode or connect to laptop audio
   - Make sure room is quiet (Twilio speech-to-text is sensitive)
   - Have backup phone ready

2. PACING:
   - Speak clearly and not too fast
   - Pause after each response to let AI finish
   - Wait for the "beep" before speaking

3. WHAT TO SHOW ON SCREEN:
   ┌────────────────────────────────┐
   │ Terminal: Server Logs          │  ← Show API calls happening
   │                                 │
   │ Browser: SMS arrives            │  ← Prove SMS works
   │                                 │
   │ ngrok Dashboard (optional)      │  ← Show request flow
   └────────────────────────────────┘

4. IF SOMETHING FAILS:
   - Have backup video ready
   - Blame the WiFi with humor: "Even AI needs good WiFi!"
   - Switch to test_installation.py demo (shows working components)

5. CONFIDENT BODY LANGUAGE:
   - Stand while presenting
   - Make eye contact with judges
   - Smile when AI responds correctly (shows confidence)
"""

# 🎯 TIME-BOXED DEMO SCRIPT (3 minutes)

"""
0:00 - 0:30  Opening
           "I'm going to call our AI assistant right now..."
           [Dial number on speaker]

0:30 - 1:30  Complex Query Demo
           "Find sushi restaurants near McGill"
           Wait for response...
           "What about ones with outdoor seating?"
           [Shows context awareness]

1:30 - 2:15  Practical Use Case
           "I also need to find an ATM"
           Wait for response...
           "Send me the details"
           [Show SMS arriving on screen]

2:15 - 2:45  Quick Queries (show speed)
           "Where's the nearest Starbucks?"
           [Fast response]

2:45 - 3:00  Closing
           "Thank you!"
           Hang up.
           "That's Call2Map - AI location intelligence for everyone."
"""

# 🔧 PRE-DEMO CHECKLIST

"""
□ Server running: python main.py
□ ngrok tunnel: ngrok http 8000
□ Twilio webhook updated with ngrok URL
□ .env file has all API keys
□ Test call completed successfully
□ Phone charged and on speaker
□ Backup video recorded
□ Screen sharing ready
□ Know the phone number by heart
□ Practiced demo 3 times
□ Water nearby (for voice)
"""

# 📞 TEST COMMAND
# Run this to verify everything works before going on stage:
# python demo_test.py

# 🎤 ELEVATOR PITCH (if asked)
"""
"Call2Map makes AI accessible to the 3 billion people with basic phones.
By combining Google Gemini for natural language understanding and Google Maps
for location intelligence, anyone can call a number and have an intelligent
conversation to find places nearby. No smartphone, no app, no barrier."
"""

# 🏆 WINNING FACTORS

"""
Why judges will love this:

✓ Solves REAL problem (accessibility)
✓ Uses Google APIs as core functionality (not just add-on)
✓ Technical complexity (multi-turn conversations, API orchestration)
✓ Production-ready (error handling, SMS fallback)
✓ Live demo (more impressive than slides)
✓ Social impact (helps elderly, low-income, rural users)
✓ Scalable architecture (async, stateless)
✓ Cost-effective (Gemini is FREE!)
"""
