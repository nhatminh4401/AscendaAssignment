from typing import List, Optional
from domain.interfaces import IMergeStrategy
from domain.models import Hotel, ImageItem, Location, Amenities, Images


class DefaultMergeStrategy(IMergeStrategy):
    # Merge two hotel objects into one by combining their fields and removing duplicates
    def merge(self, existing: Hotel, new: Hotel) -> Hotel:
        return Hotel(
            id=existing.id,
            destination_id=self._merge_value(existing.destination_id,
                                             new.destination_id),
            name=self._merge_value(existing.name, new.name),
            location=self._merge_location(existing.location, new.location),
            description=self._merge_value(existing.description,
                                          new.description),
            amenities=self._merge_amenities(existing.amenities, new.amenities),
            images=self._merge_images(existing.images, new.images),
            booking_conditions=list(
                set(existing.booking_conditions + new.booking_conditions)))

    # Merge two values, keeping the new one if it exists
    def _merge_value(self, existing: str, new: str) -> str:
        return new if new else existing

    # Merge two location objects, keeping the new one if it exists
    def _merge_location(self, existing: Location, new: Location) -> Location:
        # If existing location is not provided, return the new one
        if not existing:
            return new
        # If new location is not provided, keep the existing one
        if not new:
            return existing

        return Location(lat=new.lat if new.lat is not None else existing.lat,
                        lng=new.lng if new.lng is not None else existing.lng,
                        address=self._merge_value(existing.address,
                                                  new.address),
                        city=self._merge_value(existing.city, new.city),
                        country=self._merge_value(existing.country,
                                                  new.country))

    # Mapping of normalized terms to preferred display format
    PREFERRED_TERMS = {
        'businesscenter': 'business center',
        'drycleaning': 'dry cleaning',
        'tub': 'bathtub',
    }

    # Terms to exclude if specific versions exist
    EXCLUDE_IF_SPECIFIC = {
        'pool': {'outdoor pool', 'indoor pool'},
    }

    # Amenities that should be moved to room list only
    MOVE_TO_ROOM = {
        'aircon',
        'bathtub',
    }

    # Normalize and filter amenities
    def _normalize_amenity(self, amenity: str) -> str:
        return amenity.lower().strip().replace(' ', '')

    # Get preferred term if it exists, otherwise return original in lowercase
    def _get_preferred_term(self, amenity: str) -> str:
        normalized = self._normalize_amenity(amenity)
        preferred = self.PREFERRED_TERMS.get(normalized, amenity)
        return preferred.lower()

    # Filter out generic terms when specific versions exist
    def _filter_generic_terms(self, amenities: List[str]) -> List[str]:
        result = []
        # Normalize all amenities for comparison
        normalized_amenities = {self._normalize_amenity(a) for a in amenities}

        for amenity in amenities:
            normalized = self._normalize_amenity(amenity)

            # Check if this is a generic term that should be excluded
            should_exclude = False
            for generic, specifics in self.EXCLUDE_IF_SPECIFIC.items():
                # If normalized term is generic and any specific term is present, exclude it from the list
                if normalized == generic and any(
                        self._normalize_amenity(specific) in
                        normalized_amenities for specific in specifics):
                    should_exclude = True
                    break
            # Add to result if not excluded
            if not should_exclude:
                result.append(self._get_preferred_term(amenity))

        return result

    # Merge two amenities objects, combining and filtering out duplicates
    def _merge_amenities(self, existing: Optional[Amenities],
                         new: Optional[Amenities]) -> Amenities:
        # Handle cases where one or both objects are None
        if not existing and not new:
            return Amenities(general=[], room=[])
        if not existing:
            return new
        if not new:
            return existing

        # To remove duplicates and keep track of original terms
        seen_items = {}  # normalized -> original mapping
        room_items = set()  # normalized room items
        general_items = set()  # normalized general items

        # Process room amenities first
        all_room = (existing.room or []) + (new.room or [])
        final_room = []

        # Process room amenities for deduplication
        for item in all_room:
            # Normalize and check if already seen for deduplication
            normalized = self._normalize_amenity(item)
            if normalized not in seen_items:
                seen_items[normalized] = self._get_preferred_term(item)
                room_items.add(normalized)
                final_room.append(seen_items[normalized])

        # Process general amenities
        all_general = (existing.general or []) + (new.general or [])
        final_general = []

        # Process general amenities for deduplication
        for item in all_general:
            # Normalize and check if already seen for deduplication
            normalized = self._normalize_amenity(item)
            # Skip if should be in room only
            if normalized in self.MOVE_TO_ROOM:
                if normalized not in room_items:
                    room_items.add(normalized)
                    final_room.append(self._get_preferred_term(item))
                continue

            # Skip if already in room
            if normalized in room_items:
                continue

            # Add to general if not seen for deduplication
            if normalized not in general_items:
                seen_items[normalized] = self._get_preferred_term(item)
                general_items.add(normalized)
                final_general.append(seen_items[normalized])

        # Filter out generic terms
        final_general = self._filter_generic_terms(final_general)

        return Amenities(general=final_general, room=final_room)

    # Merge two images objects, combining and removing duplicates
    def _merge_images(self, existing: Images, new: Images) -> Images:
        return Images(rooms=self._merge_image_list(existing.rooms, new.rooms),
                      site=self._merge_image_list(existing.site, new.site),
                      amenities=self._merge_image_list(existing.amenities,
                                                       new.amenities))

    # Merge two lists of ImageItem objects, combining and removing duplicates
    def _merge_image_list(self, existing: List[ImageItem],
                          new: List[ImageItem]) -> List[ImageItem]:
        merged = {img.url: img for img in existing + new}
        return list(merged.values())
