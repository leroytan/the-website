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

# Set app environment
export APP_ENV=${APP_ENV:-development}
export PORT=${PORT:-8000}

# Install project dependencies with Poetry
echo "📦 Installing project dependencies..."
poetry install

# Activate Poetry virtual environment
echo "🔧 Activating Poetry virtual environment..."
source $(poetry env info --path)/bin/activate

# Run build script (installs dependencies, runs migrations, initializes database)
echo "🔨 Running build script..."
./scripts/build.sh

# Run start script (starts the server)
echo "🚀 Running start script..."
./scripts/start.sh
