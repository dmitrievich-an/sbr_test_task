import os

import allure
import pytest
import requests
from dotenv import load_dotenv

from helpers.data_generator import generate_booking, generate_user

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
UI_BASE_URL = os.getenv("UI_BASE_URL")
API_USERNAME = os.getenv("API_USERNAME")
API_PASSWORD = os.getenv("API_PASSWORD")
UI_LOGIN = os.getenv("UI_LOGIN")
UI_PASSWORD = os.getenv("UI_PASSWORD")


@pytest.fixture(scope="session")
def auth_token() -> str:
    """Получает токен авторизации."""
    response = requests.post(
        url=f"{API_BASE_URL}/auth",
        json={"username": API_USERNAME, "password": API_PASSWORD}
    )
    return response.json()["token"]


@pytest.fixture(scope="session")
def auth_session(auth_token: str) -> requests.Session:
    """
    Создаёт сессию с токеном авторизации в заголовке.

    :param auth_token: Токен авторизации полученный из /auth эндпоинта.
    :return: Сессия с токеном в заголовке.
    """
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": f"token={auth_token}"
    })
    return session


@pytest.fixture()
def booking_payload() -> dict:
    """Возвращает случайные данные для бронирования."""
    return generate_booking()


@pytest.fixture()
def created_booking(auth_session: requests.Session, booking_payload: dict):
    """
    Создаёт бронирование и возвращает его ID и данные.
    После теста удаляет бронирование, если оно ещё существует.

    :param auth_session: Авторизованная сессия с токеном.
    :param booking_payload: Словарь с данными бронирования.
    :return: Словарь с ключами id и payload.
    """
    response = auth_session.post(
        url=f"{API_BASE_URL}/booking",
        json=booking_payload
    )
    data = response.json()
    booking_id = data["bookingid"]

    yield {
        "id": booking_id,
        "payload": booking_payload
    }

    check = auth_session.get(url=f"{API_BASE_URL}/booking/{booking_id}")
    if check.status_code != 404:
        auth_session.delete(url=f"{API_BASE_URL}/booking/{booking_id}")


@pytest.fixture()
def user_data() -> dict:
    """Возвращает случайные данные пользователя для регистрации."""
    return generate_user()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук для создания скриншота при падении UI теста.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    if call.when == "call" and (rep.failed or hasattr(rep, "wasxfail")):
        page = item.funcargs.get("page")
        if page:
            allure.attach(
                page.screenshot(full_page=True),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG
            )
