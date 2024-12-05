import pyautogui
import subprocess
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any
import webbrowser
from selenium import webdriver
from colorama import Fore, Style, init

# Initialize colorama
init()

class CommandHandler(ABC):
    @abstractmethod
    def handle(self, *args, **kwargs):
        pass

class BrowserCommandHandler(CommandHandler):
    def handle(self, url: str = "https://google.com"):
        try:
            webbrowser.open(url)
            logging.info(f"{Fore.GREEN}Abrindo navegador: {url}{Style.RESET_ALL}")
        except Exception as e:
            logging.error(f"{Fore.RED}Erro ao abrir navegador: {e}{Style.RESET_ALL}")

class WorkspaceCommandHandler(CommandHandler):
    def handle(self, direction: str):
        try:
            if direction.lower() == "direita":
                pyautogui.hotkey('ctrl', 'alt', 'right')
            elif direction.lower() == "esquerda":
                pyautogui.hotkey('ctrl', 'alt', 'left')
            logging.info(f"{Fore.GREEN}Mudando área de trabalho: {direction}{Style.RESET_ALL}")
        except Exception as e:
            logging.error(f"{Fore.RED}Erro ao mudar área de trabalho: {e}{Style.RESET_ALL}")

class RunCommandHandler(CommandHandler):
    def handle(self, program: str):
        try:
            pyautogui.hotkey('win', 'r')
            pyautogui.write(program)
            pyautogui.press('enter')
            logging.info(f"{Fore.GREEN}Executando programa: {program}{Style.RESET_ALL}")
        except Exception as e:
            logging.error(f"{Fore.RED}Erro ao executar programa: {e}{Style.RESET_ALL}")

class SystemControlHandler(CommandHandler):
    def handle(self, action: str):
        try:
            if action == "volume up":
                pyautogui.press('volumeup')
            elif action == "volume down":
                pyautogui.press('volumedown')
            elif action == "mute":
                pyautogui.press('volumemute')
            logging.info(f"{Fore.GREEN}Controle de sistema: {action}{Style.RESET_ALL}")
        except Exception as e:
            logging.error(f"{Fore.RED}Erro no controle do sistema: {e}{Style.RESET_ALL}")

class NewsScraperHandler(CommandHandler):
    def handle(self, topic: str = "tecnologia"):
        from scrapper import WebScrapper
        try:
            scraper = WebScrapper(f"https://news.google.com/search?q={topic}")
            scraper.start_browser()
            scraper.scrape_data("{articles: {title, link}}")
            scraper.close_browser()
            logging.info(f"{Fore.GREEN}Buscando notícias sobre: {topic}{Style.RESET_ALL}")
        except Exception as e:
            logging.error(f"{Fore.RED}Erro ao buscar notícias: {e}{Style.RESET_ALL}")

class CommandFactory:
    _handlers: Dict[str, CommandHandler] = {
        "browser": BrowserCommandHandler(),
        "workspace": WorkspaceCommandHandler(),
        "run": RunCommandHandler(),
        "system": SystemControlHandler(),
        "news": NewsScraperHandler()
    }

    @classmethod
    def get_handler(cls, command_type: str) -> CommandHandler:
        return cls._handlers.get(command_type)
