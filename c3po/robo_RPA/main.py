# main.py
from src.scrapper import WebScrapper
from src.c3po_voice_command import VoiceCommands
from src.web_browser_driver import WebDriverAutomation


"""
- **WebScrapper**: Utiliza `Playwright` para fazer scraping da página, realizar buscas e navegação automatizada.
- **VoiceCommands**: Usa `speech_recognition` e `pyttsx3` para captar comandos de voz e fornecer feedback via voz.
- **WebDriverAutomation**: Controla o navegador com `Selenium` e `PyAutoGUI`, permitindo ações como abrir URLs, digitar texto, pressionar teclas, e rolar a página.
- **main.py**: Orquestra as interações entre os módulos, aguardando comandos de voz e executando as funções solicitadas.

### Conclusão

O projeto está estruturado para permitir a automação do navegador com comandos de voz, integrando diversas bibliotecas como `Playwright`, `Selenium`, `AgentQL` e `PyAutoGUI`.
"""

def main():
    voice = VoiceCommands()
    voice.speak("Hello, how can I assist you today?")

    while True:
        command = voice.listen()

        if command:
            if "open browser" in command:
                voice.speak("Opening browser.")
                web_driver = WebDriverAutomation()
                web_driver.open_url("https://www.example.com")
            elif "scrape data" in command:
                voice.speak("Scraping data from the website.")
                scrapper = WebScrapper("https://www.yellowpages.com")
                scrapper.start_browser()
                scrapper.scrape_data("""
                {
                    Listining[] {
                        Business_Name
                        Phone_Number
                        Address
                        Rating
                    }
                }
                """)
                scrapper.close_browser()
            elif "scroll" in command:
                voice.speak("Scrolling the page.")
                web_driver.scroll_page("down")
            elif "exit" in command:
                voice.speak("Goodbye!")
                break

if __name__ == "__main__":
    main()
