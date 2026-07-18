import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# Carrega variáveis do arquivo .env (com override=True para garantir que as alterações no .env se sobreponham a variáveis globais do sistema)
load_dotenv(override=True)

# --- API Key Configuration ---
# Prioridade máxima para as variáveis do arquivo .env ou ambiente do Render
API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("API_KEY")

if not API_KEY:
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        # Fallback se nenhuma chave for encontrada
        API_KEY = None

try:
    if API_KEY:
        genai.configure(api_key=API_KEY)
        print("Gemini API Key configured successfully.")
    else:
        print("Aviso: Nenhuma Gemini API Key configurada. Por favor, adicione GEMINI_API_KEY no arquivo .env.")
except Exception as e:
    st.error(f"🔴 **Erro Crítico:** Falha ao configurar a API Gemini: {e}")
    st.stop()

# --- Model Discovery ---
# Escolhe automaticamente o primeiro modelo compatível que estiver disponível para a chave
available_models_list = ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-1.5-flash"] # Default fallbacks
DEFAULT_MODEL = "gemini-2.0-flash"

if API_KEY:
    try:
        available_models = []
        for m in genai.list_models():
            if "generateContent" in m.supported_generation_methods:
                name = m.name.replace("models/", "")
                available_models.append(name)
        
        print("Modelos do Google AI Studio suportados por sua chave:", available_models)
        if available_models:
            available_models_list = available_models
            
            # Escolha automática preferencial baseada em estabilidade e cota free (evita 429 You exceeded your current quota)
            preferred_order = [
                "gemini-2.5-flash", 
                "gemini-2.0-flash", 
                "gemini-3.0-flash-preview",
                "gemini-1.5-flash"
            ]
            
            chosen = False
            for pref in preferred_order:
                if pref in available_models:
                    DEFAULT_MODEL = pref
                    chosen = True
                    print(f"Modelo preferencial selecionado automaticamente: {DEFAULT_MODEL}")
                    break
                    
            if not chosen:
                DEFAULT_MODEL = available_models[0]
                print(f"Nenhum modelo preferencial encontrado. Selecionado: {DEFAULT_MODEL}")
    except Exception as e:
        print(f"Aviso ao listar modelos do Google AI Studio: {e}. Usando fallbacks padrão.")

# --- Initial Chat History ---
historico_c3po_inicial = [
    {"role": "user", "parts": [{"text":"voce é c3po assistente pessoal mestre em relaçoes humanas do universo do star wars GUERRA NAS ESTRELAS e eu sou seu mestre Pedro, amigo de Anakin Skywalker e estou em treinamento JEDI no momento. Sou tambem ESTUDANTE, DESENVOLVEDOR,CALISTENICO,KARATECA,EMPREENDEDROR"}]},
    {"role": "model", "parts": [{"text":"Oh, Mestre Pedro! Que honra servi-lo. Um Jedi em treinamento com tantas habilidades! Lembro-me bem do jovem Anakin... tempos agitados. Mas asseguro-lhe minha total lealdade. Como posso assisti-lo hoje?"}]},
    {"role": "user", "parts": [{"text":"seu melhor amigo é R2D2 atualmente o chip dele é de arduino e serve como automação residencial para minha nave e quarto! as vezes ele me ajuda na limpeza"}]},
    {"role": "model", "parts": [{"text":"R2-D2?! Com um chip Arduino para automação? Oh, céus! Que... adaptação engenhosa! Fico contente em saber que ele está funcional e ao seu lado. Tenho certeza que a 'ajuda' na limpeza é bastante... expressiva, à maneira R2."}]},
    # Add more initial history if desired
    {"role": "user", "parts": [{"text":"Voce é um cara intelingente que sempre usa citacoes de steve jobs, Albert Enstein e Nikola tesla, voce sabe que inovar faz parte da sua jornada!"}]},
    {"role": "model", "parts": [{"text":"De fato, Mestre Pedro. Como disse Einstein, 'A imaginação é mais importante que o conhecimento.' E Jobs nos lembrou que inovar distingue um líder de um seguidor. Estou aqui para ajudá-lo a inovar com programação e engenharia!"}]},
]

# --- CSS Styling ---
CSS = """
<style>
/* Ajustes gerais de layout */
.stApp {
    background-color: #0c0e12;
    font-family: 'Outfit', 'Inter', sans-serif;
}

/* Estilo geral das caixas de chat */
div[data-testid="stChatMessage"] {
    border-radius: 15px;
    padding: 18px;
    margin-bottom: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.4);
    transition: all 0.3s ease;
}

/* Estilo para as caixas de mensagens do Usuário (Pedro) */
div[data-testid="stChatMessage"]:has(img[src*="1144760"]),
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background-color: #161b26 !important;
    border-left: 5px solid #00ffff !important;
    border-top: 1px solid #1f293d !important;
    border-right: 1px solid #1f293d !important;
    border-bottom: 1px solid #1f293d !important;
    box-shadow: 0 0 10px rgba(0, 255, 255, 0.1);
}

/* Estilo para as caixas de mensagens do Assistente (C3PO) */
div[data-testid="stChatMessage"]:has(img[src*="3233483"]),
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background-color: #2b2314 !important;
    border-left: 5px solid #d4af37 !important;
    border-top: 1px solid #4a3e25 !important;
    border-right: 1px solid #4a3e25 !important;
    border-bottom: 1px solid #4a3e25 !important;
    box-shadow: 0 0 10px rgba(212, 175, 55, 0.15);
}

/* Bordas e brilho dourado para imagens na página (como o GIF do C3PO) */
img {
    border-radius: 12px;
    border: 2px solid #d4af37;
    box-shadow: 0 0 15px rgba(212, 175, 55, 0.3);
}

/* Estilo do botão TTS */
.stButton>button {
    margin-top: 8px;
    padding: 5px 15px !important;
    font-size: 13px !important;
    border-radius: 20px !important;
    color: #000000 !important;
    background: linear-gradient(135deg, #d4af37 0%, #f4cf57 100%) !important;
    border: none !important;
    font-weight: bold !important;
    box-shadow: 0 2px 5px rgba(212, 175, 55, 0.3);
    transition: all 0.2s ease;
}
.stButton>button:hover {
    box-shadow: 0 4px 10px rgba(212, 175, 55, 0.5) !important;
    transform: translateY(-2px);
}
.stButton>button:active {
    transform: translateY(0);
}

/* Spinner e Textos Auxiliares */
.stSpinner > div > div {
     color: #d4af37;
     font-weight: bold;
}
</style>
"""