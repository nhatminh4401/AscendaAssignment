from abc import ABC, abstractmethod
from typing import List
from .models import Hotel


# Define interfaces for supplier
class ISupplier(ABC):

    @abstractmethod
    # Get hotels from supplier
    def get_hotels(self) -> List[dict]:
        pass


# Define interfaces for repository
class IHotelRepository(ABC):

    @abstractmethod
    # Save hotels to repository
    def save_all(self, hotels: List[Hotel]) -> None:
        pass

    @abstractmethod
    # Find hotels based on criteria
    def find_by_criteria(self, hotel_ids: List[str],
                         destination_ids: List[str]) -> List[Hotel]:
        pass


# Define interfaces for merge strategy
class IMergeStrategy(ABC):

    @abstractmethod
    # Merge existing and new hotels
    def merge(self, existing: Hotel, new: Hotel) -> Hotel:
        pass
