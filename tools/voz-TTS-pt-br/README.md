# Kokoro TTS Local em Português

Este projeto usa o pacote Kokoro para gerar fala localmente em português brasileiro a partir de um arquivo de texto.

## O que faz

- Lê um arquivo `.txt` com o texto a ser falado
- Gera áudio localmente com o modelo Kokoro
- Reproduz o áudio no alto-falante, se habilitado
- Salva o áudio completo e os segmentos gerados na pasta `sounds/`

## Requisitos

Antes de rodar, instale as dependências do projeto:

- Python 3.10+
- `uv` instalado
- `espeak-ng` (recomendado para melhor suporte de fala)

No Linux, você pode instalar com:

```bash
sudo apt update
sudo apt install -y espeak-ng
```

Se estiver no Arch/Manjaro:

```bash
sudo pacman -Syu espeak-ng
```

## Instalação

Entre na pasta do projeto:

```bash
cd /home/pedrov12/Documentos/GitHub/C3PO-Assistente-Virtual-BR/tools/voz-TTS-pt-br
```

Instale as dependências com:

```bash
uv sync
```

Ou, se quiser instalar manualmente:

```bash
uv pip install kokoro>=0.9.4 soundfile sounddevice numpy
```

## Como rodar

Crie um arquivo de texto com o conteúdo que deseja transformar em áudio. Exemplo:

```txt
texto_entrada.txt
```

Conteúdo de exemplo:

```txt
Olá, tudo bem? Este é um teste de fala local com o Kokoro TTS.
```

Execute o script com:

```bash
uv run kokoro_tts_voz_local.py texto_entrada.txt
```

O comando acima:

1. lê o conteúdo do arquivo `texto_entrada.txt`
2. gera a fala localmente
3. toca o áudio
4. salva o resultado em `sounds/fala_completa.wav`
5. salva também os segmentos em `sounds/segmento_XX_fala_completa.wav`

## Como configurar as vozes

As vozes estão definidas no início do arquivo `kokoro_tts_voz_local.py`:

```python
VOICES = [
    "af_heart",
    "pf_dora",
    "pm_alex",
    "pm_santa"
]

VOICE = VOICES[2]
```

### Vozes disponíveis

- `af_heart` → voz padrão
- `pf_dora` → voz em português brasileiro
- `pm_alex` → voz em português brasileiro
- `pm_santa` → voz em português brasileiro

Para trocar a voz, edite a linha:

```python
VOICE = VOICES[2]
```

Por exemplo, para usar a voz `pf_dora`:

```python
VOICE = VOICES[1]
```

Ou para usar `pm_santa`:

```python
VOICE = VOICES[3]
```

## Saída de áudio

Os arquivos gerados ficam salvos na pasta:

```bash
sounds/
```

Exemplos:

- `sounds/fala_completa.wav`
- `sounds/segmento_01_fala_completa.wav`
- `sounds/segmento_02_fala_completa.wav`

## Estrutura do projeto

```text
.
├── kokoro_tts_voz_local.py
├── texto_entrada.txt
├── sounds/
└── README.md
```

## Observações

- O script usa o idioma `p` para português
- A taxa de amostragem está definida como `24000 Hz`
- Se quiser desativar a reprodução automática do áudio, altere o parâmetro `playback` no final do script

## Exemplo rápido

```bash
cd /home/pedrov12/Documentos/GitHub/C3PO-Assistente-Virtual-BR/tools/voz-TTS-pt-br
uv run kokoro_tts_voz_local.py texto_entrada.txt
```
