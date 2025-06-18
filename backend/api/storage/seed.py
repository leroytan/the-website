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


def seed_locations(db: Session):
    locations = [
        "Ang Mo Kio",
        "Bedok North",
        "Bedok South",
        "Bishan",
        "Bukit Batok",
        "Bukit Merah",
        "Bukit Panjang",
        "Bukit Timah",
        "Central Area",
        "Changi",
        "Changi Bay",
        "Choa Chu Kang",
        "Clementi",
        "Geylang",
        "Hougang",
        "Jurong East",
        "Jurong West",
        "Kallang",
        "Lim Chu Kang",
        "Mandai",
        "Marine Parade",
        "Newton",
        "Novena",
        "Orchard",
        "Outram",
        "Pasir Ris",
        "Paya Lebar",
        "Pioneer",
        "Punggol",
        "Queenstown",
        "River Valley",
        "Rochor",
        "Seletar",
        "Sembawang",
        "Sengkang",
        "Serangoon",
        "Simpang",
        "Southern Islands",
        "Straits View",
        "Sungei Kadut",
        "Tampines",
        "Tanglin",
        "Tengah",
        "Thomson",
        "Toa Payoh",
        "Tuas",
        "Western Islands",
        "Western Water Catchment",
        "Woodlands",
        "Yishun",
        "Boon Lay",
        "Ghim Moh",
        "Gul",
        "Kent Ridge",
        "Nanyang",
        "Pasir Laba",
        "Teban Gardens",
        "Toh Tuck",
        "Tuas South",
        "West Coast",
    ]

    from api.storage.models import Location
    db.add_all([Location(name=location) for location in locations])
    db.commit()

def seed_database(db: Session):
    seed_subjects(db)
    seed_levels(db)
    seed_locations(db)
    
    # Optionally, you can log the seeding process
    print(f"Database seeded with subjects, levels and locations at {datetime.datetime.now()}.")