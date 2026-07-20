#!/usr/bin/env python3
import sys
import subprocess
import os

def notify_and_speak(title, message, speech_text=None):
    if speech_text is None:
        speech_text = message
        
    # 1. Envia notificação nativa para o SO (Linux / notify-send)
    try:
        subprocess.run(["notify-send", "-t", "5000", title, message], check=True)
    except Exception as e:
        print(f"Erro ao enviar notificação visual: {e}")

    # 2. Fala o texto usando o speech-dispatcher nativo (spd-say) com idioma português
    try:
        subprocess.run(["spd-say", "-l", "pt", "-t", "female1", speech_text], check=True)
    except Exception as es:
        # Fallback para espeak caso spd-say falhe
        try:
            subprocess.run(["espeak", "-v", "pt", speech_text], check=True)
        except Exception as ee:
            print(f"Erro ao falar áudio: {ee}")

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 c3po_notificador.py [erro | fim | mexe | falar] [detalhes]")
        sys.exit(1)

    opcao = sys.argv[1].lower()
    
    if opcao == "erro":
        title = "⚠️ C3PO - Alerta"
        msg = "Opa, algo deu errado. Estou rodando um processo agora e corrigindo."
        notify_and_speak(title, msg)
        
    elif opcao == "fim":
        title = "✅ C3PO - Atividade Concluída"
        msg = "Finalizei uma atividade. Quer ver ela rodando no terminal?"
        notify_and_speak(title, msg)
        
    elif opcao == "mexe":
        if len(sys.argv) < 3:
            print("Especifique o nome do projeto. Ex: python3 c3po_notificador.py mexe 'App de Calistenia'")
            sys.exit(1)
        projeto = sys.argv[2]
        title = "🛠️ C3PO - Novo Foco"
        msg = f"Iniciando modificações no projeto: {projeto}"
        speech = f"Estou mexendo no projeto {projeto} no momento."
        notify_and_speak(title, msg, speech)
        
    elif opcao == "falar":
        if len(sys.argv) < 3:
            print("Especifique a mensagem a ser falada.")
            sys.exit(1)
        mensagem = sys.argv[2]
        title = "💬 C3PO - Mensagem"
        notify_and_speak(title, mensagem)
        
    else:
        print("Opção inválida. Escolha entre: erro, fim, mexe ou falar.")

if __name__ == "__main__":
    main()
