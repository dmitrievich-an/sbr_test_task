import os

from dotenv import load_dotenv
from playwright.sync_api import Page

from pages.base_page import BasePage

load_dotenv()

UI_BASE_URL = os.getenv("UI_BASE_URL")


class SecurePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{UI_BASE_URL}/secure"

        self.flash_message = "#flash"
        self.logout_button = "a[href='/logout']"

    def get_flash_message(self) -> str:
        """Возвращает текст флеш-сообщения об успешном логине."""
        return self.get_element_text(self.flash_message)

    def logout(self):
        """Нажимает кнопку выхода."""
        self.click_element(self.logout_button)
