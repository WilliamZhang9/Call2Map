#!/usr/bin/env python3
"""
Demo Test Script - Verify all Google APIs are working
Run this before your hackathon demo to ensure everything is ready!
"""

import asyncio
import sys
from config import get_settings
from services.llm_service import LLMService
from services.maps_service import MapsService
from services.sms_service import sms_service
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(msg):
    print(f"{GREEN}✓ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}✗ {msg}{RESET}")

def print_info(msg):
    print(f"{BLUE}ℹ {msg}{RESET}")

def print_warning(msg):
    print(f"{YELLOW}⚠ {msg}{RESET}")

async def test_gemini_api():
    """Test Google Gemini API"""
    print_info("Testing Google Gemini API...")

    try:
        settings = get_settings()
        llm_service = LLMService(settings.gemini_api_key)

        # Test query
        response = await llm_service.process_message(
            user_message="Find sushi restaurants in Palo Alto",
            conversation_history=[],
            session_id="test"
        )

        if response and response.get('type') == 'function_call':
            print_success("Gemini API is working!")
            print_info(f"  Extracted query: {response['function_args'].get('query')}")
            print_info(f"  Extracted location: {response['function_args'].get('location')}")
            return True
        else:
            print_error("Gemini API returned unexpected response")
            return False

    except Exception as e:
        print_error(f"Gemini API test failed: {e}")
        return False

def test_maps_api():
    """Test Google Maps API"""
    print_info("Testing Google Maps API...")

    try:
        settings = get_settings()
        maps_service = MapsService(settings.google_maps_api_key)

        # Test search
        results = maps_service.search_places(
            query="sushi restaurant",
            location="Montreal, QC"
        )

        if results and len(results) > 0:
            print_success("Google Maps API is working!")
            print_info(f"  Found {len(results)} places")
            print_info(f"  Top result: {results[0]['name']}")
            if results[0].get('rating'):
                print_info(f"  Rating: {results[0]['rating']} stars")
            return True
        else:
            print_error("No results from Google Maps API")
            return False

    except Exception as e:
        print_error(f"Maps API test failed: {e}")
        return False

def test_geocoding():
    """Test Google Geocoding API"""
    print_info("Testing Google Geocoding API...")

    try:
        settings = get_settings()
        maps_service = MapsService(settings.google_maps_api_key)

        # Test geocoding
        result = maps_service.geocode_address("McGill University, Montreal")

        if result:
            print_success("Geocoding API is working!")
            print_info(f"  Coordinates: {result['lat']}, {result['lng']}")
            print_info(f"  Address: {result['formatted_address']}")
            return True
        else:
            print_error("Geocoding failed")
            return False

    except Exception as e:
        print_error(f"Geocoding test failed: {e}")
        return False

def test_twilio_config():
    """Test Twilio configuration"""
    print_info("Testing Twilio configuration...")

    try:
        settings = get_settings()

        if settings.twilio_account_sid and settings.twilio_auth_token:
            print_success("Twilio credentials configured!")
            print_info(f"  Phone number: {settings.twilio_phone_number}")
            return True
        else:
            print_error("Twilio credentials missing")
            return False

    except Exception as e:
        print_error(f"Twilio config test failed: {e}")
        return False

async def test_full_flow():
    """Test complete demo flow"""
    print_info("\nTesting complete demo flow...")

    try:
        settings = get_settings()
        llm_service = LLMService(settings.gemini_api_key)
        maps_service = MapsService(settings.google_maps_api_key)

        # Simulate user query
        user_query = "I need Asian food near McGill University"
        print_info(f"\n📱 User says: '{user_query}'")

        # Step 1: LLM processes query
        print_info("  → Gemini AI processing...")
        llm_response = await llm_service.process_message(
            user_message=user_query,
            conversation_history=[],
            session_id="demo_test"
        )

        if llm_response['type'] == 'function_call':
            query = llm_response['function_args']['query']
            location = llm_response['function_args']['location']
            print_success(f"  Gemini understood: '{query}' at '{location}'")

            # Step 2: Search Google Maps
            print_info("  → Searching Google Maps...")
            places = maps_service.search_places(query, location)

            if places:
                print_success(f"  Found {len(places)} places!")

                # Step 3: Format response
                print_info("  → Formatting response...")
                response = await llm_service.format_function_result(
                    function_name="search_places",
                    function_result={"places": places},
                    session_id="demo_test"
                )

                print_success(f"\n🤖 AI Response: {response}")

                # Show top result details
                print_info("\n📍 Top Result Details:")
                top = places[0]
                print(f"     Name: {top['name']}")
                print(f"     Rating: {top.get('rating', 'N/A')} ⭐")
                print(f"     Address: {top['address']}")
                if top.get('open_now') is not None:
                    status = "Open now" if top['open_now'] else "Closed"
                    print(f"     Status: {status}")

                return True

        return False

    except Exception as e:
        print_error(f"Full flow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🎯 CALL2MAP HACKATHON DEMO TEST")
    print("="*60 + "\n")

    results = []

    # Test individual components
    results.append(("Google Gemini API", await test_gemini_api()))
    print()

    results.append(("Google Maps API", test_maps_api()))
    print()

    results.append(("Geocoding API", test_geocoding()))
    print()

    results.append(("Twilio Config", test_twilio_config()))
    print()

    # Test full flow
    results.append(("Full Demo Flow", await test_full_flow()))

    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60 + "\n")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        if result:
            print_success(f"{name:.<40} PASS")
        else:
            print_error(f"{name:.<40} FAIL")

    print("\n" + "-"*60)
    if passed == total:
        print_success(f"All tests passed! ({passed}/{total})")
        print_success("✨ You're ready for the demo! ✨")
        return 0
    else:
        print_warning(f"Some tests failed ({passed}/{total})")
        print_warning("⚠ Fix the issues before demoing")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
