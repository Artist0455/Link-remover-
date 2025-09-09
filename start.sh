#!/usr/bin/env bash
set -euo pipefail

# Activate virtual environment if exists
if [ -f "venv/bin/activate" ]; then
  source venv/bin/activate
fi

# Export BOT_TOKEN if defined in .env
if [ -f ".env" ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "Starting Link Remover Bot in polling mode..."

# Run the polling bot
python3 main.py
