#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess

# Try importing rich for premium terminal display, fallback to standard print if not installed
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.align import Align
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False

class AgentToolbelt:
    def __init__(self):
        self.workspace_root = "/home/pedrov12/Documentos/GitHub"
        self.agents_md_path = os.path.join(self.workspace_root, ".agents", "AGENTS.md")
        self.context_path = os.path.join(self.workspace_root, ".agents", "contexto_projetos.txt")

    def print_header(self, title):
        if HAS_RICH:
            console.print(Panel(Align.center(f"[bold cyan]{title}[/bold cyan]"), border_style="cyan"))
        else:
            print(f"\n=== {title} ===\n")

    def speak(self, text):
        print(f"TTS: {text}")
        
        # Fallback 1: Native Linux spd-say (extremely fast and offline)
        try:
            if subprocess.run(["which", "spd-say"], capture_output=True).returncode == 0:
                subprocess.run(["spd-say", "-l", "pt", "-t", "female1", text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
        except Exception:
            pass

        # Fallback 2: espeak
        try:
            if subprocess.run(["which", "espeak"], capture_output=True).returncode == 0:
                subprocess.run(["espeak", "-v", "pt", text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
        except Exception:
            pass

        # Fallback 3: gTTS (Google Translate TTS)
        try:
            from gtts import gTTS
            import tempfile
            
            tts = gTTS(text=text, lang='pt')
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                tts.save(f.name)
                for player in ["mpg123", "mpv", "play", "aplay"]:
                    if subprocess.run(["which", player], capture_output=True).returncode == 0:
                        subprocess.run([player, f.name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        break
            os.unlink(f.name)
        except Exception as e:
            print(f"[Aviso] Não foi possível reproduzir o áudio por voz: {e}")

    def listen_and_recognize(self):
        try:
            import speech_recognition as sr
        except ImportError:
            print("[Erro] Biblioteca 'SpeechRecognition' não encontrada. Instale com: pip install SpeechRecognition")
            self.speak("Erro. Falta a biblioteca de reconhecimento de fala.")
            return None

        recognizer = sr.Recognizer()
        try:
            mic = sr.Microphone()
        except Exception as e:
            print(f"[Erro] Não foi possível abrir o microfone: {e}")
            self.speak("Erro. Não encontrei o microfone.")
            return None

        with mic as source:
            print("Ajustando ruído ambiente (aguarde)...")
            recognizer.adjust_for_ambient_noise(source, duration=0.6)
            print("Fale agora...")
            try:
                audio = recognizer.listen(source, timeout=6, phrase_time_limit=8)
            except sr.WaitTimeoutError:
                print("Nenhuma fala detectada.")
                return None
            except Exception as e:
                print(f"Erro ao escutar: {e}")
                return None

        try:
            text = recognizer.recognize_google(audio, language='pt-BR')
            print(f"Reconhecido: {text}")
            return text
        except sr.UnknownValueError:
            print("Áudio não compreendido.")
            return None
        except sr.RequestError as e:
            print(f"Erro na API Google STT: {e}")
            return None
        except Exception as e:
            print(f"Erro desconhecido: {e}")
            return None

    def voice_menu(self):
        self.speak("Bom dia, mestre Pedro Victor. Qual programa deseja rodar?")
        spoken_text = self.listen_and_recognize()
        
        if not spoken_text:
            self.speak("Opção não compreendida. Iniciando menu visual do sistema.")
            subprocess.run(["bash", "/home/pedrov12/Documentos/GitHub/Jedi-CyberPunk/PVRV/run_system.sh", "--fallback-menu"])
            return

        text = spoken_text.lower()
        opcao = None

        # Option mapping
        if any(w in text for w in ["um", "1", "gui", "gráfico", "grafico", "lançador", "lancador", "interface"]):
            opcao = 1
        elif any(w in text for w in ["dois", "2", "cli", "terminal", "comando"]):
            opcao = 2
        elif any(w in text for w in ["três", "tres", "3", "ia", "inteligência", "inteligencia", "antigravity", "antigravidade"]):
            opcao = 3
        elif any(w in text for w in ["quatro", "4", "todos", "tudo", "produção", "producao"]):
            opcao = 4
        elif any(w in text for w in ["cinco", "5", "detector", "movimento", "movimentos", "câmera", "camera", "opencv"]):
            opcao = 5

        if opcao == 1:
            self.speak("Iniciando interface gráfica completa.")
            subprocess.Popen(["python3", "/home/pedrov12/Documentos/GitHub/Jedi-CyberPunk/PVRV/JOBS/Projetos-Github/Launcher-GUI-PLC-Projetos/app.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif opcao == 2:
            self.speak("Abrindo terminal do Centro de Comando.")
            subprocess.Popen(["gnome-terminal", "--", "bash", "-c", "export PYTHONPATH='/home/pedrov12/Documentos/GitHub/ONS-PLC-PV-CONTROLE-E-AUTOMACAO:$PYTHONPATH'; cd /home/pedrov12/Documentos/GitHub/Jedi-CyberPunk/PVRV; python3 run_CLI.py; exec bash"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif opcao == 3:
            self.speak("Iniciando inteligência artificial antigravidade.")
            subprocess.Popen(["gnome-terminal", "--", "bash", "-c", "cd /home/pedrov12/Documentos/GitHub/Jedi-CyberPunk/PVRV; export PYTHONPATH='/home/pedrov12/Documentos/GitHub/ONS-PLC-PV-CONTROLE-E-AUTOMACAO:$PYTHONPATH'; /home/pedrov12/Documentos/Antigravity-x64/antigravity run_CLI.py; exec bash"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif opcao == 4:
            self.speak("Rodando todos os serviços da Batcaverna.")
            subprocess.Popen(["gnome-terminal", "--", "bash", "-c", "bash /home/pedrov12/Documentos/GitHub/rodar_todos.sh; exec bash"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif opcao == 5:
            self.speak("Iniciando detector de movimentos OpenCV.")
            subprocess.Popen(["python3", "/home/pedrov12/Documentos/GitHub/Jedi-CyberPunk/PVRV/Meu-Segundo-Cerebro-2026/MENTE/Build Knowlodge/Programação/Python/Computer Vision/detector_de_movimentos.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            self.speak(f"Opção {spoken_text} não encontrada. Iniciando menu visual.")
            subprocess.run(["bash", "/home/pedrov12/Documentos/GitHub/Jedi-CyberPunk/PVRV/run_system.sh", "--fallback-menu"])

    def show_status(self):
        self.print_header("STATUS DA BATCAVERNA PVRV")
        projects = {
            "Pikachu-Flask-Server": 5555,
            "C3PO-Assistente-Virtual-BR": 5000,
            "astro-blog-pedrov12": 3000
        }
        
        if HAS_RICH:
            table = Table(title="Serviços & Portas")
            table.add_column("Projeto", style="cyan")
            table.add_column("Porta Padrão", style="magenta")
            table.add_column("Diretório", style="green")
            
            for proj, port in projects.items():
                path = os.path.join(self.workspace_root, proj)
                exists_str = "[green]✔ Existente[/green]" if os.path.exists(path) else "[red]✘ Não encontrado[/red]"
                table.add_row(proj, str(port), exists_str)
            console.print(table)
        else:
            for proj, port in projects.items():
                path = os.path.join(self.workspace_root, proj)
                exists = "Existe" if os.path.exists(path) else "Não encontrado"
                print(f"- {proj} (Porta: {port}) -> {exists}")

    def read_rules(self):
        self.print_header("REGRAS DO AGENTE (AGENTS.md)")
        if not os.path.exists(self.agents_md_path):
            print(f"Arquivo de regras não encontrado em: {self.agents_md_path}")
            return
            
        with open(self.agents_md_path, "r", encoding="utf-8") as f:
            content = f.read()
            if HAS_RICH:
                from rich.markdown import Markdown
                console.print(Markdown(content))
            else:
                print(content)

    def print_context(self):
        self.print_header("CONTEXTO DOS PROJETOS")
        if not os.path.exists(self.context_path):
            print(f"Arquivo de contexto não encontrado em: {self.context_path}")
            return
            
        with open(self.context_path, "r", encoding="utf-8") as f:
            print(f.read())

def main():
    parser = argparse.ArgumentParser(description="Ferramentas de Agente C3PO - Batcaverna")
    parser.add_argument("action", choices=["status", "rules", "context", "speak", "voice_menu"], help="Ação a executar")
    parser.add_argument("--message", "-m", type=str, help="Mensagem para falar (usado com a ação 'speak')")
    
    args = parser.parse_args()
    tool = AgentToolbelt()
    
    if args.action == "status":
        tool.show_status()
    elif args.action == "rules":
        tool.read_rules()
    elif args.action == "context":
        tool.print_context()
    elif args.action == "speak":
        msg = args.message or "Iniciando sistema operacional C3PO da Batcaverna"
        tool.speak(msg)
    elif args.action == "voice_menu":
        tool.voice_menu()

if __name__ == "__main__":
    main()
