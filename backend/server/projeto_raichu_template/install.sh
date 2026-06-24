#!/bin/bash
set -e
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 -m venv .venv || true
source .venv/bin/activate
pip install --upgrade pip
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
fi
if [ -f frontend/package.json ]; then
  echo "Run 'cd frontend && npm install' to install frontend deps"
fi
echo "Venv pronta. Ative: source .venv/bin/activate"
