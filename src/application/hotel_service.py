from domain.interfaces import IHotelRepository, ISupplier, IMergeStrategy
from domain.models import Hotel
from typing import List


class HotelService:
    # Initialize hotel service with repository, suppliers, and merge strategy
    def __init__(self, repository: IHotelRepository,
                 suppliers: List[ISupplier], merge_strategy: IMergeStrategy):
        self._repository = repository
        self._suppliers = suppliers
        self._merge_strategy = merge_strategy

    # Process hotels from all suppliers
    def process_hotels(self):
        for supplier in self._suppliers:
            raw_data = supplier.get_hotels()
            hotels = [supplier.parse_hotel(item) for item in raw_data]
            self._repository.save_all(hotels)

    # Find hotels based on criteria
    def find_hotels(self, hotel_ids: List[str],
                    destination_ids: List[str]) -> List[Hotel]:
        hotels = self._repository.find_by_criteria(hotel_ids, destination_ids)

        # If both hotel_ids and destination_ids are empty, return all hotels
        if not hotel_ids and not destination_ids:
            return hotels

        # Filter hotels based on criteria
        filtered_hotels = []
        for hotel in hotels:
            # If hotel_ids is provided, hotel must match one of them
            if hotel_ids and hotel.id not in hotel_ids:
                continue

            # If destination_ids is provided, hotel must match one of them
            if destination_ids and hotel.destination_id not in destination_ids:
                continue

            filtered_hotels.append(hotel)

        return filtered_hotels
