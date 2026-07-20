# 🤖 C3PO - Assistente Virtual Inteligente

![C3PO](https://moseisleychronicles.wordpress.com/wp-content/uploads/2015/11/untitled-215.gif)

## 📝 Descrição do projeto

C3PO é um assistente virtual inteligente desenvolvido em Python e React, inspirado no famoso droide de Star Wars. Ele é especializado em ajudar pessoas com TDAH a gerenciar suas tarefas, estudos e rotinas usando técnicas de Scrum e Kanban.

Atualmente ele possui sua interface em Streamlit para chatbot e configuraçao de voz nativa do python.



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
- Streamlit 
- CSS Moderno

---

## 🚀 Como Executar com interface Streamlit

```bash
pip install -r requirements.txt
```

```bash
streamlit run streamlit_c3po_dashboard_app.py
```

---

## 🚀 Como Executar com interface Web

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

---

## 🚀 Como Executar com Docker

- use o arquivo Dockerfile com o docker-compose para rodar o processo via CLI ou interface grafica

---

## 🚀 Como Executar Open Jarvis

O projeto oficial está completo no github: 

- https://github.com/open-jarvis/OpenJarvis

O OpenJarvis é essa pilha. É uma estrutura para a IA pessoal local, construída em torno de três ideias principais: primitivas compartilhadas para a construção de agentes no dispositivo; avaliações que tratam energia, FLOPs, latência e custo em dólar como restrições de primeira classe juntamente com a precisão; e um loop de aprendizado que melhora os modelos usando dados de rastreamento locais. O objetivo é simples: tornar possível a criação de agentes de IA pessoais que são executados localmente por padrão, chamando a nuvem apenas quando realmente necessário. O OpenJarvis pretende ser uma plataforma de pesquisa e uma base de produção para a IA local, no espírito da PyTorch.

- Um versão mais reduzida feita por um BR,  verifique os arquivos `/jarvis`

- É um projeto publico para uso de voz e ativação com palmas

- use o arquivo Dockerfile com o docker-compose para rodar o processo via CLI ou interface grafica


## Configurar a voz do Jarvis (ElevenLabs)

A voz do Jarvis usa o serviço ElevenLabs. Você precisa de duas informações dele: a API key e o Voice ID.

1. Crie uma conta em https://elevenlabs.io 
2. Gere uma API key nas configurações da sua conta (menu de developers > API Keys).   
3. clica em create api key, e depois create api key de novo (não precisa marcar nada).
4. Escolha uma voz em My Voices / Voice Library e copie o Voice ID dela.

Guarde a API key e o Voice ID — você vai usá-los no próximo passo.

> ℹ️ Sem essas duas informações, o Jarvis ainda roda, mas pula a fala de boas-vindas (as outras ações — Spotify, Chrome, Cursor — continuam funcionando).
>

## Criar o arquivo .env

O script carrega automaticamente um arquivo .env que deve ficar na mesma pasta do jarvis.py.

1. No editor, clique com o botão direito na pasta do projeto > New File > digite exatamente .env (com o ponto na frente e sem nenhuma extensão como .txt).
2. Cole dentro dele a sua API key e o seu Voice ID, usando os nomes exatos das variáveis abaixo.
3. Salve o arquivo (Ctrl + S / Cmd + S).

# Arquivo .env — deve ficar na MESMA pasta do jarvis.py

ELEVENLABS_API_KEY=sua_api_key_aqui

ELEVENLABS_VOICE_ID=seu_voice_id_aqui


## Rodar o Jarvis

1. No terminal do editor (dentro da pasta do projeto), rode:

```bash
python jarvis.py
```

1. Se o Windows pedir permissão para usar o microfone, permita.
2. Você deve ver o Jarvis iniciar e ficar ouvindo as palmas.
3. Bata palma duas vezes rápidas, assim: 👏👏

💡 Para parar o Jarvis, aperte Ctrl + C no terminal.


## O que o Jarvis faz

Jarvis é um script em Python que **fica ouvindo o seu microfone e, quando você bate palma duas vezes (*double-clap*), dispara uma sequência de boas-vindas estilo Jarvis** — abre o Spotify, janelas do Chrome, o Cursor e fala uma frase de boas-vindas usando a voz do ElevenLabs.

- **📦 Repositório oficial: https://github.com/hectorg2211/jarvis**

- https://political-cantaloupe-0db.notion.site/Como-instalar-o-Jarvis-no-seu-computador-do-zero-gr-tis-e-open-source-3926dd01fb4880f6a146e1eba48cef2c#3926dd01fb4880efb015c38dee0bd9dc

- https://github.com/open-jarvis/OpenJarvis

Não precisa saber programar para seguir este passo a passo. Basta ir fazendo cada etapa na ordem.

> ℹ️ **Observação:** o projeto foi feito e testado principalmente no Windows. No Mac/Linux algumas ações (abrir Spotify/Chrome/Cursor) podem precisar de ajustes no código.
>


---


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



## 👨‍💻 Desenvolvedor

- Pedro Victor Veras
  - Estudante de Engenharia Elétrica
  - Desenvolvedor Full Stack
  - Especialista em IA e Automação

## 🌟 Agradecimentos

Agradecimentos especiais à Codeium e à comunidade Star Wars por inspirarem este projeto!
