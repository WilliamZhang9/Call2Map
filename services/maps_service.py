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
                fields=['opening_hours', 'formatted_phone_number', 'website']
            )
            
            details = {}
            if 'result' in result:
                place_info = result['result']
                details['phone'] = place_info.get('formatted_phone_number')
                details['website'] = place_info.get('website')
                
                if 'opening_hours' in place_info:
                    details['open_now'] = place_info['opening_hours'].get('open_now')
            
            return details
            
        except Exception as e:
            logger.error(f"Error getting place details: {e}")
            return {}
    
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
