#!/bin/bash

# Test runner script for the backend
# This script runs all tests with proper configuration

echo "🧪 Running Backend Tests"
echo "========================="

# Set environment variables for testing
export TESTING=true

# Run tests with coverage (this is the command that works)
echo "Running all tests with coverage..."
poetry run pytest tests/ -v --cov=api --cov-report=term-missing --cov-report=html --cov-config=.coveragerc --tb=short

echo ""
echo "✅ All tests completed!"
echo "📊 Coverage report generated in htmlcov/index.html"
