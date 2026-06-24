#!/bin/bash
# Wrapper to run C3PO native voice alerts

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="python3"

# Activate venv if exists
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
fi

python3 "$SCRIPT_DIR/tools/c3po_voice_alerts.py" "$@"
