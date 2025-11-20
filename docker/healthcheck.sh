#!/usr/bin/env bash
set -euo pipefail

PORT=${APP_PORT:-8501}
URL="http://127.0.0.1:${PORT}/healthz"

if command -v curl >/dev/null 2>&1; then
  if curl -fsS "$URL" >/dev/null 2>&1; then
    exit 0
  fi
  # Streamlit does not expose /healthz, so fall back to root
  curl -fsS "http://127.0.0.1:${PORT}" >/dev/null 2>&1 || exit 1
else
  exit 0
fi
