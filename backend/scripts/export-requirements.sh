#!/bin/bash

# Export requirements script
# This script exports Poetry dependencies to requirements.txt

echo "📦 Exporting Poetry dependencies to requirements.txt"
echo "=================================================="

# Export Poetry dependencies to requirements.txt
poetry export --without-hashes --format=requirements.txt > requirements.txt

echo "✅ Requirements exported to requirements.txt"