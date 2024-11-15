import requests
from domain.interfaces import ISupplier
from typing import List


# Define base supplier class
class BaseSupplier(ISupplier):
    # Initialize base supplier with API URL
    def __init__(self, api_url: str):
        self.api_url = api_url

    # Get hotels from supplier
    def get_hotels(self) -> List[dict]:
        response = requests.get(self.api_url)
        response.raise_for_status()
        return response.json()
