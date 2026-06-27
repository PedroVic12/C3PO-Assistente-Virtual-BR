import subprocess
import pyautogui
import time
import os
from typing import Optional

class LinuxCommands:
    """Classe para executar comandos específicos do Linux"""
    
    @staticmethod
    def run_command(command: str) -> Optional[str]:
        """Executa um comando no terminal"""
        try:
            result = subprocess.run(command.split(), capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            print(f"Erro ao executar comando: {e}")
            return None

    @staticmethod
    def open_run_dialog():
        """Simula Win+R no Linux (Alt+F2)"""
        pyautogui.hotkey('alt', 'f2')
        time.sleep(0.5)

    @staticmethod
    def switch_workspace_right():
        """Muda para área de trabalho à direita"""
        pyautogui.hotkey('ctrl', 'alt', 'right')
        time.sleep(0.5)

    @staticmethod
    def switch_workspace_left():
        """Muda para área de trabalho à esquerda"""
        pyautogui.hotkey('ctrl', 'alt', 'left')
        time.sleep(0.5)

    @staticmethod
    def run_exe(exe_path: str):
        """Executa um arquivo .exe usando Wine"""
        if not exe_path.endswith('.exe'):
            print("Arquivo não é um executável .exe")
            return
        
        try:
            subprocess.Popen(['wine', exe_path])
        except Exception as e:
            print(f"Erro ao executar .exe: {e}")

class AutomationControl:
    """Classe para automação de interface usando PyAutoGUI"""
    
    def __init__(self):
        # Configuração de segurança do PyAutoGUI
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5

    def open_browser(self, browser: str = 'brave'):
        """Abre um navegador específico"""
        browsers = {
            'brave': 'brave-browser',
            'firefox': 'firefox',
            'chrome': 'google-chrome'
        }
        
        browser_cmd = browsers.get(browser.lower(), 'brave-browser')
        subprocess.Popen([browser_cmd])
        time.sleep(2)  # Aguarda o navegador abrir

    def open_github_desktop(self):
        """Abre o GitHub Desktop (assumindo que está instalado via Wine)"""
        github_path = os.path.expanduser('~/.wine/drive_c/Users/Public/Desktop/GitHub Desktop.exe')
        if os.path.exists(github_path):
            LinuxCommands.run_exe(github_path)
        else:
            print("GitHub Desktop não encontrado. Verifique a instalação.")

    def type_text(self, text: str):
        """Digite texto com segurança"""
        pyautogui.write(text, interval=0.1)

    def press_enter(self):
        """Pressiona Enter"""
        pyautogui.press('enter')

    def click_position(self, x: int, y: int):
        """Clica em uma posição específica"""
        pyautogui.click(x, y)

    def move_to(self, x: int, y: int):
        """Move o mouse para uma posição"""
        pyautogui.moveTo(x, y, duration=0.5)

# Exemplo de uso
if __name__ == '__main__':
    # Inicializa as classes
    linux_cmd = LinuxCommands()
    auto = AutomationControl()

    # Exemplos de uso
    print("Testando comandos...")
    
    # Mudar área de trabalho
    linux_cmd.switch_workspace_right()
    time.sleep(1)
    linux_cmd.switch_workspace_left()
    
    # Abrir navegador
    auto.open_browser('brave')
    time.sleep(2)
    
    # Abrir GitHub Desktop
    auto.open_github_desktop()
