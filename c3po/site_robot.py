from playwright.sync_api import sync_playwright
import pyautogui
import time

def automacao_crikk(texto, voz="Natasha English (Australia)", idioma="Portuguese (Brazil)"):
    with sync_playwright() as p:
        # Abrir o Chromium
        navegador = p.chromium.launch(headless=False)  # headless=False para visualizar o navegador
        pagina = navegador.new_page()
        pagina.goto("https://crikk.com/text-to-speech/")
        
        # Selecionar o idioma
        pagina.click('text=Portuguese (Brazil)')  # Ajustar o seletor ao botão correto

        # Selecionar a voz
        pagina.click(f'text={voz}')  # Ajustar o seletor ao botão correto

        # Digitar o texto
        pagina.fill('textarea', texto)

        # Clicar no botão "Generate"
        pagina.click('text=Generate')  # Ajustar o seletor ao botão correto
        time.sleep(5)  # Esperar o áudio ser gerado

        # Usar PyAutoGUI para clicar no botão de play
        pyautogui.click(x=1000, y=500)  # Ajustar coordenadas para o botão de play
        time.sleep(10)  # Esperar o áudio tocar

        # Verificar se o áudio foi reproduzido corretamente (substituir com lógica específica)
        sucesso = True  # Você pode implementar verificações mais robustas

        # Fechar o Chromium após reprodução
        navegador.close()
        return sucesso

# Exemplo de uso
texto_para_converter = "Olá, como vai você?"
resultado = automacao_crikk(texto_para_converter)

if resultado:
    print("Áudio reproduzido com sucesso!")
else:
    print("Falha na reprodução do áudio.")
