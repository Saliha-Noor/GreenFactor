"""Workload driver for pydantic
Exercises BaseModel validation and serialization with complex nested models.
"""
import sys
import os

repo_root = os.path.join(os.path.dirname(__file__), "..", "..", "repos", "python", "pydantic")
sys.path.insert(0, repo_root)

from pydantic import BaseModel, Field
from typing import List, Optional

class Address(BaseModel):
    street: str
    city: str
    zipcode: str
    country: str = "US"

class Item(BaseModel):
    id: int
    name: str
    price: float
    tags: List[str] = Field(default_factory=list)

class User(BaseModel):
    id: int
    username: str
    email: str
    address: Optional[Address] = None
    orders: List[Item] = Field(default_factory=list)

def run_workload():
    # Build a large complex payload
    payload = {
        "id": 12345,
        "username": "benchmark_user",
        "email": "user@example.com",
        "address": {
            "street": "123 Main St",
            "city": "San Francisco",
            "zipcode": "94105",
            "country": "US"
        },
        "orders": [
            {"id": j, "name": f"Item_{j}", "price": j * 9.99, "tags": ["tagA", "tagB", "tagC"]} 
            for j in range(20)
        ]
    }
    
    for _ in range(5000):
        # 1. Parse from dictionary (Validation)
        user = User(**payload)
        
        # 2. Serialize to dictionary
        _ = user.model_dump()
        
        # 3. Serialize to JSON
        _ = user.model_dump_json()

if __name__ == "__main__":
    run_workload()
    print("OK: pydantic workload finished")
