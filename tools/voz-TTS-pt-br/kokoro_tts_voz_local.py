import sys
from pathlib import Path
from kokoro import KPipeline

#from IPython.display import display, Audio

import soundfile as sf
import numpy as np
import sounddevice as sd
import subprocess
import os

# uv init

# 1️⃣ Install kokoro
#!pip install -q kokoro>=0.9.4 soundfile
# 2️⃣ Install espeak, used for English OOD fallback and some non-English languages
# yay -S speak-ng

# uv pip install kokoro>=0.9.4 soundfile sounddevice numpy  

#! rode no terminal

# uv run kokoro_tts_voz_local.py texto_entrada.txt

VOICES = [
    "af_heart", # default
    "pf_dora", # voz em pt br feminina
    "pm_alex", # voz em pt br masculina
    "pm_santa" # voz em pt br Papai noel
]

VOICE = VOICES[1]

LANGUAGE = "p"
sample_rate = 24 * 1000  # 24kHz

ROOT_DIR = Path(__file__).resolve().parent
SOUNDS_DIR = ROOT_DIR / "sounds"
SOUNDS_DIR.mkdir(parents=True, exist_ok=True)

pipeline = KPipeline(
    lang_code=LANGUAGE,
)


def carregar_texto(texto_entrada):
    if isinstance(texto_entrada, (str, os.PathLike)):
        caminho = Path(texto_entrada)
        if caminho.exists() and caminho.is_file():
            return caminho.read_text(encoding="utf-8")
    return str(texto_entrada)


def resolver_caminho_saida(output_path):
    caminho = Path(output_path)
    if caminho.is_absolute():
        return caminho
    return SOUNDS_DIR / caminho


def falar_tts_local(texto, voice, playback=False, output_path="fala_completa.wav"):
    texto_final = carregar_texto(texto)
    print(f"Texto de entrada carregado: {texto_final[:120]}...")
    generator = pipeline(texto_final, voice=voice)
    results = list(generator)

    # gerando audios
    for i, (gs, ps, audio) in enumerate(results):
        os.system("clear")
        print(f"Gerando audio {i + 1} de {len(results)}")
        print(f"[{i}] graphemes: {gs}")
        print(f"\n[{i}] phonemes: {ps}")

    if results:
        stream = np.concatenate([audio for _, _, audio in results])

        if playback:
            sd.play(stream, samplerate=sample_rate)
            sd.wait()

        output_file = resolver_caminho_saida(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        sf.write(str(output_file), stream, sample_rate)
        print(f"Áudio completo salvo como {output_file}")

        for i, (_, _, audio) in enumerate(results):
            chunk_path = SOUNDS_DIR / f"segmento_{i + 1:02d}_{output_file.stem}.wav"
            sf.write(str(chunk_path), audio, sample_rate)
            print(f"Segmento {i + 1} salvo como {chunk_path}")
    else:
        print("Nenhum áudio foi gerado.")

    return [audio for _, _, audio in results]


def main():
    subprocess.run("clear", shell=True)

    
    print("\n\nIniciando o Kokoro TTS local...\n\n")


    text_viviane = "Olá, Viviane Gomes, tudo bem? Aqui é a nova voz do Kokoro TTS, e estou muito feliz em poder falar com você! O mestre Pedro Victor sempre fala muito bem de você. Enfim, estou aqui para te atualizar sobre o progresso dos serviços de programação e automação que ele vem desenvolvendo. Agora, eu tenho acesso local ao computador dele em Campo Grande, onde posso ativar serviços e disparar diferentes comandos na hora que eu quiser! Haha. Ele me pediu para te dar um recado: ele está com um save no jogo do Jurassic Park para iniciar um novo jogo do parque com uma nova família de dinossauros junto com você. Além disso, ele está no seu aguardo para jogar a missão 'Vinho do Divino' no jogo The Witcher 3, junto com você no Discord. Eu sei que vocês se gostam muito e espero falar com você novamente em breve. Até logo!"

    if len(sys.argv) < 2:
        print("Informe o caminho do arquivo .txt para gerar a fala.")
        return

    caminho = Path(sys.argv[1])
    if not caminho.exists() or not caminho.is_file():
        print(f"Arquivo não encontrado: {caminho}")
        return

    print(f"Lendo texto do arquivo: {caminho}\n\n")
    falar_tts_local(caminho, VOICE, playback=True, output_path="fala_completa.wav")


if __name__ == "__main__":
    main()