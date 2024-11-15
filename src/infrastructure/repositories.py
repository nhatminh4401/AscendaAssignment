from typing import List, Dict
from domain.interfaces import IHotelRepository
from domain.models import Hotel
from application.merge_strategy import DefaultMergeStrategy


class InMemoryHotelRepository(IHotelRepository):
    # Initialize in-memory repository
    def __init__(self):
        self._hotels: Dict[str, Hotel] = {}
        self._merge_strategy = DefaultMergeStrategy()

    # Save hotels to repository
    def save_all(self, hotels: List[Hotel]) -> None:
        for hotel in hotels:
            # Check if hotel already exists
            if hotel.id in self._hotels:
                # Merge with existing hotel data
                merged = self._merge_strategy.merge(self._hotels[hotel.id],
                                                    hotel)
                self._hotels[hotel.id] = merged
            else:
                # New hotel
                self._hotels[hotel.id] = hotel

    # Find hotels based on criteria
    def find_by_criteria(self, hotel_ids: List[str],
                         destination_ids: List[str]) -> List[Hotel]:
        results = []
        # Filter hotels based on criteria
        for hotel in self._hotels.values():
            if (not hotel_ids or hotel.id in hotel_ids) and \
               (not destination_ids or hotel.destination_id in destination_ids):
                results.append(hotel)
        return results
