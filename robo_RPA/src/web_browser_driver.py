# webdriver.py
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyautogui
import time

class WebDriverAutomation:
    def __init__(self):
        self.driver = webdriver.Chrome(

            options=webdriver.ChromeOptions(
                add_arguments=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-setuid-sandbox',
                ]
                
            )
        )

    def open_url(self, url):
        self.driver.get(url)

    def type_text(self, text):
        pyautogui.write(text, interval=0.1)

    def press_enter(self):
        pyautogui.press('enter')

    def scroll_page(self, direction="down"):
        if direction == "down":
            pyautogui.scroll(-100)
        else:
            pyautogui.scroll(100)

    def close_browser(self):
        self.driver.quit()
