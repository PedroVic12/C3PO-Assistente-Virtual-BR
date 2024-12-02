# 🤖 C3PO - Assistente Virtual Inteligente

![C3PO](https://moseisleychronicles.wordpress.com/wp-content/uploads/2015/11/untitled-215.gif)

## 📝 Descrição
C3PO é um assistente virtual inteligente desenvolvido em Python e React, inspirado no famoso droide de Star Wars. Ele é especializado em ajudar pessoas com TDAH a gerenciar suas tarefas, estudos e rotinas usando técnicas de Scrum e Kanban.

## ✨ Funcionalidades

- 💬 Chat interativo com interface Star Wars
- 🎙️ Entrada e saída de voz
- 📊 Gerenciamento de tarefas com Kanban
- ⏱️ Técnica Pomodoro integrada
- 🧠 Suporte especializado para TDAH
- 📚 Auxílio em estudos e programação
- 🎯 Foco em produtividade e organização

## 🛠️ Tecnologias

### Backend
- Python 3.12+
- Flask
- Google Gemini AI
- Speech Recognition
- ElevenLabs (Text-to-Speech)

### Frontend
- React
- TypeScript
- Vite
- CSS Moderno

## 🚀 Como Executar

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/C3PO-Assistente-Virtual-BR.git
cd C3PO-Assistente-Virtual-BR
```

2. Configure o ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
cd frontend && npm install
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas chaves API
```

5. Inicie os servidores:
```bash
# Terminal 1 - Backend
python app.py

# Terminal 2 - Frontend
cd frontend && npm run dev
```

## 🎯 Recursos Principais

- **Gerenciamento de Tarefas**
  - Organização com Kanban
  - Priorização inteligente
  - Lembretes e notificações

- **Suporte ao TDAH**
  - Técnicas de foco
  - Gestão de tempo
  - Hiperfoco produtivo

- **Assistente de Estudos**
  - Programação
  - Engenharia Elétrica
  - Artigos Científicos

## 🔔 Alarm Clock Feature

The C3PO now includes a modern alarm clock feature with a graphical interface built using Flet. Here's what was implemented:

### Features
- Modern dark-themed UI
- Sound file selection for alarm
- Time selection using dropdowns (hours, minutes, seconds)
- Start/Stop alarm functionality
- Background alarm monitoring
- Visual feedback and status updates

### How to Use
1. Launch the alarm clock:
   ```bash
   python src/alarm_clock.py
   ```

2. Select your alarm sound:
   - Click "Pick sound file"
   - Choose an MP3 or WAV file
   - The selected file name will be displayed

3. Set the alarm time:
   - Use the dropdowns to select hours, minutes, and seconds
   - The time is in 24-hour format

4. Control the alarm:
   - Click "Start Alarm" to set it
   - Click "Stop Alarm" to cancel it
   - Current status is shown below the buttons

### Technical Details
- Built with Flet for modern UI
- Uses pygame for sound playback
- Runs alarm in background thread
- Supports MP3 and WAV audio formats
- Real-time status updates
- Thread-safe implementation

### Dependencies
- Flet
- Pygame
- Python standard libraries (datetime, threading)

## 👨‍💻 Desenvolvedor

- Pedro Victor Veras
  - Estudante de Engenharia Elétrica
  - Desenvolvedor Full Stack
  - Especialista em IA e Automação

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🌟 Agradecimentos

Agradecimentos especiais à Codeium e à comunidade Star Wars por inspirarem este projeto!
