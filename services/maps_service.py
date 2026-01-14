# services/maps_service.py
import googlemaps
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class MapsService:
    def __init__(self, api_key: str):
        self.client = googlemaps.Client(key=api_key)

    def search_places(self, query: str, location: str) -> List[Dict]:
        """Search for places near a location"""
        try:
            # First, geocode the location
            geocode_result = self.client.geocode(location)
            if not geocode_result:
                logger.error(f"Could not geocode location: {location}")
                return []

            lat_lng = geocode_result[0]['geometry']['location']

            # Search for places
            results = self.client.places_nearby(
                location=(lat_lng['lat'], lat_lng['lng']),
                radius=5000,  # 5km radius
                keyword=query,
                rank_by='prominence'
            )

            places = []
            for place in results.get('results', [])[:5]:  # Top 5
                place_info = {
                    'name': place.get('name'),
                    'address': place.get('vicinity'),
                    'rating': place.get('rating'),
                    'user_ratings_total': place.get('user_ratings_total', 0),
                    'place_id': place.get('place_id'),
                    'types': place.get('types', [])
                }

                # Get additional details
                if place.get('place_id'):
                    details = self._get_place_details(place['place_id'])
                    place_info.update(details)

                places.append(place_info)

            logger.info(f"Found {len(places)} places for query: {query}")
            return places

        except Exception as e:
            logger.error(f"Maps API error: {e}")
            return []

    def _get_place_details(self, place_id: str) -> Dict:
        """Get detailed information about a place"""
        try:
            result = self.client.place(
                place_id=place_id,
                fields=[
                    'opening_hours',
                    'formatted_phone_number',
                    'website',
                    'url',  # Google Maps URL
                    'price_level',
                    'serves_dinner',
                    'serves_lunch',
                    'reservable'
                ]
            )

            details = {}
            if 'result' in result:
                place_info = result['result']
                details['phone'] = place_info.get('formatted_phone_number')
                details['website'] = place_info.get('website')
                details['maps_url'] = place_info.get('url')  # Direct Google Maps link
                details['price_level'] = place_info.get('price_level')  # 0-4 scale
                details['reservable'] = place_info.get('reservable', False)

                if 'opening_hours' in place_info:
                    details['open_now'] = place_info['opening_hours'].get('open_now')

                # Extract booking URL if it's a known platform
                if details.get('website'):
                    details['booking_url'] = self._extract_booking_url(details['website'])

            return details

        except Exception as e:
            logger.error(f"Error getting place details: {e}")
            return {}

    def _extract_booking_url(self, website: str) -> Optional[str]:
        """Extract booking URL if from known reservation platforms"""
        booking_platforms = [
            'opentable.com',
            'resy.com',
            'yelp.com/reservations',
            'sevenrooms.com',
            'tock.com',
            'bookatable.com',
            'thefork.com',
            'reserve.google.com'
        ]

        website_lower = website.lower()
        for platform in booking_platforms:
            if platform in website_lower:
                return website

        return None

    def get_reservation_info(self, place_id: str) -> Dict:
        """Get reservation-specific information for a place"""
        try:
            details = self._get_place_details(place_id)

            reservation_info = {
                'place_id': place_id,
                'can_reserve': details.get('reservable', False),
                'phone': details.get('phone'),
                'website': details.get('website'),
                'booking_url': details.get('booking_url'),
                'maps_url': details.get('maps_url')
            }

            # Determine reservation method
            if reservation_info['booking_url']:
                reservation_info['method'] = 'online'
                reservation_info['platform'] = self._identify_platform(reservation_info['booking_url'])
            elif reservation_info['phone']:
                reservation_info['method'] = 'phone'
            else:
                reservation_info['method'] = 'unknown'

            return reservation_info

        except Exception as e:
            logger.error(f"Error getting reservation info: {e}")
            return {}

    def _identify_platform(self, url: str) -> str:
        """Identify the booking platform from URL"""
        url_lower = url.lower()
        if 'opentable' in url_lower:
            return 'OpenTable'
        elif 'resy' in url_lower:
            return 'Resy'
        elif 'tock' in url_lower:
            return 'Tock'
        elif 'sevenrooms' in url_lower:
            return 'SevenRooms'
        elif 'yelp' in url_lower:
            return 'Yelp'
        elif 'reserve.google' in url_lower:
            return 'Google Reserve'
        return 'Website'

    def geocode_address(self, address: str) -> Optional[Dict]:
        """Convert address to coordinates"""
        try:
            result = self.client.geocode(address)
            if result:
                location = result[0]['geometry']['location']
                return {
                    'lat': location['lat'],
                    'lng': location['lng'],
                    'formatted_address': result[0]['formatted_address']
                }
        except Exception as e:
            logger.error(f"Geocoding error: {e}")
        return None
