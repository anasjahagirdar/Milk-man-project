#!/bin/bash

set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/MilkMan/backend"

log() {
  printf '[backend-service] %s\n' "$1"
}

activate_venv() {
  if [ -f "$BACKEND_DIR/venv/bin/activate" ]; then
    source "$BACKEND_DIR/venv/bin/activate"
    return 0
  fi

  if [ -f "$ROOT_DIR/venv/bin/activate" ]; then
    source "$ROOT_DIR/venv/bin/activate"
    return 0
  fi

  return 1
}

find_python() {
  if [ -x "$BACKEND_DIR/venv/bin/python" ]; then
    printf '%s\n' "$BACKEND_DIR/venv/bin/python"
    return 0
  fi

  if [ -x "$ROOT_DIR/venv/bin/python" ]; then
    printf '%s\n' "$ROOT_DIR/venv/bin/python"
    return 0
  fi

  if command -v python3 >/dev/null 2>&1; then
    command -v python3
    return 0
  fi

  if command -v python >/dev/null 2>&1; then
    command -v python
    return 0
  fi

  return 1
}

cd "$BACKEND_DIR"

if [ -f ".env" ]; then
  set -a
  source ".env"
  set +a
fi

activate_venv || true

PYTHON_BIN="$(find_python)"
if [ -z "$PYTHON_BIN" ]; then
  log "Python runtime was not found"
  exit 1
fi

export HOST="${HOST:-0.0.0.0}"
export PORT="${PORT:-5000}"
export FLASK_DEBUG="${FLASK_DEBUG:-false}"
export PYTHONUNBUFFERED=1

if command -v gunicorn >/dev/null 2>&1; then
  log "Starting Gunicorn on ${HOST}:${PORT}"
  exec gunicorn \
    --bind "${HOST}:${PORT}" \
    --workers "${GUNICORN_WORKERS:-2}" \
    --threads "${GUNICORN_THREADS:-4}" \
    --timeout "${GUNICORN_TIMEOUT:-120}" \
    --access-logfile - \
    --error-logfile - \
    app.main:app
fi

if [ -x "$BACKEND_DIR/venv/bin/gunicorn" ]; then
  log "Starting bundled Gunicorn on ${HOST}:${PORT}"
  exec "$BACKEND_DIR/venv/bin/gunicorn" \
    --bind "${HOST}:${PORT}" \
    --workers "${GUNICORN_WORKERS:-2}" \
    --threads "${GUNICORN_THREADS:-4}" \
    --timeout "${GUNICORN_TIMEOUT:-120}" \
    --access-logfile - \
    --error-logfile - \
    app.main:app
fi

log "Gunicorn not found, falling back to python -m app.main"
exec "$PYTHON_BIN" -m app.main