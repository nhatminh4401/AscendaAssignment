from .base import BaseSupplier
from domain.models import Hotel, Location, Images, Amenities
from typing import Dict, Any


class AcmeSupplier(BaseSupplier):
    # Initialize the supplier with the API URL
    def __init__(self):
        super().__init__(
            "https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/acme")

    # Parse the hotel data from the JSON response
    def parse_hotel(self, data: Dict[str, Any]) -> Hotel:
        return Hotel(
            id=str(data.get("Id", "")),
            destination_id=str(data.get("DestinationId", "")),
            name=data.get("Name", ""),
            description=data.get("Description", ""),
            location=self._parse_location(data),
            amenities=self._parse_amenities(data),
            images=Images(
                rooms=[], site=[],
                amenities=[]),  # Not found in JSON from ACME supplier
            booking_conditions=[]  # Not found in JSON from ACME supplier
        )

    # Parse the location data from the JSON response
    def _parse_location(self, data: Dict[str, Any]) -> Location:
        lat = data.get("Latitude")
        lng = data.get("Longitude")
        return Location(lat=float(lat) if lat else None,
                        lng=float(lng) if lng else None,
                        address=data.get("Address", ""),
                        city=data.get("City", ""),
                        country=data.get("Country", ""))

    # Parse the amenities data from the JSON response
    def _parse_amenities(self, data: Dict[str, Any]) -> Amenities:
        facilities = [f.strip() for f in data.get("Facilities", [])]
        return Amenities(
            general=facilities,
            room=[]  # Not found in JSON from ACME supplier
        )
