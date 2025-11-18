#!/usr/bin/env bash
set -euo pipefail

APP_MODE=${APP_MODE:-streamlit}
APP_PORT=${APP_PORT:-8501}
export STREAMLIT_SERVER_PORT=${APP_PORT}

cd /app

if [[ "$APP_MODE" == "api" ]]; then
  exec uvicorn project_forge.src.api.app:app --host 0.0.0.0 --port "${APP_PORT}"
else
  exec streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port "${APP_PORT}" --server.headless true
fi
