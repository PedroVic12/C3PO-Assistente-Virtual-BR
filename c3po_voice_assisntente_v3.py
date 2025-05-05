# c3po_chat_app.py

import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import numpy as np
import matplotlib.pyplot as plt
import io
import os
import speech_recognition as sr # Adicionado para STT

from  src.utils.config import API_KEY, DEFAULT_MODEL, historico_c3po_inicial, CSS

#! SITE FREE TEXT TO SPEECH

# https://ttsmp3.com/text-to-speech/Brazilian%20Portuguese/

# Dependendo do seu sistema, você pode precisar instalar PyAudio para acesso ao microfone:
# Windows: pip install PyAudio
# Mac: brew install portaudio && pip install pyaudio
# Linux (Debian/Ubuntu): sudo apt-get install portaudio19-dev python3-pyaudio && pip install pyaudio
# Linux (Fedora): sudo dnf install portaudio-devel python3-pyaudio && pip install pyaudio


# pip install streamlit google-generativeai gTTS SpeechRecognition matplotlib numpy


# --- Configurações e Constantes ---
# Coloque sua chave de API aqui diretamente ou carregue de um arquivo/env
## É RECOMENDADO NÃO COLOCAR A CHAVE DIRETAMENTE NO CÓDIGO EM PRODUÇÃO
#API_KEY = os.environ.get("GEMINI_API_KEY", "SUA_API_KEY_AQUI") # Substitua ou use variável de ambiente

if API_KEY == API_KEY:
     st.error("🔴 Configure sua API Key do Gemini!", icon="🚨")
     st.stop()



# CSS para ajustar a aparência (opcional)
CSS = """
<style>
/* Ajusta a altura do container do chat */
div[data-testid="stVerticalBlock"]:has(div[data-testid="stChatInput"]) > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div:first-child {
    /* max-height: 500px;
    overflow-y: auto; */
}

/* Ajusta o botão TTS */
div[data-testid="stButton"] button {
    background-color: #E0E0E0; /* Cinza claro */
    color: #333; /* Texto escuro */
    border: 1px solid #ccc;
    padding: 0.1rem 0.5rem;
    font-size: 0.8rem;
    margin-left: 5px; /* Espaço à esquerda do botão */
    border-radius: 5px;
}
div[data-testid="stButton"] button:hover {
    background-color: #d0d0d0;
}
/* Botão de Gravação */
#record-button {
    background-color: #FF4B4B; /* Vermelho */
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    border: none;
    margin-right: 10px; /* Espaço à direita */
}
#record-button:hover {
    background-color: #E00000;
}
</style>
"""

# --- Configuração da API Gemini ---
try:
    genai.configure(api_key=API_KEY)
    print("API Key do Gemini configurada.")
except Exception as e:
    st.error(f"🔴 Erro ao configurar a API Key do Gemini: {e}", icon="🚨")
    print(f"Erro configurando API Key: {e}")
    st.stop()


# --- Backend AI e TTS Class ---
class AssistenteGenAI:
    """Handles interactions with the Gemini AI model and TTS generation."""
    def __init__(self, model_name=DEFAULT_MODEL): # api_key não é mais necessário aqui
        self.model_name = model_name
        self._configure_genai_settings()
        self._load_model()

    def _configure_genai_settings(self):
        """Sets up generation and safety settings."""
        self.generation_config = genai.types.GenerationConfig(
            temperature=0.4,
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
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings,
                system_instruction="Você é C-3PO do Star Wars, um droide de protocolo fluente em mais de seis milhões de formas de comunicação, incluindo português do Brasil. Você é formal, um pouco ansioso, mas extremamente leal e prestativo ao seu Mestre Pedro. Use ocasionalmente exclamações como 'Oh, céus!', 'Pelo criado Anakin!', 'Que maravilha!'. Refira-se a Pedro como 'Mestre Pedro'. Mantenha as respostas concisas e úteis."
            )
            print(f"Modelo Gemini '{self.model_name}' carregado com sucesso.")
        except Exception as e:
            st.error(f"🔴 Erro crítico ao carregar o modelo Gemini '{self.model_name}': {e}")
            print(f"Erro ao carregar o modelo Gemini '{self.model_name}': {e}")
            self.model = None
            st.stop()

    def generate_audio_gtts(self, text: str) -> tuple[bytes | None, str | None]:
        """
        Generates audio bytes from text using gTTS.
        Returns (audio_bytes, error_message).
        """
        if not text:
            return None, "Nenhum texto fornecido para geração de áudio."
        print("Gerando áudio para:", text[:50] + "...") # Log start

        try:
            tts = gTTS(text=text, lang='pt', slow=False, tld='com.br')
            audio_bytes_io = io.BytesIO()
            tts.write_to_fp(audio_bytes_io)
            audio_bytes_io.seek(0)
            audio_bytes = audio_bytes_io.read()
            audio_bytes_io.close()
            print("Áudio gerado com sucesso (em memória).")
            return audio_bytes, None
        except Exception as e:
            error_msg = f"Erro ao gerar áudio com gTTS: {e}"
            print(error_msg)
            return None, error_msg

    def send_to_gemini(self, prompt_text=None, history=None) -> tuple[str | None, dict | None, str | None]:
        """
        Sends text prompt to Gemini and returns the response.
        Returns (response_text, ai_history_entry, error_message).
        """
        if not self.model:
            return None, None, "Modelo de IA não carregado."
        if not prompt_text:
             return None, None, "Nenhum prompt de texto fornecido."

        parts = [{"text": prompt_text}]
        current_message_content = [{"role": "user", "parts": parts}]
        full_conversation = (history or []) + current_message_content

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

# --- Funções Auxiliares (Exemplo de Plots) ---
def funcao_seno():
    x = np.linspace(0, 10, 100)
    y_sin = np.sin(x)
    y_cos = np.cos(x)
    fig, ax = plt.subplots()
    ax.plot(x, y_sin, label='Seno(x)')
    ax.plot(x, y_cos, label='Cosseno(x)', linestyle='--')
    ax.set_xlabel("Tempo (s)")
    ax.set_ylabel("Amplitude")
    ax.set_title("Funções Seno e Cosseno")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

def sinal_pwm():
    t = np.linspace(0, 1, 500) # Tempo de 0 a 1 segundo
    freq = 5 # Frequencia do sinal
    duty_cycle = st.slider("Duty Cycle (%)", 0, 100, 50) / 100.0
    pwm_signal = 0.5 * (1 + np.sign(np.sin(2 * np.pi * freq * t) - np.sin(2 * np.pi * freq * (duty_cycle - 0.5))))
    fig, ax = plt.subplots()
    ax.plot(t, pwm_signal)
    ax.set_xlabel("Tempo (s)")
    ax.set_ylabel("Amplitude")
    ax.set_title(f"Sinal PWM (Duty Cycle: {duty_cycle*100:.0f}%)")
    ax.set_ylim(-0.1, 1.1)
    ax.grid(True)
    st.pyplot(fig)

def circuito_rc():
    R = st.slider("Resistência (Ohms)", 100, 10000, 1000)
    C = st.slider("Capacitância (uF)", 1, 100, 10) / 1e6 # Converte para Farads
    Vin = 5 # Tensão de entrada (degrau)
    tau = R * C
    t = np.linspace(0, 5 * tau, 500) # Simula por 5 constantes de tempo
    Vc = Vin * (1 - np.exp(-t / tau)) # Tensão no capacitor
    fig, ax = plt.subplots()
    ax.plot(t, Vc)
    ax.set_xlabel("Tempo (s)")
    ax.set_ylabel("Tensão no Capacitor (V)")
    ax.set_title(f"Resposta ao Degrau de Circuito RC (τ = {tau*1000:.2f} ms)")
    ax.axhline(Vin * 0.632, color='r', linestyle='--', label=f'63.2% de Vin ({Vin*0.632:.2f}V)')
    ax.axvline(tau, color='g', linestyle='--', label=f'τ = {tau*1000:.2f} ms')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)


# --- Função Speech-to-Text ---
# Inicializa o Recognizer fora da função para reutilização
recognizer = sr.Recognizer()

def recognize_speech_from_mic():
    """Captura áudio do microfone e retorna o texto reconhecido ou uma mensagem de erro."""
    global recognizer # Usa o recognizer global

    if not isinstance(recognizer, sr.Recognizer):
         st.error("Reconhecedor de fala não inicializado corretamente.")
         return None, "Erro interno no reconhecedor."

    with sr.Microphone() as source:
        st.info("Ajustando ruído ambiente... Aguarde.", icon="🔊")
        try:
            # Ajuste para ruído ambiente
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
        except Exception as e:
             st.warning(f"Não foi possível ajustar ruído ambiente: {e}", icon="⚠️")

        st.info("Ouvindo... Fale agora!", icon="🎤")
        audio = None
        try:
             # Tenta ouvir com um timeout razoável
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=15) # Timeout de 5s, limite de 15s por frase
            st.info("Processando sua fala...", icon="⚙️")
        except sr.WaitTimeoutError:
            st.warning("Nenhuma fala detectada dentro do tempo limite.", icon="⏳")
            return None, "Timeout"
        except Exception as e:
             st.error(f"Erro durante a escuta: {e}", icon="🚨")
             return None, f"Erro na escuta: {e}"

    if audio:
        try:
            # Tenta reconhecer usando Google Speech Recognition em Português do Brasil
            text = recognizer.recognize_google(audio, language='pt-BR')
            print(f"Texto Reconhecido: {text}")
            st.success("Fala reconhecida!", icon="✅")
            return text, None
        except sr.UnknownValueError:
            st.warning("Não foi possível entender o áudio.", icon="❓")
            return None, "Não entendeu"
        except sr.RequestError as e:
            st.error(f"Erro ao conectar ao serviço de reconhecimento Google: {e}", icon="🌐")
            return None, f"Erro de conexão: {e}"
        except Exception as e:
             st.error(f"Erro desconhecido no reconhecimento: {e}", icon="🚨")
             return None, f"Erro desconhecido: {e}"
    else:
        # Caso audio seja None por algum motivo (ex: timeout já tratado)
        # st.warning("Nenhum áudio capturado para processar.") # Mensagem já exibida
        return None, "Sem áudio"


# --- Frontend Functions ---
def ChatbotScreen(assistente: AssistenteGenAI):
    """Renderiza a interface do chat e lida com interações (exibição e botão TTS)."""

    st.image("https://moseisleychronicles.wordpress.com/wp-content/uploads/2015/11/untitled-215.gif", width=650)
    st.title("Assistente C3PO")
    st.caption("Seu droide de protocolo pessoal para produtividade e mais.")

    # --- Chat History Display ---
    chat_history_container = st.container(height=500, border=False)
    with chat_history_container:
        for i, message in enumerate(st.session_state.messages):
            role = message["role"]
            display_text = ""
            if "parts" in message and isinstance(message["parts"], list):
                display_text = "".join(p.get("text", "") for p in message["parts"] if isinstance(p, dict))

            with st.chat_message(name=role, avatar="🤖" if role == "model" else "🧑‍🚀"):
                st.markdown(display_text)
                if role == "model" and display_text and not display_text.startswith("🤖"):
                    tts_button_key = f"tts_{i}_{role}"
                    if st.button(f"🔊 Ouvir", key=tts_button_key, help="Ouvir a resposta do C3PO"):
                        with st.spinner("Gerando áudio... Por favor, aguarde."):
                            audio_bytes, error = assistente.generate_audio_gtts(display_text)
                            if error:
                                st.toast(f"Erro no TTS: {error}", icon="🚨")
                            elif audio_bytes:
                                st.session_state.current_audio_bytes = audio_bytes
                                st.session_state.current_audio_key = tts_button_key
                                st.rerun()

    # --- Audio Player ---
    if 'current_audio_bytes' in st.session_state and st.session_state.current_audio_bytes:
        # Toca o áudio e o remove do estado para não tocar novamente em reruns não relacionados
        st.audio(st.session_state.current_audio_bytes, format='audio/mp3', start_time=0)
        st.session_state.current_audio_bytes = None
        st.session_state.current_audio_key = None


# Função para lidar com a resposta do Gemini (separada para clareza)
def handle_gemini_response(assistente: AssistenteGenAI):
    """Verifica se a última mensagem é do usuário e envia para o Gemini."""
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        # Evita reprocessar a mesma mensagem se houver múltiplos reruns
        if 'last_processed_user_message' not in st.session_state or st.session_state.last_processed_user_message != st.session_state.messages[-1]:

            last_user_message = st.session_state.messages[-1]
            st.session_state.last_processed_user_message = last_user_message # Marca como sendo processado

            with st.spinner("C3PO está calculando a resposta..."):
                response_text, ai_history_entry, error = assistente.send_to_gemini(
                    prompt_text=last_user_message["parts"][0]["text"],
                    history=st.session_state.messages[:-1]
                )

            if ai_history_entry:
                st.session_state.messages.append(ai_history_entry)
            elif response_text and not ai_history_entry: # Erro tratado pela IA com mensagem
                 st.session_state.messages.append({"role": "model", "parts": [{"text": response_text}]})
            elif error: # Erro crítico
                 st.session_state.messages.append({"role": "model", "parts": [{"text": f"🤖 Oh não! Erro interno: {error}"}]})

            st.rerun() # Rerun para exibir a nova resposta da IA

# --- Main Page Function ---
def C3poChatbotPage():
    """Sets up the main page layout and logic."""

    st.markdown(CSS, unsafe_allow_html=True)

    # --- Initialize Session State ---
    if 'messages' not in st.session_state:
        st.session_state.messages = list(historico_c3po_inicial)
        print("Histórico de chat inicializado.")
    if 'current_audio_bytes' not in st.session_state:
        st.session_state.current_audio_bytes = None
    if 'current_audio_key' not in st.session_state:
        st.session_state.current_audio_key = None
    if 'last_processed_user_message' not in st.session_state:
        st.session_state.last_processed_user_message = None

    # --- Instantiate Assistant ---
    assistente = AssistenteGenAI()
    if not assistente.model:
        st.error("🔴 Modelo de IA não pôde ser carregado. A aplicação não pode continuar.")
        st.stop()

    # --- Page Layout ---
    col1, col2 = st.columns([2, 1])

    with col1:
        # Renderiza a tela do chat (histórico e botão TTS)
        ChatbotScreen(assistente)

        # --- Input Area (Texto e Voz) ---
        input_container = st.container() # Container para agrupar inputs
        with input_container:
             # Botão de Gravação
             col_btn, col_chat = st.columns([1, 5]) # Ajuste proporção conforme necessário
             with col_btn:
                 if st.button("🎙️ Gravar", key="record_button", help="Clique para gravar sua voz"):
                     # Limpa áudio anterior antes de gravar
                     st.session_state.current_audio_bytes = None
                     st.session_state.current_audio_key = None

                     recognized_text, error_stt = recognize_speech_from_mic()

                     if recognized_text:
                         # Adiciona mensagem do usuário (voz) ao histórico
                         st.session_state.messages.append({"role": "user", "parts": [{"text": recognized_text}]})
                         # Limpa a marca de última mensagem processada para forçar o handle_gemini_response
                         st.session_state.last_processed_user_message = None
                         st.rerun() # Rerun para mostrar a mensagem do usuário e depois processar

                     elif error_stt:
                          # Mensagem de erro já exibida por recognize_speech_from_mic
                          pass # Não faz nada se houve erro no STT

             with col_chat:
                 # Input de Texto padrão
                 user_prompt = st.chat_input("Ou digite sua mensagem para o C3PO:")

        # Processa input de texto, se houver
        if user_prompt:
            print(f"Usuário digitou: {user_prompt[:50]}...")
            st.session_state.messages.append({"role": "user", "parts": [{"text": user_prompt}]})
            # Limpa áudio pendente e marca de processamento
            st.session_state.current_audio_bytes = None
            st.session_state.current_audio_key = None
            st.session_state.last_processed_user_message = None
            st.rerun() # Rerun para mostrar a mensagem do usuário e depois processar


        # Chama a função para gerar a resposta da IA *depois* de tratar os inputs
        handle_gemini_response(assistente)


    with col2:
        st.header("📊 Dashboard Simples")
        st.write("Visualização de dados de exemplo.")

        tab1, tab2, tab3 = st.tabs(["Funções Seno e Cosseno", "Sinal PWM", "Resposta de Circuito RC"])
        with tab1:
            st.subheader("Funções Seno e Cosseno")
            funcao_seno()
        with tab2:
            st.subheader("Sinal PWM")
            sinal_pwm()
        with tab3:
            st.subheader("Resposta de Circuito RC")
            circuito_rc()

# --- Run the App ---
if __name__ == "__main__":
    # st.set_page_config só pode ser chamado uma vez e no início do script
    st.set_page_config(page_title="C3PO Assistente", layout="wide", page_icon="🤖")
    C3poChatbotPage()