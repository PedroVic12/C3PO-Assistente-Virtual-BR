#!/bin/bash
set -e
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"
# ativa venv se existir
if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
fi
# frontend dev em background (se existir)
if [ -f frontend/package.json ]; then
  (cd frontend && nohup npm run dev > ../frontend_dev.log 2>&1 &)
  FRONTEND_PID=$!
  echo "Frontend PID: $FRONTEND_PID"
fi
# roda Flask em foreground para logs
python3 main.py
