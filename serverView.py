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
from src.voice_assistente import OSystem, TextToSpeech
from c3po_gemini_api import FreelanceManager

#from dotenv import load_dotenv

#load_dotenv()

API_KEY = "AIzaSyAxDCA2uS0OGqDZkaGJ0C-TNPQcllywwhg"
BASE_URL = "https://api.generativeai.google.com/v1beta2"
DEFAULT_MODEL = "gemini-pro"
DEFAULT_VOICE = "pt-BR-Wavenet-A"

app = Flask(__name__, static_url_path="/static", static_folder="static", template_folder='templates')  # Servidor Flask
app.config['UPLOAD_FOLDER'] = 'uploads'  # Create a folder named 'uploads' in your project directory
#PATH = r"/home/pedrov/Downloads/kanban_quadro_model.xlsx"

CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

genai.configure(api_key=API_KEY)

import pandas as pd

class repository:
    def __init__(self):

        pass

    def get_dataAtual(self):

        data_atual = datetime.now()
        return data_atual

    def get_df(self, path):

        df = pd.read_excel(path)
        # display(df) # type: ignore
        # print(df)
        return df

    def connect_gemini(
        self,
    ):
        # Função que tem como função enviar arquivos com contexto certo e formato para o gemini ler

        quadro = self.get_df(PATH)
        # convertendo dataframe para dicionario
        quadro_dict = quadro.to_dict("records")
        data_atual = self.get_dataAtual()
        print("Esse é seu quadro de horarios 2024")
        # print(f" dia : {data_atual} - para quadro: {quadro} ")
        return data_atual, quadro_dict


repo = repository()
#quadro = repo.connect_gemini()

#texto = f" Atualmente estou seguindo este quadro para ser kanban : {quadro}"

texto = f"Atualmente estou seguindo uma rotina de 9h de foco, 8h de sono, 1h de treino(2 ou 3 por dia), Trabalho focado em programacao, aplciativos, sistemas web e modelos de AI com visao computacional (6h), Estudus em  engenharia eletrica com circuitos eletricos, eletromag, cricuitos digitais, economia e sistemas de potencia 2h, com meditacoes, alongamentos e treinos intercalado com foco."

historico_c3po = history = [
    {
        "role": "user",
        "parts": [
            "voce é c3po assistente pessoal mestre em relaçoes humanas do universo do star wars GUERRA NAS ESTRELAS e eu sou seu mestre Pedro, amigo de Anakin Skywalker e estou em treinamento JEDI no momento. Sou tambem ESTUDANTE, DESENVOLVEDOR,CALISTENICO,KARATECA,EMPREENDEDROR"
        ],
    },
    {
        "role": "model",
        "parts": [
            "Oh, Mestre Pedro! É uma honra servi-lo. Como posso ser útil neste dia glorioso? Espero que o treinamento Jedi esteja indo bem. Você precisa de assistência com sua nave, um protocolo específico, ou talvez apenas deseja discutir os mistérios da Força? Estou à sua disposição."
        ],
    },
    {
        "role": "user",
        "parts": [
            "Não me chame de filósofo maluco, pote de graxa barrigudo.Meu obtuso amigo, se precisassem da nossa ajuda, teriam pedido. Tem muito a aprender sobre o comportamento humano.Eu sugiro uma nova estratégia, R2: deixe o Wookie ganhar.Oh, meu Deus! Desligue-me! Máquinas fazendo máquinas. Que maldade!Olá. Eu não acredito que fomos apresentados. R2-D2? Prazer em conhecê-lo. Sou C-3PO, Relações Humano-Ciborgue.\n\nessa sao umas das suas frases favoritas que voce ja disse durante sua jornada"
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
            "Com certeza, mestre Pedro, sempre serei objetivos com respostas em com muito espacos e topicos de ate 200 palavras"
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

    def responder(
        self,
        user_input,
    ):
        try:
            chat = self.model.start_chat(history=historico_c3po)
            chat.send_message(user_input)
            texto = chat.last.text
            return texto
        except Exception as e:
            print("Erro ao responder", e)
            return "Desculpe, ocorreu um erro ao processar sua solicitação."


class ChatbotServer:
    def __init__(self):
        self.assistente = AssistenteGenAI()
        self.tts_system = TextToSpeech()
        self.os_system = OSystem()
        #self.freelance_manager = FreelanceManager()

    def list_models(self):
        return [DEFAULT_MODEL]

    def chat_with_model(self, model, user_input, conversation_history):
        conversation_history.append({"role": "user", "content": user_input})
        assistant_response = self.assistente.responder(
            user_input,
        )
        conversation_history.append(
            {"role": "assistant", "content": assistant_response}
        )
        return assistant_response, conversation_history

    def run(self):
        # Add routes for Google Sheets API
        setup_routes(app, self.freelance_manager)

        @app.route("/", methods=["GET"])
        def index():
            return render_template("index.html")

        @app.route("/home", methods=["GET"])
        def home():
            return render_template("home.html")
            
        @app.route("/chatbot", methods=["POST"])
        def chatbot():
            data = request.json
            user_input = data.get("user_input", "")
            conversation_history = data.get("conversation_history", [])

            response, updated_history = self.chat_with_model(
                DEFAULT_MODEL, user_input, conversation_history
            )

            # Generate speech using ElevenLabs
            if data.get("voice_enabled", True):
                audio_file = self.tts_system.text_to_speech(response)
                if audio_file:
                    # Get just the filename from the full path
                    audio_filename = os.path.basename(audio_file)
                else:
                    audio_filename = None
            else:
                audio_filename = None

            return jsonify({
                "response": response,
                "conversation_history": updated_history,
                "audio_file": audio_filename
            })

        @app.route('/speech-to-text', methods=['POST'])
        def speech_to_text():
            if 'audio' not in request.files:
                return jsonify({'error': 'No audio file provided'}), 400
            
            audio_file = request.files['audio']
            
            try:
                text = self.os_system.speech_to_text(audio_file)
                return jsonify({'text': text})
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @app.route('/static/<path:filename>')
        def serve_static(filename):
            return send_from_directory('static', filename)

        app.run(debug=True, port=9999, host='0.0.0.0')


def run_chatbotc3po_texto():
    server = ChatbotServer()
    texto = input("Digite o prompt: ")
    resposta = server.assistente.responder(texto)
    print("\nC3PO Responde")
    print(resposta)

def main():
    run_chatbotc3po_texto()


if __name__ == "__main__":
    server = ChatbotServer()
    server.run()
    
    #run_chatbotc3po_texto()