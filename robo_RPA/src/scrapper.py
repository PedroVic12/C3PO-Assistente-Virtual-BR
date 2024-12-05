# scrapper.py
from playwright.sync_api import sync_playwright
import agentql


class WebScrapper:
    def __init__(self, url):
        self.url = url
        self.browser = None
        self.page = None

    def start_browser(self):
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=True)
            self.page = agentql.wrap(self.browser.new_page())
            self.page.goto(self.url)

    def query_data(self, query):
        response = self.page.query_data(query)
        return response

    def fill_form(self, selector, value):
        self.page.query_element(selector).fill(value)

    def click_button(self, selector):
        self.page.query_element(selector).click()

    def scrape_data(self, query):
        filters = self.page.query_elements("""
        {
            banner {
                Business
                Address
                Find_button
            }
        }
        """)

        filters.banner.Business.fill("Dentist")
        filters.banner.Address.fill("Chicago, IL")
        filters.banner.Find_button.click()

        for i in range(3):
            next_page = self.page.query_elements("{next_page_button}")
            data = self.query_data(query)
            print(f"Page {i + 1}: {data}")
            next_page.next_page_button.click()
            self.page.wait_for_timeout(2000)

    def close_browser(self):
        self.browser.close()
