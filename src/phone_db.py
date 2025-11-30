import json
import os
from typing import List, Dict, Any, Optional

class PhoneDB:
    def __init__(self, db_path: str = "data/phones.json"):
        self.db_path = db_path
        self.phones = self._load_data()

    def _load_data(self) -> List[Dict[str, Any]]:
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Database file not found at {self.db_path}")
            return []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {self.db_path}")
            return []

    def search_phones(self, query: str = "", min_price: Optional[int] = None, max_price: Optional[int] = None, brand: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search phones by name/description and filter by price/brand.
        """
        results = []
        query = query.lower()
        
        for phone in self.phones:
            # Text match
            match = (query in phone['name'].lower() or 
                     query in phone['description'].lower() or
                     query in phone['brand'].lower())
            
            # Filters
            if min_price is not None and phone['price'] < min_price:
                continue
            if max_price is not None and phone['price'] > max_price:
                continue
            if brand is not None and brand.lower() not in phone['brand'].lower():
                continue
                
            if match or not query: # If query is empty, return all matching filters
                results.append(phone)
                
        return results

    def get_phone_by_id(self, phone_id: str) -> Optional[Dict[str, Any]]:
        for phone in self.phones:
            if phone['id'] == phone_id:
                return phone
        return None

    def get_all_brands(self) -> List[str]:
        return sorted(list(set(phone['brand'] for phone in self.phones)))

if __name__ == "__main__":
    # Test
    db = PhoneDB()
    print(f"Loaded {len(db.phones)} phones.")
    results = db.search_phones("pixel")
    print(f"Found {len(results)} phones matching 'pixel'")
