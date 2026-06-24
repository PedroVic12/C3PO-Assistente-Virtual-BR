#!/usr/bin/env python3
import os
import sys
import argparse

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
        try:
            from gtts import gTTS
            import tempfile
            import subprocess
            
            # Simple play command using a common linux audio player
            tts = gTTS(text=text, lang='pt')
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
                tts.save(f.name)
                # Try playing using mpg123, play, aplay or similar
                for player in ["mpg123", "mpv", "play", "aplay"]:
                    if subprocess.run(["which", player], capture_output=True).returncode == 0:
                        subprocess.run([player, f.name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        break
            os.unlink(f.name)
        except Exception as e:
            print(f"[Aviso] Não foi possível reproduzir o áudio por voz: {e}")

    def show_status(self):
        self.print_header("STATUS DA BATCAVERNA PVRV")
        
        # Check active projects and endpoints
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
    parser.add_argument("action", choices=["status", "rules", "context", "speak"], help="Ação a executar")
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

if __name__ == "__main__":
    main()
