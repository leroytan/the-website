#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# Start the application
uvicorn api.index:app --host 0.0.0.0 --port $PORT