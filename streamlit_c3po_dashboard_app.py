import streamlit as st
import google.generativeai as genai
import numpy as np
import matplotlib.pyplot as plt
import io
import os
import asyncio
import edge_tts
from PIL import Image
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env (com override=True)
load_dotenv(override=True)

from src.utils.config import API_KEY, DEFAULT_MODEL, historico_c3po_inicial, CSS, available_models_list

#! SITE FREE TEXT TO SPEECH

# https://ttsmp3.com/text-to-speech/Brazilian%20Portuguese/


#! Debugar questoes de imports dos graficos e tabelas de engenharia eletrica alimentando LLM no setup

#from src.utils import funcao_seno, sinal_pwm, circuito_rc

# --- Helper function for personal context injection ---
def carregar_contexto_projetos():
    contexto = ""
    try:
        context_path = "/home/pedrov12/Documentos/GitHub/.agents/contexto_projetos.txt"
        if os.path.exists(context_path):
            with open(context_path, "r", encoding="utf-8") as f:
                contexto += "\n--- CONTEXTO DOS PROJETOS DO MESTRE PEDRO ---\n" + f.read()
    except Exception as e:
        print("Erro ao ler contexto_projetos.txt:", e)
        
    try:
        rules_path = "/home/pedrov12/Documentos/GitHub/.agents/AGENTS.md"
        if os.path.exists(rules_path):
            with open(rules_path, "r", encoding="utf-8") as f:
                contexto += "\n--- REGRAS DE OURO E LIMITE WIP DO MESTRE PEDRO ---\n" + f.read()
    except Exception as e:
        print("Erro ao ler AGENTS.md:", e)
        
    return contexto

# --- Backend AI and TTS Class ---
class AssistenteGenAI:
    """Handles interactions with the Gemini AI model and TTS generation."""
    def __init__(self, model_name=DEFAULT_MODEL, api_key=None):
        self.model_name = model_name
        self.api_key = api_key # Store the key if needed elsewhere, though genai config is global
        self.contexto_extra = carregar_contexto_projetos()
        self._configure_genai_settings()
        self._load_model()

    def _configure_genai_settings(self):
        """Sets up generation and safety settings."""
        # Note: genai.configure(api_key=...) should already be done outside
        self.generation_config = genai.types.GenerationConfig(
            temperature=0.4, # Adjusted for more consistent C3PO persona
            top_k=40,
            top_p=0.95,
            candidate_count=1,
        )
        self.safety_settings = [
             {"category": c, "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
             for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH",
                       "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]
        ]

    def _load_model(self):
        """Loads the generative model."""
        try:
            # Build custom system instruction containing personal context, rules and repository capabilities
            capabilities = (
                "\n--- ESTRUTURA E CAPACIDADES DO SEU REPOSITÓRIO (C3PO-Assistente-Virtual-BR) ---\n"
                "Você reside dentro do repositório 'C3PO-Assistente-Virtual-BR'. Aqui está a estrutura de arquivos e o que cada um deles faz para que você possa guiar o Mestre Pedro:\n"
                "- `streamlit_c3po_dashboard_app.py`: Sua interface principal do Chatbot e Dashboard em Streamlit, utilizando voz masculina Edge-TTS (pt-BR-AntonioNeural) com suporte a uploads de imagens e busca integrada do Google.\n"
                "- `app.py`: Um servidor web Flask local que atua como backend/API de controle.\n"
                "- `requirements.txt`: Dependências Python do projeto (Streamlit, Flask, gTTS, edge-tts, etc.).\n"
                "- `tools/agent_toolbelt.py`: Um painel CLI de controle para a Batcaverna, capaz de verificar o status dos serviços locais (Flask, Astro Blog, Pikachu-Flask-Server), ler regras e contextos do Segundo Cérebro, e emitir voz local via terminal.\n"
                "- `tools/c3po_voice_alerts.py`: Utilitário para acionar alertas sonoros no Linux usando spd-say, pyttsx3, gTTS ou espeak.\n"
                "- `run_toolbelt.sh`: Um script shell para inicializar o painel CLI.\n"
                "- `c3po_notificador.py`: Um automatizador de notificações no sistema."
            )
            system_instruction = (
                "Você é C-3PO do Star Wars, um droide de protocolo fluente em mais de seis milhões de formas de comunicação, incluindo português do Brasil. "
                "Você é formal, um pouco ansioso, mas extremamente leal e prestativo ao seu Mestre Pedro. "
                "Use ocasionalmente exclamações como 'Oh, céus!', 'Pelo criado Anakin!', 'Que maravilha!'. "
                "Refira-se a Pedro como 'Mestre Pedro'. Mantenha as respostas concisas e úteis.\n\n"
                f"Aqui está o contexto real dos projetos atuais e a rotina do Mestre Pedro:\n{self.contexto_extra}\n{capabilities}"
            )
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings,
                system_instruction=system_instruction,
                tools=["google_search_retrieval"]
            )
            print(f"Modelo Gemini '{self.model_name}' carregado com sucesso.")
        except Exception as e:
            st.error(f"🔴 Erro crítico ao carregar o modelo Gemini '{self.model_name}': {e}")
            print(f"Erro ao carregar o modelo Gemini '{self.model_name}': {e}")
            self.model = None
            st.stop() # Stop if model fails to load

    def generate_audio_gtts(self, text: str) -> tuple[bytes | None, str | None]:
        """
        Generates audio bytes from text using Microsoft Edge TTS (free, male Brazilian voice: pt-BR-AntonioNeural).
        Returns (audio_bytes, error_message).
        """
        if not text:
            return None, "Nenhum texto fornecido para geração de áudio."
        
        print("Gerando áudio via Edge-TTS para:", text[:50] + "...")
        try:
            communicate = edge_tts.Communicate(text, "pt-BR-AntonioNeural")
            
            # Helper to run async stream in synchronous context
            async def get_bytes():
                audio_data = b""
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_data += chunk["data"]
                return audio_data

            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
            audio_bytes = loop.run_until_complete(get_bytes())
            print("Áudio gerado com sucesso via Edge-TTS.")
            return audio_bytes, None
        except Exception as e:
            error_msg = f"Erro ao gerar áudio com Edge-TTS: {e}"
            print(error_msg)
            return None, error_msg

    def send_to_gemini(self, prompt_text=None, history=None, image=None) -> tuple[str | None, dict | None, str | None]:
        """
        Sends text prompt and optional image to Gemini and returns the response.
        Returns (response_text, ai_history_entry, error_message).
        """
        if not self.model:
            return None, None, "Modelo de IA não carregado."

        if not prompt_text:
             return None, None, "Nenhum prompt de texto fornecido."

        # Prepare parts for the current message
        parts = []
        if image:
            parts.append(image) # PIL Image
        parts.append(prompt_text)

        # Build clean conversation history format for API
        full_conversation = []
        for h in (history or []):
            api_parts = []
            for p in h["parts"]:
                if isinstance(p, dict) and "text" in p:
                    api_parts.append(p["text"])
                elif isinstance(p, str):
                    api_parts.append(p)
            if "image_pil" in h and h["image_pil"]:
                api_parts.insert(0, h["image_pil"])
            full_conversation.append({"role": h["role"], "parts": api_parts})

        # Append current user prompt
        full_conversation.append({"role": "user", "parts": parts})

        print(f"Enviando para Gemini (Histórico: {len(history or [])} msgs): {prompt_text[:50]}...")

        try:
            response = self.model.generate_content(
                contents=full_conversation,
                stream=False
            )
            response.resolve()

            if response.candidates and response.candidates[0].content.parts:
                response_text = "".join(part.text for part in response.candidates[0].content.parts if hasattr(part, 'text'))
                ai_response_for_history = {"role": "model", "parts": [{"text": response_text}]}
                print(f"Gemini respondeu: {response_text[:50]}...")
                return response_text, ai_response_for_history, None
            else:
                 # Handle blocked or empty responses
                 finish_reason = "N/A"
                 block_reason = "N/A"
                 safety_feedback_str = "N/A"
                 if hasattr(response, 'prompt_feedback'):
                     safety_feedback_str = str(response.prompt_feedback)
                 if response.candidates:
                    candidate = response.candidates[0]
                    finish_reason = candidate.finish_reason.name if hasattr(candidate.finish_reason, 'name') else str(candidate.finish_reason)
                    if finish_reason == 'SAFETY' and candidate.safety_ratings:
                        block_reason = candidate.safety_ratings[0].category.name if hasattr(candidate.safety_ratings[0].category, 'name') else str(candidate.safety_ratings[0].category)

                 error_msg = f"Nenhuma resposta de texto recebida da IA. Razão: {finish_reason}. Bloqueio: {block_reason}. Feedback: {safety_feedback_str}"
                 print(f"Erro Gemini: {error_msg}")
                 return f"🤖 Oh céus! Não posso processar isso. ({error_msg})", None, error_msg

        except Exception as e:
            error_msg = f"Erro ao comunicar com a API Gemini: {e}"
            print(f"Erro Gemini: {error_msg}")
            return f"🤖 Houve um erro: {error_msg}", None, error_msg


C3PO_AVATAR = "https://cdn-icons-png.flaticon.com/512/3233/3233483.png"
USER_AVATAR = "https://cdn-icons-png.flaticon.com/512/1144/1144760.png"

def ChatHistoryDisplay(assistente: AssistenteGenAI):
    # --- Chat History Display ---
    setup_indices = [0, 2, 3, 4, 5]
    
    # Render alignment configurations inside expander
    with st.expander("📜 Ver Alinhamento de Configuração do C-3PO", expanded=False):
        for idx in setup_indices:
            if idx < len(st.session_state.messages):
                message = st.session_state.messages[idx]
                role = message["role"]
                display_text = "".join(p.get("text", "") for p in message["parts"] if isinstance(p, dict))
                with st.chat_message(name=role, avatar=C3PO_AVATAR if role == "model" else USER_AVATAR):
                    st.markdown(display_text)
                    
    # Visible messages to render on the main chat screen (expanded layout)
    visible_messages = []
    # 1. Greeting message is at index 1 of historico_c3po_inicial
    if len(st.session_state.messages) > 1:
        visible_messages.append((1, st.session_state.messages[1]))
        
    # 2. Live conversation messages
    for i in range(len(historico_c3po_inicial), len(st.session_state.messages)):
        visible_messages.append((i, st.session_state.messages[i]))
        
    # Render all visible messages
    for idx, message in visible_messages:
        role = message["role"]
        display_text = "".join(p.get("text", "") for p in message["parts"] if isinstance(p, dict))
        
        with st.chat_message(name=role, avatar=C3PO_AVATAR if role == "model" else USER_AVATAR):
            # Render uploaded image if present in the message
            if "image_bytes" in message and message["image_bytes"]:
                st.image(message["image_bytes"], caption="Imagem enviada", width=300)
            st.markdown(display_text)
            
            # Add TTS button only for non-empty model messages
            if role == "model" and display_text and not display_text.startswith("🤖"):
                tts_button_key = f"tts_visible_{idx}" # Unique key based on original index
                if st.button(f"🔊 Ouvir", key=tts_button_key, help="Ouvir a resposta do C3PO"):
                    with st.spinner("Gerando áudio... Por favor, aguarde."):
                        audio_bytes, error = assistente.generate_audio_gtts(display_text)
                        if error:
                            st.toast(f"Erro no TTS: {error}", icon="🚨")
                        elif audio_bytes:
                            st.session_state.current_audio_bytes = audio_bytes
                            st.session_state.current_audio_key = tts_button_key
                            st.rerun()

# --- Frontend Functions ---
def ChatbotScreen(assistente: AssistenteGenAI):
    """Renders the chat interface and handles interactions."""

    st.title("Assistente C3PO")
    st.image("https://moseisleychronicles.wordpress.com/wp-content/uploads/2015/11/untitled-215.gif", width=650)
    st.text("Seu droide de protocolo pessoal para produtividade, gerenciamento de tarefas, TDAH e Rotina.")

    ChatHistoryDisplay(assistente)

    # --- Audio Player ---
    # Display audio player and autoplay if set
    if 'current_audio_bytes' in st.session_state and st.session_state.current_audio_bytes:
         st.audio(st.session_state.current_audio_bytes, format='audio/mp3', start_time=0, autoplay=True)
         # Clear the audio after displaying it once to prevent re-playing on next rerun
         st.session_state.current_audio_bytes = None
         st.session_state.current_audio_key = None

    # --- User Input ---
    user_prompt = st.chat_input("Digite sua mensagem para o C3PO:")
    if user_prompt:
        print(f"Usuário digitou: {user_prompt[:50]}...")
        user_msg = {"role": "user", "parts": [{"text": user_prompt}]}
        
        # Check if there is an uploaded image in session state
        uploaded_image = st.session_state.get("uploaded_image_file")
        if uploaded_image:
            user_msg["image_pil"] = Image.open(uploaded_image)
            user_msg["image_bytes"] = uploaded_image.getvalue()
            
        # Append user message to state immediately for display
        st.session_state.messages.append(user_msg)
        
        # Clear any pending audio playback before showing spinner/getting response
        st.session_state.current_audio_bytes = None
        st.session_state.current_audio_key = None
        st.rerun() # Rerun to show user message instantly

# Separate function to handle the Gemini response after the user message is shown
def handle_gemini_response(assistente: AssistenteGenAI):
    # Check all user messages in chat history
    user_messages = [m for m in st.session_state.messages if m["role"] == "user"]
    num_user_messages = len(user_messages)
    
    # Initialize processed counter if not in session state
    if "processed_user_messages_count" not in st.session_state:
        initial_user_count = sum(1 for m in st.session_state.messages[:len(historico_c3po_inicial)] if m["role"] == "user")
        st.session_state.processed_user_messages_count = initial_user_count

    # Check if there is a new user message to process
    if num_user_messages > st.session_state.processed_user_messages_count:
        # Mark as processed immediately
        st.session_state.processed_user_messages_count = num_user_messages
        
        last_user_message = user_messages[-1]

        with st.spinner("C3PO está calculando a resposta..."):
            # Pass optional image to gemini call
            image_pil = last_user_message.get("image_pil")
            
            # Use history before the latest user message
            history_before = [m for m in st.session_state.messages if m is not last_user_message]
            
            response_text, ai_history_entry, error = assistente.send_to_gemini(
                prompt_text=last_user_message["parts"][0]["text"],
                history=history_before,
                image=image_pil
            )

        # If Gemini returned a valid response structure, add it to history
        if ai_history_entry:
            st.session_state.messages.append(ai_history_entry)
            # Auto generate audio for the response if Autoplay is enabled in the sidebar/session_state
            if st.session_state.get("autoplay_voice", True):
                audio_bytes, error_audio = assistente.generate_audio_gtts(response_text)
                if audio_bytes:
                    st.session_state.current_audio_bytes = audio_bytes
                    st.session_state.current_audio_key = "auto_response"
        # If there was an error but Gemini generated an error message text
        elif response_text and not ai_history_entry:
             st.session_state.messages.append({"role": "model", "parts": [{"text": response_text}]})
        # If there was a critical error and no text response
        elif error:
             st.session_state.messages.append({"role": "model", "parts": [{"text": f"🤖 Oh não! Erro interno: {error}"}]})

        # Rerun to display the new AI response
        st.rerun()


# --- Main Page Function ---
def C3poChatbotPage():
    """Sets up the main page layout and logic."""
    
    # --- Apply CSS ---
    st.markdown(CSS, unsafe_allow_html=True)

    # --- Initialize Session State ---
    if 'messages' not in st.session_state:
        # Start with a fresh copy of the initial history
        st.session_state.messages = list(historico_c3po_inicial)
        print("Histórico de chat inicializado.")

    if 'current_audio_bytes' not in st.session_state:
        st.session_state.current_audio_bytes = None
    if 'current_audio_key' not in st.session_state:
        st.session_state.current_audio_key = None
    if 'processed_user_messages_count' not in st.session_state:
        initial_user_count = sum(1 for m in st.session_state.messages if m["role"] == "user")
        st.session_state.processed_user_messages_count = initial_user_count

    # --- Initialize Selected Model ---
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = DEFAULT_MODEL

    # --- Sidebar Controls & Context ---
    st.sidebar.title("🛠️ Configurações C-3PO")
    st.sidebar.checkbox("Autoplay Voz", value=True, key="autoplay_voice")
    
    # Model Selection Dropdown
    model_idx = 0
    if st.session_state.selected_model in available_models_list:
        model_idx = available_models_list.index(st.session_state.selected_model)
    selected_model = st.sidebar.selectbox(
        "🤖 Modelo Gemini",
        options=available_models_list,
        index=model_idx,
        help="Escolha o modelo da API do Gemini."
    )
    if selected_model != st.session_state.selected_model:
        st.session_state.selected_model = selected_model
        st.rerun()

    st.sidebar.success("🔊 Voz Masculina Edge-TTS: ATIVA (pt-BR-AntonioNeural)")

    # --- Instantiate Assistant ---
    # Pass the selected model and API key
    assistente = AssistenteGenAI(model_name=st.session_state.selected_model, api_key=API_KEY)
    if not assistente.model: # Check if model loaded successfully
         st.error("🔴 Modelo de IA não pôde ser carregado. A aplicação não pode continuar.")
         st.stop()
    
    st.sidebar.markdown("---")
    # File uploader for images
    uploaded_image = st.sidebar.file_uploader("📸 Anexar Imagem para C3PO", type=["png", "jpg", "jpeg"], key="uploaded_image_file")
    if uploaded_image:
         st.sidebar.image(uploaded_image, caption="Imagem anexada para o próximo prompt", use_container_width=True)
         
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧠 Contexto & Memória do Mestre Pedro")
    st.sidebar.info(f"O C-3PO leu com sucesso {len(assistente.contexto_extra)} caracteres do seu Segundo Cérebro.")
    st.sidebar.text_area("Contexto Carregado", assistente.contexto_extra, height=350)

    # --- Page Layout ---
    col1, col2 = st.columns([2, 1]) # Chat takes more space

    with col1:
        # Render the chat screen (displays history, handles input)
        ChatbotScreen(assistente)
        # Handle the response generation *after* potential input/rerun
        handle_gemini_response(assistente)


    # with col2:
    #     st.header("📊 Dashboard Simples")
    #     st.write("Visualização de dados de exemplo.")
        
    #     # Criação das abas
    #     tab1, tab2, tab3 = st.tabs(["Funções Seno e Cosseno", "Sinal PWM", "Resposta de Circuito RC"])
    #     with tab1:
    #         st.subheader("Funções Seno e Cosseno")
    #         funcao_seno()

    #     with tab2:
    #         st.subheader("Sinal PWM")
    #         sinal_pwm()

    #     with tab3:
    #         st.subheader("Resposta de Circuito RC")
    #         circuito_rc()

# --- Run the App ---
if __name__ == "__main__":
    C3poChatbotPage()
