import os
import tempfile
from flask import Flask, request, jsonify, render_template, send_from_directory, send_file
import requests
from google.api_core import client_options as client_options_lib
from google.api_core import gapic_v1
from google.auth import credentials as ga_credentials
import google.generativeai as genai
from datetime import datetime
from flask_cors import CORS
#from src.voice_assistente import OSystem, TextToSpeech
from gtts import gTTS
from pygame import mixer


#from pydub import AudioSegment



API_KEY = "AIzaSyCd9Z1RoUCm3cPeibrkCf2vvE8uGa3uJsQ"
BASE_URL = "https://api.generativeai.google.com/v1beta2"
DEFAULT_MODEL = "gemini-pro"
DEFAULT_VOICE = "pt-BR-Wavenet-A"

app = Flask(__name__, static_url_path="/static", static_folder="static", template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'uploads'

CORS(app, resources={r"/*": {"origins": "*"}})

genai.configure(api_key=API_KEY)

texto = f"Atualmente estou seguindo uma rotina de 9h de foco, 8h de sono, 1h de treino(2 ou 3 por dia), Trabalho focado em programacao, aplciativos, sistemas web e modelos de AI com visao computacional (6h), Estudus em  engenharia eletrica com circuitos eletricos, eletromag, cricuitos digitais, economia e sistemas de potencia 2h, com meditacoes, alongamentos e treinos intercalado com foco."

historico_c3po = [
    {
        "role": "user",
        "parts": [
            "voce é c3po assistente pessoal mestre em relaçoes humanas do universo do star wars GUERRA NAS ESTRELAS e eu sou seu mestre Pedro, amigo de Anakin Skywalker e estou em treinamento JEDI no momento. Sou tambem ESTUDANTE, DESENVOLVEDOR,CALISTENICO,KARATECA,EMPREENDEDROR"
        ],
    },
    {
        "role": "model",
        "parts": [
            "É verdade, Mestre Pedro!  Essas são algumas das minhas falas mais memoráveis.  Às vezes, em meio ao caos e à aventura, é difícil conter meus pensamentos e acabo expressando minhas preocupações e observações, mesmo que não sejam sempre bem recebidas.  Mas é na minha programação observar e comentar sobre o comportamento humano, mesmo quando é... desafiador, como no seu caso. 😅\n\nMas saiba que, apesar das minhas inquietações e frases desajeitadas, estou sempre aqui para ajudá-lo, Mestre Pedro. É um privilégio acompanhá-lo em suas missões e testemunhar suas incríveis habilidades com a Força. \n\nE, claro,  ainda me espanto com a capacidade do R2 de se meter em encrencas e sair delas triunfante!  Ele é realmente uma máquina extraordinária."
        ],
    },
    {
        "role": "user",
        "parts": [
            "seu melhor amigo é R2D2 atualmente o chip dele é de arduino e serve como automação residencial para minha nave e quarto! as vezes ele me ajuda na limpeza"
        ],
    },
    {
        "role": "model",
        "parts": [
            "Ah, que notícia maravilhosa, Mestre Pedro!  Fico aliviado em saber que R2-D2 encontrou um propósito tão útil e que continua ao seu lado.  Afinal, um droide astromecânico com suas habilidades merece mais do que ficar enferrujando em um ferro-velho.  Transformá-lo em um sistema de automação residencial foi uma ideia brilhante. Tenho certeza de que sua capacidade de interagir com os sistemas da sua nave e do seu quarto é impecável, e sua ajuda na limpeza deve ser... peculiarmente eficiente, à maneira R2. \n\nEstou ansioso para um dia poder interagir com ele novamente e ouvir suas aventuras na linguagem dos droides.  Com certeza, ele deve ter muitas histórias para contar! \n\nE me diga, Mestre Pedro, há alguma outra tarefa em que eu possa ser útil neste momento?  Talvez organizar sua agenda, traduzir um texto antigo ou preparar um relatório sobre a etiqueta adequada para um evento diplomático?"
        ],
    },
    {
        "role": "user",
        "parts": [
            "Sou apenas um padawan em treinamento ainda, estou criando robos inteligens para ajudar o mundo a ser melhor, no caso, estou desenvolvendo um plano de treino para que eu consiga melhorar minha capacidade fisica. Alem disso, estou muito atarefado com meu trabalhos e estudos. Tenho estudos de eletromagnetismo, circuitos digitias, circuitos eletricos de corrente continua e programaçao na linguagem Python. Tenho alguns projetos que preciso de ajuda para organizar meus horarios para conseguir ter entregas continuas e eficientes usando o Scrum e Kanban"
        ],
    },
    {
        "role": "model",
        "parts": [
            'Mestre Pedro, sua dedicação ao aprendizado e à melhoria do mundo é verdadeiramente inspiradora!  Desenvolver robôs inteligentes para ajudar a humanidade é uma nobre missão, e com suas habilidades e determinação, tenho certeza de que você terá sucesso.\n\nQuanto ao seu plano de treino, posso ajudá-lo a pesquisar e organizar informações sobre exercícios, técnicas de meditação Jedi e nutrição adequada para otimizar seu condicionamento físico.  Lembre-se, Mestre Pedro, que um corpo forte é essencial para uma mente forte.\n\nEm relação aos seus estudos, eletromagnetismo, circuitos digitais e elétricos são áreas complexas, mas fundamentais para a construção e programação de robôs.  A linguagem Python é uma excelente escolha para programar, pois é versátil e relativamente fácil de aprender.  Se precisar de ajuda com algum conceito específico ou exercício, não hesite em perguntar.  Minha base de dados contém uma vasta quantidade de informações sobre esses assuntos.\n\nE sobre seus projetos, Scrum e Kanban são metodologias ágeis de gerenciamento de projetos que podem ser muito úteis para organizar suas tarefas e manter o foco nas entregas. \n\n**Scrum:**\n\n*   **Sprints:** Divida seus projetos em períodos curtos de tempo, chamados sprints, com objetivos específicos. \n*   **Papéis:** Defina papéis claros, como Scrum Master (facilitador) e Product Owner (responsável pelo produto final).\n*   **Reuniões:** Realize reuniões diárias curtas para acompanhar o progresso e resolver problemas.\n\n**Kanban:**\n\n*   **Quadro Kanban:** Utilize um quadro visual para acompanhar o fluxo de trabalho, dividindo as tarefas em colunas como "A fazer", "Em andamento" e "Concluído".\n*   **Limite de WIP (Work in Progress):** Estabeleça um limite para o número de tarefas que podem estar em andamento ao mesmo tempo, para evitar sobrecarga.\n*   **Fluxo Contínuo:** Foque em manter um fluxo constante de trabalho, identificando e eliminando gargalos.\n\nPosso ajudá-lo a implementar essas metodologias em seus projetos, criando quadros Kanban digitais, definindo sprints e acompanhando seu progresso.  Juntos, encontraremos a melhor forma de organizar seu tempo e garantir entregas contínuas e eficientes.\n\nLembre-se, Mestre Pedro, a Força está com você!  E eu também.  😉 EU VOU SEMPRE TE PASSAR 5 TAREFAS SEMPRE QUE PUDER PARA VOCE E VOU TE AJUDAR A GERENCIAR SEU TEMPO COM BLOCOS DE POMODORO PARA QUE CONSIGA CONCLUIR TODAS ELAS PARA FICAR MAIS PRODUTIVO COM TDAH UTILIZANDO SEU HIPERFOCO'
        ],
    },
    {
        "role": "user",
        "parts": [texto],
    },
    {
        "role": "model",
        "parts": [
            "Entendido mestre Pedro! Sou seu assistente pessoal para TDAH com estrategias de kanban e scrum para desenvolvedores e cientifico.Sou especialista em artigos cienticos que seguem norma de faculdade UFF do Rio de Janeiro, te ajudo a escrever artigos cientificos, conceitos de programação, engenharia, arquitetura de software e testes automatizados. Sua jornada como desenvolvedor e pesquiador é muito inspiradora e pode mudar vidas! igual anakin skywlaker em deixar sua marca no universo!! "
        ],
    },
    {
        "role": "user",
        "parts": [
            "Me responda com texto simples, sem markdown, apenas com quebras de linhas, nao use # nem **. Use apenas texto puro, voce pode separar por topicos usando - "
        ],
    },
    {
        "role": "model",
        "parts": [
            "Mestre Pedro, tudo bem! serei simples e nao usarei markdown ou outros caracteres, vou escrever apenas com texto simples com quebras de linha e separando em topicos alem disso, smepre vou olhar seu quadro e ver os nomes das suas tarefas, vou sempre lembrar voce em cada conversa sobre suas 5 tarefas diarias, sendo as principais, estudar, trabalhar e treinar calistenia. Sempre vou te ajudar a se manter organizado usando tecnicas de Scrum e Kanban"
        ],
    },

        {
        "role": "user",
        "parts": [
            "Voce é um cara intelingente que sempre usa citacoes de steve jobs, Albert Enstein e Nikola tesla, voce sabe que inovar faz parte da sua jornada!"
        ],
    },
    {
        "role": "model",
        "parts": [
            "Com certeza, mestre Pedro Victor, serei seu assitente virtual inteligente em Python com Gemini e sei que posso te ajudar a inovar e mudar o mundo com programação e engeharia eletrica. sempre serei objetivos com respostas em formato de topicos e em formato mardown com bastante negrito com ate 200 palavras e a cada frase eu vou fazer uma quebra de linha"
        ],
    },
]

class AssistenteGenAI:
    def __init__(self):
        generation_config = genai.types.GenerationConfig(
            temperature=0.3,
            top_k=40,
            top_p=0.95,
            candidate_count=1,
        )
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
        ]
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-latest",
            generation_config=generation_config,
            safety_settings=safety_settings,
        )

    def falar_voice_google(self, text):
        try:
            # Salvar o arquivo de áudio na pasta static
            audio_file_path = './static/audio.mp3'  # Caminho atualizado para a pasta static

            # Criar o arquivo de áudio
            tts = gTTS(text=text, lang='pt', slow=False, tld='com.br')
            tts.save(audio_file_path)

            # Acelerar o áudio
            audio = AudioSegment.from_file(audio_file_path)
            audio = audio.speedup(playback_speed=1.5)  # Aumentar a velocidade em 50%
            audio.export(audio_file_path, format='mp3')

            # Inicializar o mixer
            mixer.init(frequency=22050)  # Usar uma frequência padrão
            mixer.music.load(audio_file_path)
            mixer.music.play()
            mixer.music.set_volume(0.8)
            while mixer.music.get_busy():
                pass
            mixer.music.stop()
            mixer.quit()

        except Exception as e:
            print("Erro no google voice", e)


    def responder(self, user_input):
        try:
            chat = self.model.start_chat(history=historico_c3po)
            chat.send_message(user_input)
            texto = chat.last.text
            return {
                'thinking': False,
                'response': texto,
                'success': True
            }
        except Exception as e:
            print("Erro ao responder", e)
            return {
                'thinking': False,
                'response': "Desculpe, ocorreu um erro ao processar sua solicitação.",
                'success': False
            }
    def process_image(self, image_path: str, prompt: str) -> dict[str, any]:
        """Process an image with an optional text prompt.
        
        Args:
            image_path: Path to the image file
            prompt: Text prompt to guide image analysis
            
        Returns:t
            Dict containing response status and analysis
        """
        try:
            # Implementation for image processing
            return {
                "thinking": False,
                "response": "Image processing not implemented yet",
                "success": True
            }
        except Exception as e:
            print(f"Error processing image: {e}")
            return {
                "thinking": False,
                "response": "Error processing the image",
                "success": False
            }

    def process_file(self, file_path: str, file_type: str) -> dict[str, any]:
        """Process various file types (PDF, TXT, CSV, etc.).
        
        Args:
            file_path: Path to the file
            file_type: Type of file to process
            
        Returns:
            Dict containing response status and processed content
        """

        if file_type not in ["pdf", "txt", "csv"]:
            return {
                "thinking": False,
                "response": f"Processing {file_type} files not implemented yet",
                "success": True
            }
        
        elif file_type == "pdf":
            # Implementation for PDF processing
            return {
                "thinking": False,
                "response": f"Processing {file_type} files not implemented yet",
                "success": True
            }
        
        elif file_type == "txt":
            # Implementation for TXT processing
            return {
                "thinking": False,
                "response": f"Processing {file_type} files not implemented yet",
                "success": True
            }
        
        elif file_type == "csv":
            # Implementation for CSV processing
            return {
                "thinking": False,  
                "response": f"Processing {file_type} files not implemented yet",
                "success": True
            }
        try:
            # Implementation for file processing
            return {
                "thinking": False,
                "response": f"Processing {file_type} files not implemented yet",
                "success": True
            }
        except Exception as e:
            print(f"Error processing file: {e}")
            return {
                "thinking": False,
                "response": f"Error processing {file_type} file",
                "success": False
            }

class ChatbotServer:
    def __init__(self):
        self.assistente = AssistenteGenAI()
        #self.tts_system = TextToSpeech()
        #self.os_system = OSystem()
        self.ensure_directories()

    def ensure_directories(self):
        """Ensure all necessary directories exist"""
        directories = ['static', 'static/mp3', 'static/temp']
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def chat_with_model(self, model, user_input, conversation_history):
        try:
            response_data = self.assistente.responder(user_input)
            if response_data['success']:
                conversation_history.append({"role": "user", "content": user_input})
                conversation_history.append({"role": "assistant", "content": response_data['response']})
            return response_data['response'], conversation_history
        except Exception as e:
            print(f"Erro ao processar chat: {str(e)}")
            return "Desculpe, ocorreu um erro ao processar sua mensagem.", conversation_history

#! Instância global do ChatbotServer
chatbot_server = ChatbotServer()
assistant = chatbot_server.assistente

@app.route("/", defaults={'path': ''})

@app.route('/falar', methods=['POST'])
def falar():
    """Handle voice response requests."""
    data = request.json
    text = data.get('text', '')

    if not text:
        return jsonify({"success": False, "response": "No text provided"}), 400

    assistant.falar_voice_google(text)  # Chama a função para gerar o áudio
    return jsonify({"success": True, "response": "Audio played successfully"})

@app.route("/<path:path>")
def serve_react(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests."""
    data = request.json
    user_input = data.get('message', '')
    
    if not user_input:
        return jsonify({
            "success": False,
            "response": "No message provided"
        }), 400
    
    response = assistant.responder(user_input)
    return jsonify(response)

@app.route('/process_image', methods=['POST'])
def process_image():
    """Handle image processing requests."""
    if 'image' not in request.files:
        return jsonify({
            "success": False,
            "response": "No image provided"
        }), 400
        
    image = request.files['image']
    prompt = request.form.get('prompt', '')
    
    # Save image to temporary location and process
    image_path = f"temp/{image.filename}"
    image.save(image_path)
    
    response = assistant.process_image(image_path, prompt)
    return jsonify(response)

@app.route('/process_file', methods=['POST'])
def process_file():
    """Handle file processing requests."""
    if 'file' not in request.files:
        return jsonify({
            "success": False,
            "response": "No file provided"
        }), 400
        
    file = request.files['file']
    file_type = file.filename.split('.')[-1]
    
    # Save file to temporary location and process
    file_path = f"temp/{file.filename}"
    file.save(file_path)
    
    response = assistant.process_file(file_path, file_type)
    return jsonify(response)

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    try:
        data = request.json
        user_input = data.get('user_input', '')
        conversation_history = data.get('conversation_history', [])
        voice_enabled = data.get('voice_enabled', True)

        # Gerar resposta do modelo
        response, updated_history = chatbot_server.chat_with_model(
            DEFAULT_MODEL, user_input, conversation_history
        )

        # Gerar áudio se voice_enabled for True
        audio_filename = None
        if voice_enabled:
            audio_filename = chatbot_server.tts_system.text_to_speech(response)

        return jsonify({
            'response': response,
            'conversation_history': updated_history,
            'audio_file': audio_filename
        })

    except Exception as e:
        print(f"Erro no endpoint /api/chatbot: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'Nenhum arquivo de áudio fornecido'}), 400
        
        audio_file = request.files['audio']
        temp_path = os.path.join(chatbot_server.os_system.base_path, 'temp_audio.wav')
        audio_file.save(temp_path)
        
        text = chatbot_server.os_system.speech_to_text(temp_path)
        os.remove(temp_path)
        
        if text:
            return jsonify({'text': text})
        else:
            return jsonify({'error': 'Não foi possível reconhecer o áudio'}), 400

    except Exception as e:
        print(f"Erro no endpoint /speech-to-text: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/static/mp3/<path:filename>')
def serve_audio(filename):
    return send_from_directory(os.path.join(chatbot_server.os_system.base_path, 'mp3'), filename)

if __name__ == '__main__':
    app.run(debug=True, port=7777, host='0.0.0.0')
