#!/bin/bash

# Fast test runner script for pre-commit
# This script runs tests quickly with progress indicators

echo "🧪 Running Backend Tests (Pre-commit Mode)"
echo "=========================================="

# Set environment variables for testing
export TESTING=true

# Force unbuffered output for pre-commit
export PYTHONUNBUFFERED=1

# Run tests with detailed progress indicators
echo "Running tests with detailed progress indicators..." >&2
poetry run python -u -m pytest tests/ \
    --tb=short \
    --cov=api \
    --cov-report=term-missing \
    --cov-config=.coveragerc \
    --durations=10 \
    --maxfail=3 \
    --color=yes \
    --disable-warnings \
    --capture=no \
    --verbose \
    --no-header \
    --no-summary 2>&1

# Capture the exit code from pytest
TEST_EXIT_CODE=$?

echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Tests failed with exit code $TEST_EXIT_CODE"
    echo "Please fix the failing tests before committing."
fi

# Exit with the same code as pytest
exit $TEST_EXIT_CODE
