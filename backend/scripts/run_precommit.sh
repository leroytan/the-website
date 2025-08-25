#!/bin/bash

# Pre-commit runner script
# This script runs pre-commit hooks

echo "🔧 Running Pre-commit Hooks"
echo "============================"

# Run pre-commit (we're already in the backend directory)
pre-commit run --all-files

echo ""
echo "✅ Pre-commit hooks completed!"
echo ""
echo "Note: If the export-requirements hook 'failed', it means requirements.txt was updated."
echo "This is expected behavior - the file was successfully exported."
