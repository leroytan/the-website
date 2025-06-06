import datetime

from api.storage.models import Level, Subject
from sqlalchemy.orm import Session

def seed_subjects(db: Session):
    subjects = [
        Subject(name="Mathematics"),
        Subject(name="Physics"),
        Subject(name="Chemistry"),
        Subject(name="Biology"),
        Subject(name="English Literature"),
        Subject(name="Computer Science"),
        Subject(name="History"),
        Subject(name="Spanish"),
        Subject(name="Economics"),
        Subject(name="Music")
    ]
    db.add_all(subjects)
    db.commit()

def seed_levels(db: Session):
    # Create test levels
    levels = [
        Level(name="Primary 1", sort_order=1),
        Level(name="Primary 2", sort_order=2),
        Level(name="Primary 3", sort_order=3),
        Level(name="Primary 4", sort_order=4),
        Level(name="Primary 5", sort_order=5),
        Level(name="Primary 6", sort_order=6),
        Level(name="Secondary 1", sort_order=7),
        Level(name="Secondary 2", sort_order=8),
        Level(name="Secondary 3", sort_order=9),
        Level(name="Secondary 4", sort_order=10),
        Level(name="Secondary 5", sort_order=11),
        Level(name="Junior College 1", sort_order=12),
        Level(name="Junior College 2", sort_order=13),
    ]
    db.add_all(levels)
    db.commit()

def seed_database(db: Session):
    seed_subjects(db)
    seed_levels(db)
    
    # Optionally, you can log the seeding process
    print(f"Database seeded with subjects and levels at {datetime.datetime.now()}.")