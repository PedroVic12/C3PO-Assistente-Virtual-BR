#!/bin/bash
# Wrapper to run the C3PO agent toolbelt commands

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="python3"

# Check if venv is active or exists
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
fi

if [ -f "$SCRIPT_DIR/c3po/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/c3po/venv/bin/activate"
fi

# Run the python agent toolbelt with any arguments passed
python3 "$SCRIPT_DIR/tools/agent_toolbelt.py" "$@"
