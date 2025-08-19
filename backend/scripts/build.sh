#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# Install dependencies and run database migrations
pip install -r requirements.txt && alembic upgrade head