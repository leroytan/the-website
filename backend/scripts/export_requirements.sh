#!/bin/bash

# Export requirements script
# This script exports Poetry dependencies to requirements.txt

echo "📦 Exporting Poetry dependencies to requirements.txt"
echo "=================================================="

# Export Poetry dependencies to requirements.txt
poetry export --without-hashes --format=requirements.txt > requirements.txt

# Capture the exit code from poetry export
EXPORT_EXIT_CODE=$?

if [ $EXPORT_EXIT_CODE -eq 0 ]; then
    echo "✅ Requirements exported to requirements.txt"
else
    echo "❌ Failed to export requirements with exit code $EXPORT_EXIT_CODE"
fi

# Exit with the same code as poetry export
exit $EXPORT_EXIT_CODE