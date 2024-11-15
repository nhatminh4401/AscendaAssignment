from .base import BaseSupplier
from domain.models import Hotel, Location, Images, Amenities, ImageItem
from typing import Dict, Any, List


class PatagoniaSupplier(BaseSupplier):
    # Initialize the supplier with the API URL
    def __init__(self):
        super().__init__(
            "https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/patagonia")

    # Parse the hotel data from the JSON response
    def parse_hotel(self, data: Dict[str, Any]) -> Hotel:
        return Hotel(
            id=str(data.get("id", "")),
            destination_id=str(data.get("destination", "")),
            name=data.get("name", ""),
            description=data.get("info", ""),
            location=self._parse_location(data),
            amenities=self._parse_amenities(data.get("amenities", [])),
            images=self._parse_images(data.get("images", {})),
            booking_conditions=[]  # Not found in JSON from Patagonia supplier
        )

    # Parse the location data from the JSON response
    def _parse_location(self, data: Dict[str, Any]) -> Location:
        return Location(
            lat=float(data.get("lat", None)),
            lng=float(data.get("lng", None)),
            address=data.get("address", ""),
            city="",  # Not found in JSON from Patagonia supplier
            country=""  # Not found in JSON from Patagonia supplier
        )

    # Parse the amenities data from the JSON response
    def _parse_amenities(self, amenities: List[str]) -> Amenities:
        return Amenities(
            general=amenities,  # All amenities go to general list
            room=[]  # Empty room amenities as they're not provided
        )

    # Parse the images data from the JSON response
    def _parse_images(self, images: Dict[str, List[Dict[str, str]]]) -> Images:
        return Images(
            rooms=[
                ImageItem(url=img["url"], description=img.get("description"))
                for img in images.get("rooms", [])
            ],
            site=[],  # Not found in JSON from Patagonia supplier
            amenities=[
                ImageItem(url=img["url"], description=img.get("description"))
                for img in images.get("amenities", [])
            ])
