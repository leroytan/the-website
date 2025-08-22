#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# Initialize database (seeding and populating) after migrations
echo "Initializing database..."
python -c "
from api.storage.models import Base
from api.storage.connection import engine
from sqlalchemy.orm import Session
from api.storage.seed import seed_database
from api.storage.populate import insert_test_data
from api.config import settings

# Create tables if they don't exist
Base.metadata.create_all(engine)
print('Tables created')

# Seed database
with Session(engine) as session:
    print('Seeding database')
    seed_database(session)
    print('Database seeded')

# Populate with test data if enabled
if settings.db_populate_check:
    print('Inserting test data')
    success = insert_test_data(engine)
    print('Test data inserted')

print('Database initialization complete')
"
