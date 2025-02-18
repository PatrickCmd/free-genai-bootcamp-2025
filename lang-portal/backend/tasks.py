from invoke import task
import os
from init_db import init_db, seed_data

@task
def initialize_db(c):
    """Initialize the database and create tables."""
    if os.path.exists("words.db"):
        os.remove("words.db")
    init_db()
    print("Database initialized successfully.")

@task
def seed_db(c):
    """Seed the database with initial data."""
    seed_data()
    print("Database seeded successfully.")

@task
def setup(c):
    """Initialize and seed the database."""
    initialize_db(c)
    seed_db(c)
    print("Database setup complete.") 