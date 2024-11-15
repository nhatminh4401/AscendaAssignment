from .base import BaseSupplier
from domain.models import Hotel, Location, Images, Amenities, ImageItem
from typing import List, Dict, Any

class PaperfliesSupplier(BaseSupplier):
    # Initialize the supplier with the API URL
    def __init__(self):
        super().__init__("https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/paperflies")

    # Parse the hotel data from the JSON response
    def parse_hotel(self, data: Dict[str, Any]) -> Hotel:
        return Hotel(
            id=str(data.get("hotel_id", "")),
            destination_id=str(data.get("destination_id", "")),
            name=data.get("hotel_name", ""),
            description=data.get("details", ""),
            location=self._parse_location(data.get("location", {})),
            amenities=self._parse_amenities(data.get("amenities", {})),
            images=self._parse_images(data.get("images", {})),
            booking_conditions=data.get("booking_conditions", [])
        )

    # Parse the location data from the JSON response
    def _parse_location(self, location: Dict[str, Any]) -> Location:
        return Location(
            lat=None,  # Not found in JSON from Paperflies supplier
            lng=None,  # Not found in JSON from Paperflies supplier
            address=location.get("address", ""),
            city="",  # Not found in JSON from Paperflies supplier
            country=location.get("country", "")
        )

    # Parse the amenities data from the JSON response
    def _parse_amenities(self, amenities: Dict[str, List[str]]) -> Amenities:
        return Amenities(
            general=amenities.get("general", []),
            room=amenities.get("room", [])
        )

    # Parse the images data from the JSON response
    def _parse_images(self, images: Dict[str, List[Dict[str, str]]]) -> Images:
        return Images(
            rooms=[ImageItem(url=img["link"], description=img.get("caption")) 
                  for img in images.get("rooms", [])],
            site=[ImageItem(url=img["link"], description=img.get("caption"))
                 for img in images.get("site", [])],
            amenities=[]  # Not found in JSON from Paperflies supplier
        )