"""Workload driver for faker
Exercises proxy and generators to produce massive amounts of synthetic data.
"""
import sys
import os

repo_root = os.path.join(os.path.dirname(__file__), "..", "..", "repos", "python", "faker")
sys.path.insert(0, repo_root)

from faker import Faker

def run_workload():
    fake = Faker()
    Faker.seed(42) # Ensure determinism
    
    for i in range(10000):
        _ = fake.name()
        _ = fake.address()
        _ = fake.email()
        _ = fake.text(max_nb_chars=200)
        _ = fake.date_of_birth(minimum_age=18, maximum_age=90)
        _ = fake.company()
        _ = fake.credit_card_number()
        
        # Profile involves generating a dict of many fake attributes
        _ = fake.profile(fields=['username', 'name', 'mail', 'residence'])

if __name__ == "__main__":
    run_workload()
    print("OK: faker workload finished")
