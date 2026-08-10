"""Workload driver for requests
Exercises the Request and PreparedRequest objects within a session.
"""
import sys
import os

repo_root = os.path.join(os.path.dirname(__file__), "..", "..", "repos", "python", "requests", "src")
sys.path.insert(0, repo_root)

import requests
from requests.models import Request

def run_workload():
    session = requests.Session()
    
    headers = {
        "User-Agent": "GreenRefactor Benchmark/1.0",
        "Accept": "application/json",
        "X-Custom-Header": "BenchmarkValue",
        "Authorization": "Bearer some-token"
    }
    
    # Generate CPU load by repeatedly building, preparing, and validating large requests
    for i in range(5000):
        req = Request(
            method="POST",
            url=f"https://api.example.com/v1/resource/{i}",
            headers=headers,
            params={"sort": "desc", "page": str(i), "filter": "active,verified"},
            json={"id": i, "name": f"Item_{i}", "active": True, "tags": ["a", "b", "c"]}
        )
        prep = session.prepare_request(req)
        
        # Access properties to ensure parsing completed
        _ = prep.path_url
        _ = prep.headers
        _ = prep.body

if __name__ == "__main__":
    run_workload()
    print("OK: requests workload finished")
