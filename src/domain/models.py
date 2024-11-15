from dataclasses import dataclass
from typing import List, Optional


# Define data classes for domain models
@dataclass
class Location:
    lat: Optional[float]
    lng: Optional[float]
    address: str
    city: str
    country: str


@dataclass
class ImageItem:
    url: str
    description: Optional[str]


@dataclass
class Images:
    rooms: List[ImageItem]
    site: List[ImageItem]
    amenities: List[ImageItem]


@dataclass
class Amenities:
    general: List[str]
    room: List[str]


@dataclass
class Hotel:
    id: str
    destination_id: str
    name: str
    location: Location
    description: str
    amenities: Amenities
    images: Images
    booking_conditions: List[str]
