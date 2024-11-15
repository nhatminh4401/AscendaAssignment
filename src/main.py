import argparse
import json
import sys
from application.hotel_service import HotelService
from infrastructure.suppliers.acme import AcmeSupplier
from application.merge_strategy import DefaultMergeStrategy
from infrastructure.repositories import InMemoryHotelRepository
from infrastructure.suppliers.patagonia import PatagoniaSupplier
from infrastructure.suppliers.paperflies import PaperfliesSupplier

def main():
    parser = argparse.ArgumentParser(description='Hotel Data Merger')
    # If there are arguments to be passed
    if len(sys.argv) > 1:
        parser.add_argument('hotel_ids', type=str, help='Hotel IDs')
        parser.add_argument('destination_ids', type=str, help='Destination IDs')
        args = parser.parse_args()
    # If there are no arguments to be passed then hotel_ids and destination_ids are set to none
    else:
        args = argparse.Namespace(hotel_ids='none', destination_ids='none')

    # Initialize suppliers to get data from suppliers
    suppliers = [
        AcmeSupplier(), 
        PatagoniaSupplier(),
        PaperfliesSupplier()
    ]

    # Initialize repository to save data in memory
    repository = InMemoryHotelRepository()
    # Initialize merge strategy to merge data
    merge_strategy = DefaultMergeStrategy()

    # Initialize service
    service = HotelService(repository, suppliers, merge_strategy)

    # Process hotels
    service.process_hotels()

    hotel_ids = []
    destination_ids = []

    if args.hotel_ids.lower() != 'none':
        hotel_ids = [id.strip() for id in args.hotel_ids.split(',') if id.strip()]

    if args.destination_ids.lower() != 'none':
        destination_ids = [id.strip() for id in args.destination_ids.split(',') if id.strip()]

    # Find and output results
    results = service.find_hotels(hotel_ids, destination_ids)

    # Convert to JSON with proper handling of nested objects
    json_results = json.dumps(
        [hotel.__dict__ for hotel in results],
        default=lambda o: o.__dict__,
        indent=2,
        ensure_ascii=False
    )
    print(json_results)

if __name__ == "__main__":
    main()