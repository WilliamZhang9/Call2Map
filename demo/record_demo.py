#!/usr/bin/env python3
"""
Demo Recording Script
Record a perfect demo call as backup for your presentation
"""

import json
from datetime import datetime

# 🎬 PERFECT DEMO SCRIPT
# This is the ideal conversation flow - practice until it's natural

DEMO_CONVERSATION = {
    "title": "Call2Map - Restaurant Search Demo",
    "duration": "2 minutes 45 seconds",
    "scenario": "Finding dinner in Palo Alto",
    "turns": [
        {
            "timestamp": "0:00",
            "speaker": "System",
            "text": "[Phone rings]"
        },
        {
            "timestamp": "0:03",
            "speaker": "AI",
            "text": "Hello! Welcome to Call 2 Map. I'm your A I assistant. I can help you find restaurants, stores, and other places near you. How can I help you today?"
        },
        {
            "timestamp": "0:15",
            "speaker": "User",
            "text": "I'm looking for sushi restaurants near McGill University",
            "notes": "Clear, natural request with location"
        },
        {
            "timestamp": "0:20",
            "speaker": "AI",
            "text": "I'll search for sushi restaurants near McGill University.",
            "technical": "Gemini extracts: query='sushi restaurants', location='McGill University'"
        },
        {
            "timestamp": "0:22",
            "speaker": "System",
            "text": "[Calling Google Maps API...]"
        },
        {
            "timestamp": "0:24",
            "speaker": "AI",
            "text": "I found 5 sushi restaurants near McGill. The top rated is Kazu on Sainte-Catherine Street, with 4.5 stars from 1200 reviews. They're open until 10 PM tonight. Would you like me to send you the full list?",
            "notes": "Mentions: name, rating, location, hours, offers SMS"
        },
        {
            "timestamp": "0:40",
            "speaker": "User",
            "text": "Yes, send me the list. And what about ones with outdoor seating?",
            "notes": "Two requests: SMS + new search with context"
        },
        {
            "timestamp": "0:45",
            "speaker": "AI",
            "text": "I've sent the details to your phone. For sushi places with outdoor seating near McGill, I recommend Jun I, rated 4.5 stars. They have a beautiful outdoor terrace and are open now.",
            "technical": "Context preserved: still searching sushi near McGill",
            "notes": "SMS sends, new search with added filter"
        },
        {
            "timestamp": "1:00",
            "speaker": "System",
            "text": "[SMS arrives on phone with formatted list]",
            "sms_content": """
Sushi Restaurants near Stanford:

1. Sushi Tomi ⭐ 4.6
   342 University Ave, Palo Alto
   Open until 10:00 PM
   (650) 555-1234

2. Miyake ⭐ 4.5
   140 University Ave
   Outdoor seating available

3. Sushi Sam ⭐ 4.7
   218 E 3rd Ave, San Mateo

View on map: https://goo.gl/maps/xyz
            """
        },
        {
            "timestamp": "1:05",
            "speaker": "User",
            "text": "Perfect! One more thing - where's the nearest ATM?",
            "notes": "Different query type, tests versatility"
        },
        {
            "timestamp": "1:10",
            "speaker": "AI",
            "text": "The nearest ATM is at TD Bank, 1410 Rue Peel, just 2 blocks from Kazu. It's available 24/7.",
            "notes": "Provides location context relative to previous result"
        },
        {
            "timestamp": "1:22",
            "speaker": "User",
            "text": "Great, thanks!",
            "notes": "Natural ending"
        },
        {
            "timestamp": "1:24",
            "speaker": "AI",
            "text": "You're welcome! Enjoy your meal at Kazu. Have a great evening!",
            "notes": "Friendly, remembers the recommendation"
        },
        {
            "timestamp": "1:30",
            "speaker": "User",
            "text": "[Hangs up]"
        }
    ]
}

# 🎯 ALTERNATIVE DEMO #2: Emergency Scenario

EMERGENCY_DEMO = {
    "title": "Call2Map - Emergency Services Demo",
    "duration": "1 minute 30 seconds",
    "scenario": "Car breakdown assistance",
    "turns": [
        {
            "speaker": "AI",
            "text": "Hello! Welcome to Call 2 Map. How can I help you today?"
        },
        {
            "speaker": "User",
            "text": "Help! My car broke down on Highway 15 near Montreal and I need a tow truck",
            "notes": "Urgent, emotional - tests AI handling"
        },
        {
            "speaker": "AI",
            "text": "I'll help you right away. Searching for 24-hour towing services near Highway 15, Montreal."
        },
        {
            "speaker": "AI",
            "text": "I found 3 tow truck services nearby. The closest is AAA Towing, available 24/7, phone number 1-800-AAA-HELP. They're 5 miles away with average 20-minute response time. I'm texting you their details and two backup options now."
        },
        {
            "speaker": "System",
            "text": "[SMS with emergency contacts sent]"
        }
    ]
}

# 🎯 ALTERNATIVE DEMO #3: Tourist Guide

TOURIST_DEMO = {
    "title": "Call2Map - Tourist Guide Demo",
    "duration": "2 minutes",
    "scenario": "First-time visitor planning",
    "turns": [
        {
            "speaker": "AI",
            "text": "Hello! Welcome to Call 2 Map. How can I help you today?"
        },
        {
            "speaker": "User",
            "text": "I'm visiting Montreal for the first time. What are the top attractions near Old Montreal?"
        },
        {
            "speaker": "AI",
            "text": "Welcome to Montreal! Near Old Montreal, the top attractions are Notre-Dame Basilica, Place Jacques-Cartier which is a 5-minute walk, and the Old Port. All are within 1 kilometer. Would you like details on any of these?"
        },
        {
            "speaker": "User",
            "text": "Tell me about Notre-Dame Basilica"
        },
        {
            "speaker": "AI",
            "text": "Notre-Dame Basilica is a stunning Gothic Revival church on Notre-Dame Street, rated 4.7 stars. It's open now until 6 PM, featuring breathtaking stained glass windows and beautiful architecture. It's about 10 minutes walk from the Old Port. Should I send you directions?"
        },
        {
            "speaker": "User",
            "text": "Yes please!"
        },
        {
            "speaker": "AI",
            "text": "I've texted you walking directions from Old Montreal to Notre-Dame Basilica, along with ticket information and nearby attractions. Enjoy your visit!"
        }
    ]
}

# 📝 DEMO RECORDING CHECKLIST

RECORDING_CHECKLIST = """
BEFORE RECORDING:
□ Test call completed successfully
□ Server running: python main.py
□ ngrok tunnel active
□ Clear, quiet environment
□ Phone charged, good signal
□ Screen recording software ready (OBS, QuickTime, etc.)
□ Practice the script 3 times

WHAT TO RECORD:
□ Terminal window showing server logs
□ Phone screen showing incoming call
□ Audio of conversation (use speaker or mixer)
□ SMS arriving (if possible)
□ Browser tab with system dashboard

RECORDING SETTINGS:
• Resolution: 1920x1080 minimum
• Frame rate: 30fps
• Audio: Clear, no echo
• Duration: 2-3 minutes
• Format: MP4 or MOV

DURING RECORDING:
□ Speak clearly and naturally
□ Wait for AI to finish responses
□ Show SMS notifications
□ Point out technical highlights

AFTER RECORDING:
□ Trim start/end
□ Add text overlays (optional):
  - "Gemini AI processing..."
  - "Google Maps API called"
  - "SMS sent"
□ Export in high quality
□ Test playback
□ Upload to backup location

BACKUP LOCATIONS:
• USB drive
• Google Drive
• Laptop hard drive
• Email to yourself
"""

# 🎥 RECORDING SCRIPT WITH PAUSES

RECORDING_SCRIPT = """
===========================================
DEMO RECORDING SCRIPT WITH TIMING
===========================================

[0:00] Start screen recording

[0:02] Show terminal with server running
       Say: "Call2Map server is running"

[0:05] Show phone screen, dial number
       Say: "I'm calling the AI assistant now"

[0:08] Wait for ring...

[0:10] AI greets you

[0:15] Say clearly:
       "I'm looking for sushi restaurants near McGill University"

[0:18] Wait for AI to process...

[0:20] AI responds with results
       HIGHLIGHT: Point out "4.5 stars" and "open until 10 PM"
[0:35] Say:
       "Send me the list and what about outdoor seating?"

[0:40] CAMERA: Switch to show SMS arriving on phone

[0:45] AI responds about outdoor seating
       HIGHLIGHT: Say "Notice it remembered I was looking for sushi"

[1:05] Say:
       "Where's the nearest ATM?"

[1:10] AI responds with ATM location
       HIGHLIGHT: "Even provides context - 2 blocks from the restaurant"

[1:25] Say:
       "Thank you!"

[1:28] AI says goodbye

[1:32] Hang up

[1:35] Show SMS on screen (zoom in)
       Say: "The SMS includes names, ratings, addresses, and map links"

[1:45] Show terminal logs (optional)
       Say: "You can see the API calls in real-time"

[1:55] End screen with:
       "Call2Map - AI for Everyone"
       [Your contact info]

[2:00] Stop recording
"""

# 💡 TIPS FOR GREAT RECORDING

RECORDING_TIPS = """
AUDIO QUALITY:
• Use external mic if possible
• Reduce background noise
• Speak toward phone mic
• Test audio levels before recording

VIDEO QUALITY:
• Good lighting
• Clean background
• Stable camera/recording
• Show relevant screens only

EDITING TIPS:
• Cut dead air
• Speed up long pauses (1.2x)
• Add subtle background music (optional)
• Include text overlays for key moments:
  - "Gemini AI Understanding..."
  - "Google Maps Searching..."
  - "SMS Sent ✓"

CALL QUALITY:
• Use WiFi, not cellular
• Quiet room
• Clear pronunciation
• Natural pacing

BACKUP PLAN:
If live recording fails:
1. Record a screen mockup with voice-over
2. Show individual components working
3. Explain what should happen

The goal: Show judges it works, even if demo fails
"""

# 🎬 EXPORT THIS CONVERSATION

def export_demo_script(demo_data, filename):
    """Export demo script to JSON for reference"""
    with open(filename, 'w') as f:
        json.dump(demo_data, f, indent=2)
    print(f"✓ Demo script exported to {filename}")

def print_script_readable(demo_data):
    """Print demo script in readable format"""
    print("\n" + "="*60)
    print(f"  {demo_data['title'].upper()}")
    print(f"  Duration: {demo_data['duration']}")
    print(f"  Scenario: {demo_data['scenario']}")
    print("="*60 + "\n")

    for turn in demo_data['turns']:
        timestamp = turn.get('timestamp', '')
        speaker = turn['speaker']
        text = turn['text']

        print(f"[{timestamp}] {speaker}:")
        print(f"  {text}")

        if 'notes' in turn:
            print(f"  💡 {turn['notes']}")

        if 'technical' in turn:
            print(f"  🔧 {turn['technical']}")

        if 'sms_content' in turn:
            print("  📱 SMS Content:")
            for line in turn['sms_content'].strip().split('\n'):
                print(f"     {line}")

        print()

if __name__ == "__main__":
    # Print all demo scripts
    print_script_readable(DEMO_CONVERSATION)
    print("\n" + "="*60 + "\n")
    print_script_readable(EMERGENCY_DEMO)
    print("\n" + "="*60 + "\n")
    print_script_readable(TOURIST_DEMO)

    # Export to JSON
    export_demo_script(DEMO_CONVERSATION, "demo_script_main.json")
    export_demo_script(EMERGENCY_DEMO, "demo_script_emergency.json")
    export_demo_script(TOURIST_DEMO, "demo_script_tourist.json")

    print("\n" + "="*60)
    print("📋 RECORDING CHECKLIST")
    print("="*60)
    print(RECORDING_CHECKLIST)

    print("\n" + "="*60)
    print("🎥 RECORDING SCRIPT")
    print("="*60)
    print(RECORDING_SCRIPT)

    print("\n" + "="*60)
    print("💡 RECORDING TIPS")
    print("="*60)
    print(RECORDING_TIPS)

    print("\n✨ Ready to record your demo! Good luck! 🎬\n")
