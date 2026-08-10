"""Workload driver for sqlalchemy
Exercises Engine, Session, and declarative models using an in-memory SQLite DB.
"""
import sys
import os

repo_root = os.path.join(os.path.dirname(__file__), "..", "..", "repos", "python", "sqlalchemy", "lib")
sys.path.insert(0, repo_root)

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100))
    orders = relationship("Order", back_populates="user")

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float)
    description = Column(String(200))
    user = relationship("User", back_populates="orders")

def run_workload():
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Insert loop
    for i in range(1000):
        u = User(name=f"User_{i}", email=f"user_{i}@example.com")
        for j in range(3):
            o = Order(amount=(i+1)*j*10.5, description=f"Order {j} for user {i}")
            u.orders.append(o)
        session.add(u)
    
    session.commit()

    # Query loop
    for i in range(100):
        users = session.query(User).filter(User.name.like("User_%")).limit(50).all()
        for u in users:
            _ = u.name
            _ = [o.amount for o in u.orders]
            
    session.close()

if __name__ == "__main__":
    run_workload()
    print("OK: sqlalchemy workload finished")
