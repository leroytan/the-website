#!/bin/bash

# Python formatting script
# This script formats all Python files using Ruff

echo "🎨 Formatting Python Files"
echo "=========================="

# Set environment variables
export TESTING=true

# Format all Python files in the backend directory
echo "Formatting Python files with Ruff..."
poetry run ruff format api/ tests/ --check

# Capture the exit code from ruff format
FORMAT_EXIT_CODE=$?

if [ $FORMAT_EXIT_CODE -eq 0 ]; then
    echo "✅ All Python files are properly formatted!"
else
    echo "❌ Some Python files need formatting. Running format..."
    poetry run ruff format api/ tests/
    echo "✅ Python files have been formatted!"
fi

# Also run Ruff linting to fix any auto-fixable issues
echo "🔧 Running Ruff linting with auto-fix..."
poetry run ruff check api/ tests/ --fix

# Capture the exit code from ruff check
LINT_EXIT_CODE=$?

if [ $LINT_EXIT_CODE -eq 0 ]; then
    echo "✅ All Python files pass linting!"
else
    echo "⚠️  Some linting issues remain (non-auto-fixable)"
fi

# Exit with success if formatting was successful
exit 0
