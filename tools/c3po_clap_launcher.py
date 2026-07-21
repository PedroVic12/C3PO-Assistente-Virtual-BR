#!/usr/bin/env python3
"""
C3PO Clap Launcher:
Listens to your default microphone. When a double-clap is detected,
it speaks a greeting and launches the C3PO Voice Menu to ask which program to run.
"""

import os
import sys
import time
import logging
import subprocess
import threading
import numpy as np
import sounddevice as sd

# --- Tuning knobs (Identical to jarvis.py for reliability) ---
SAMPLE_RATE = 44100
BLOCK_MS = 40
CHANNELS = 1

SPIKE_RATIO = 7.0
COOLDOWN_S = 0.45
MIN_DOUBLE_GAP_S = 0.05
MAX_DOUBLE_GAP_S = 0.35
RETRIGGER_RATIO = 0.55
NOISE_FLOOR_ALPHA = 0.992
MIN_RMS = 0.012
QUIET_GATE_MULT = 2.2

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("c3po_clap")

def block_samples() -> int:
    n = int(SAMPLE_RATE * BLOCK_MS / 1000)
    return max(n, 1)

def rms_mono(block: np.ndarray) -> float:
    if block.ndim > 1:
        block = np.mean(block.astype(np.float64), axis=1)
    else:
        block = block.astype(np.float64)
    if block.size == 0:
        return 0.0
    return float(np.sqrt(np.mean(block**2)))

def play_alert_voice(text):
    # Try spd-say (extremely fast and native on Linux)
    try:
        if subprocess.run(["which", "spd-say"], capture_output=True).returncode == 0:
            subprocess.run(["spd-say", "-l", "pt", "-t", "female1", text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return
    except Exception:
        pass
    
    # Try espeak
    try:
        if subprocess.run(["which", "espeak"], capture_output=True).returncode == 0:
            subprocess.run(["espeak", "-v", "pt", text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return
    except Exception:
        pass

def run_c3po_voice_menu():
    log.info("Double clap actions: Launching voice menu!")
    play_alert_voice("Entendido. Iniciando reconhecimento de voz.")
    # Run the voice menu in a separate terminal or process
    script_path = "/home/pedrov12/Documentos/GitHub/C3PO-Assistente-Virtual-BR/tools/agent_toolbelt.py"
    subprocess.Popen(["python3", script_path, "voice_menu"])

def main():
    blocksize = block_samples()
    noise_floor = 1e-4
    last_logged_double = 0.0
    first_clap_time = None
    spike_armed = True

    log.info("C3PO Clap Listener online. Batas palmas duas vezes (👏👏) para me chamar.")

    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="float32",
            blocksize=blocksize,
        ) as stream:
            while True:
                data, overflowed = stream.read(blocksize)
                if overflowed:
                    log.warning("Input overflow; try a larger BLOCK_MS")

                level = rms_mono(data)

                quiet_gate = noise_floor * QUIET_GATE_MULT
                if level < quiet_gate:
                    noise_floor = NOISE_FLOOR_ALPHA * noise_floor + (
                        1.0 - NOISE_FLOOR_ALPHA
                    ) * level
                    noise_floor = max(noise_floor, 1e-7)

                threshold = max(noise_floor * SPIKE_RATIO, MIN_RMS)
                now = time.monotonic()
                retrigger_level = threshold * RETRIGGER_RATIO

                if level < retrigger_level:
                    spike_armed = True

                if (
                    spike_armed
                    and level >= threshold
                    and (now - last_logged_double) >= COOLDOWN_S
                ):
                    spike_armed = False
                    if first_clap_time is None:
                        first_clap_time = now
                    else:
                        gap = now - first_clap_time
                        if gap < MIN_DOUBLE_GAP_S:
                            pass
                        elif gap <= MAX_DOUBLE_GAP_S:
                            first_clap_time = None
                            last_logged_double = now
                            log.info("👏👏 Duas palmas detectadas! Chamando C3PO...")
                            # Run actions in a background thread to prevent blocking
                            threading.Thread(
                                target=run_c3po_voice_menu, daemon=True
                            ).start()
                        else:
                            first_clap_time = now

    except KeyboardInterrupt:
        log.info("Stopped.")
        return 0
    except Exception as e:
        log.error("Error: %s", e)
        return 1

if __name__ == "__main__":
    sys.exit(main())
