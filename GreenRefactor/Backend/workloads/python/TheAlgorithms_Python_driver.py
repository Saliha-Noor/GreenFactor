"""Workload driver for TheAlgorithms_Python — sorts/merge_sort.py
Imports the merge_sort function and sorts a large random list.
"""
import random
import sys
import os

# Add repo root to path so we can import from it
repo_root = os.path.join(os.path.dirname(__file__), "..", "..", "repos", "python", "TheAlgorithms_Python")
sys.path.insert(0, repo_root)

try:
    from sorts.merge_sort import merge_sort
except ImportError:
    # Fallback: define a local merge_sort if import fails
    def merge_sort(collection):
        if len(collection) <= 1:
            return collection
        mid = len(collection) // 2
        left = merge_sort(collection[:mid])
        right = merge_sort(collection[mid:])
        return list(_merge(left, right))

    def _merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

if __name__ == "__main__":
    random.seed(42)
    data = [random.randint(0, 100000) for _ in range(5000)]
    for _ in range(3):
        result = merge_sort(list(data))
    assert result == sorted(data), "Sort result mismatch"
    print(f"OK: sorted {len(data)} elements")
