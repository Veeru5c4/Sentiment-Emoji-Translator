#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

echo "Project root: $PROJECT_ROOT"

# Optional: load environment variables from .env if present
if [[ -f ".env" ]]; then
  echo "Loading environment variables from .env"
  # shellcheck disable=SC1091
  set -a
  source ".env"
  set +a
fi

# Ensure virtual environment exists and is activated
if [[ ! -d ".venv" ]]; then
  echo "Creating virtual environment (.venv)..."
  python3 -m venv .venv
fi

echo "Activating virtual environment..."
# shellcheck disable=SC1091
source .venv/bin/activate

echo "Installing dependencies (if needed)..."
pip install --upgrade pip >/dev/null
pip install -r requirements.txt >/dev/null

# Default URLs / ports
BACKEND_HOST="${BACKEND_HOST:-localhost}"
BACKEND_PORT="${BACKEND_PORT:-8000}"
export BACKEND_URL="${BACKEND_URL:-http://$BACKEND_HOST:$BACKEND_PORT}"

echo "Starting FastAPI backend on ${BACKEND_HOST}:${BACKEND_PORT}..."
uvicorn backend.main:app --reload --host "$BACKEND_HOST" --port "$BACKEND_PORT" &
BACKEND_PID=$!

cleanup() {
  echo
  echo "Shutting down backend (PID=$BACKEND_PID)..."
  kill "$BACKEND_PID" 2>/dev/null || true
  wait "$BACKEND_PID" 2>/dev/null || true
  echo "Done."
}

trap cleanup INT TERM

echo "Starting Streamlit frontend (will connect to $BACKEND_URL)..."
streamlit run frontend/app.py

cleanup


