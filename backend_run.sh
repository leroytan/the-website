#!/bin/bash

# Get Windows-style APPDATA path in Git Bash
APPDATA_LOCAL="/c/Users/$USERNAME/AppData/Local"
POETRY_HOME="$APPDATA_LOCAL/pypoetry"
export PATH="$POETRY_HOME/bin:$PATH"

# Install Poetry if missing
if ! command -v poetry &> /dev/null; then
  echo "⚙️ Poetry not found. Installing into $POETRY_HOME ..."
  curl -sSL https://install.python-poetry.org | POETRY_HOME="$POETRY_HOME" python3 -
  if [ $? -ne 0 ]; then
    echo "❌ Failed to install Poetry."
    exit 1
  fi
  echo "✅ Poetry installed successfully."
fi

# Move to backend directory (relative to script)
cd "$(dirname "$0")/backend" || {
  echo "❌ Failed to cd into backend folder."
  exit 1
}

# Install project dependencies
poetry install

# Set app environment and run the server
export APP_ENV=${APP_ENV:-development}
poetry run python -m uvicorn api.index:app --reload
