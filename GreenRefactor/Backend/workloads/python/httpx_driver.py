"""Workload driver for httpx
Exercises the Client and Request building internals.
"""
import sys
import os

repo_root = os.path.join(os.path.dirname(__file__), "..", "..", "repos", "python", "httpx")
sys.path.insert(0, repo_root)

import httpx

def run_workload():
    client = httpx.Client(base_url="https://api.example.com", headers={"X-App-Version": "1.0.0"})
    
    for i in range(5000):
        # build_request does not send the request over the network.
        # It exercises URL parsing, header merging, query encoding, and json encoding.
        req = client.build_request(
            method="POST",
            url=f"/v1/users/{i}/profile",
            params={"skip": "0", "limit": str(i % 100), "expand": ["history", "settings"]},
            headers={"Authorization": "Bearer secret-token", "X-Trace-Id": f"trace-{i}"},
            json={
                "id": i,
                "first_name": f"User{i}",
                "last_name": f"Test{i}",
                "settings": {
                    "theme": "dark",
                    "notifications": True,
                    "tags": ["a", "b", "c", "d"]
                }
            }
        )
        
        # Access attributes to force any lazy evaluation
        _ = req.method
        _ = req.url
        _ = req.headers
        _ = req.content

if __name__ == "__main__":
    run_workload()
    print("OK: httpx workload finished")
