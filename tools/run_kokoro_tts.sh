#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR/voz-TTS-pt-br"

TEXT_FILE="${1:-$PROJECT_DIR/texto_entrada.txt}"

if [[ "$TEXT_FILE" != /* ]]; then
    TEXT_FILE="$PROJECT_DIR/$TEXT_FILE"
fi

if [[ ! -f "$TEXT_FILE" ]]; then
    echo "Arquivo de texto não encontrado: $TEXT_FILE" >&2
    exit 1
fi

cd "$PROJECT_DIR"
echo "Executando TTS com: $TEXT_FILE"
uv run kokoro_tts_voz_local.py "$TEXT_FILE"
echo "Gerando o arquivo de audio..."

