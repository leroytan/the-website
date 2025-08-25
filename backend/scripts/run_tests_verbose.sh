#!/bin/bash

# Verbose test runner script for the backend
# This script runs all tests with maximum progress visibility

echo "🧪 Running Backend Tests (Verbose Mode)"
echo "======================================="

# Set environment variables for testing
export TESTING=true

# Run tests with maximum progress visibility
echo "Running all tests with maximum progress indicators..."
poetry run pytest tests/ \
    --tb=short \
    --cov=api \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-config=.coveragerc \
    --durations=10 \
    --maxfail=5 \
    --color=yes \
    --verbose \
    --capture=no \
    --disable-warnings

# Capture the exit code from pytest
TEST_EXIT_CODE=$?

echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed!"
    echo "📊 Coverage report generated in htmlcov/index.html"
else
    echo "❌ Tests failed with exit code $TEST_EXIT_CODE"
    echo "Please fix the failing tests before committing."
fi

# Exit with the same code as pytest
exit $TEST_EXIT_CODE
