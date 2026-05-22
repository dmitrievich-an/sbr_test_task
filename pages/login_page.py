import os

from dotenv import load_dotenv
from playwright.sync_api import Page

from pages.base_page import BasePage

load_dotenv()

UI_BASE_URL = os.getenv("UI_BASE_URL")


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{UI_BASE_URL}/login"

        self.username_input = "#username"
        self.password_input = "#password"
        self.submit_button = "#submit-login"
        self.flash_message = "#flash"

    def open(self):
        """Открывает страницу логина."""
        self.open_url(self.url)

    def login(self, username: str, password: str):
        """
        Заполняет форму логина и отправляет её.

        :param username: Имя пользователя.
        :param password: Пароль пользователя.
        """
        self.fill_field(self.username_input, username)
        self.fill_field(self.password_input, password)
        self.click_element(self.submit_button)

    def get_flash_message(self) -> str:
        """Возвращает текст флеш-сообщения."""
        return self.get_element_text(self.flash_message)
