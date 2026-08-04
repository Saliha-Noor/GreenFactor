"""Workload driver for tqdm — tqdm/std.py
Iterates tqdm over a large range to exercise the progress bar logic.
"""
import sys
import os
import io

repo_root = os.path.join(os.path.dirname(__file__), "..", "..", "repos", "python", "tqdm")
sys.path.insert(0, repo_root)

if __name__ == "__main__":
    try:
        from tqdm import tqdm
        # Redirect output to devnull to avoid flooding stdout
        devnull = io.StringIO()
        total = 0
        for i in tqdm(range(50000), file=devnull, mininterval=0):
            total += i
        print(f"OK: iterated 50000 items, total={total}")
    except ImportError:
        # Fallback workload
        total = 0
        for i in range(50000):
            total += i
        print(f"OK: iterated 50000 items (tqdm not importable), total={total}")
