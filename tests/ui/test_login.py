import os

import allure
import pytest
from dotenv import load_dotenv

from helpers.data_generator import generate_user
from pages.login_page import LoginPage
from pages.secure_page import SecurePage

load_dotenv()

UI_LOGIN = os.getenv("UI_LOGIN")
UI_PASSWORD = os.getenv("UI_PASSWORD")


@allure.feature("Авторизация")
class TestLogin:

    @allure.title("Успешная авторизация с валидными кредами")
    def test_successful_login(self, page):
        """Проверяет, что успешный логин редиректит на /secure с флеш-сообщением и отображается кнопка Logout."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(UI_LOGIN, UI_PASSWORD)

        secure_page = SecurePage(page)
        assert "You logged into a secure area!" in secure_page.get_flash_message()
        assert page.locator(secure_page.logout_button).is_visible()

    @allure.title("Авторизация с невалидными данными показывает сообщение об ошибке")
    @pytest.mark.parametrize("username, password, expected_message", [
        (generate_user()["username"], UI_PASSWORD, "Your username is invalid!"),
        (UI_LOGIN, generate_user()["password"], "Your password is invalid!"),
        ("", "", "Your username is invalid!"),
    ])
    def test_login_with_invalid_credentials(self, page, username, password, expected_message):
        """Проверяет, что невалидные данные показывают соответствующее сообщение об ошибке."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(username, password)

        assert expected_message in login_page.get_flash_message()

    @allure.title("Авторизация с заведомо неверными кредами (ожидаемое падение)")
    @pytest.mark.xfail(reason="Демонстрация падения теста со скриншотом в Allure отчёте")
    def test_login_with_wrong_credentials(self, page):
        """Намеренно падающий тест для демонстрации скриншота в Allure отчёте."""
        login_page = LoginPage(page)
        login_page.open()
        login_page.login("wronguser472", "wrongpassword")

        assert "You logged into a secure area!" in login_page.get_flash_message()