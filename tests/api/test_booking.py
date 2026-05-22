import os

import allure
import pytest
import requests

API_BASE_URL = os.getenv("API_BASE_URL")


@allure.feature("Booking API")
class TestCreateBooking:
    """Тесты для POST /booking"""

    @allure.story("Создание бронирования")
    @allure.title("Успешное создание бронирования возвращает статус 200")
    def test_create_booking_status_code(self, auth_session: requests.Session, booking_payload: dict):
        """Проверяет, что статус код ответа равен 200."""
        response = auth_session.post(
            url=f"{API_BASE_URL}/booking",
            json=booking_payload
        )
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    @allure.story("Создание бронирования")
    @allure.title("Успешное создание бронирования возвращает bookingid в виде числа")
    def test_create_booking_returns_id(self, auth_session: requests.Session, booking_payload: dict):
        """Проверяет, что в ответе есть bookingid и он является числом."""
        response = auth_session.post(
            url=f"{API_BASE_URL}/booking",
            json=booking_payload
        )
        data = response.json()
        assert "bookingid" in data, "В ответе отсутствует поле bookingid"
        assert isinstance(data["bookingid"], int), f"bookingid должен быть числом, получен {type(data['bookingid'])}"

    @allure.story("Создание бронирования")
    @allure.title("Данные в ответе совпадают с отправленными")
    def test_create_booking_response_matches_payload(self, auth_session: requests.Session, booking_payload: dict):
        """Проверяет, что данные в ответе совпадают с отправленными."""
        response = auth_session.post(
            url=f"{API_BASE_URL}/booking",
            json=booking_payload
        )
        booking = response.json()["booking"]
        assert booking["firstname"] == booking_payload["firstname"]
        assert booking["lastname"] == booking_payload["lastname"]
        assert booking["totalprice"] == booking_payload["totalprice"]
        assert booking["depositpaid"] == booking_payload["depositpaid"]
        assert booking["bookingdates"]["checkin"] == booking_payload["bookingdates"]["checkin"]
        assert booking["bookingdates"]["checkout"] == booking_payload["bookingdates"]["checkout"]
        assert booking["additionalneeds"] == booking_payload["additionalneeds"]

    @allure.story("Создание бронирования с невалидными данными")
    @allure.title("Создание бронирования с пустым телом возвращает ошибку")
    def test_create_booking_empty_body(self, auth_session: requests.Session):
        """Проверяет поведение API при отправке пустого тела."""
        response = auth_session.post(
            url=f"{API_BASE_URL}/booking",
            json={}
        )
        assert response.status_code != 200, f"API не должен принимать пустое тело, получен статус {response.status_code}"

    @allure.story("Создание бронирования с невалидными данными")
    @allure.title("Создание бронирования без обязательного поля возвращает ошибку")
    def test_create_booking_missing_required_field(self, auth_session: requests.Session, booking_payload: dict):
        """Проверяет поведение API при отсутствии обязательного поля firstname."""
        payload = booking_payload.copy()
        del payload["firstname"]
        response = auth_session.post(
            url=f"{API_BASE_URL}/booking",
            json=payload
        )
        assert response.status_code != 200, f"API не должен принимать тело без обязательного поля, получен статус {response.status_code}"

    @allure.story("Создание бронирования с невалидными данными")
    @allure.title("Создание бронирования со строкой в поле totalprice возвращает ошибку")
    @pytest.mark.xfail(reason="Баг API: сервер принимает строку вместо числа в поле totalprice и возвращает 200")
    def test_create_booking_invalid_type(self, auth_session: requests.Session, booking_payload: dict):
        """Проверяет поведение API при передаче строки вместо числа в totalprice."""
        payload = booking_payload.copy()
        payload["totalprice"] = "не число"
        response = auth_session.post(
            url=f"{API_BASE_URL}/booking",
            json=payload
        )
        assert response.status_code != 200, f"API не должен принимать строку в поле totalprice, получен статус {response.status_code}"


@allure.feature("Booking API")
class TestGetBooking:
    """Тесты для GET /booking/:id"""

    @allure.story("Получение бронирования")
    @allure.title("Успешное получение бронирования возвращает статус 200")
    def test_get_booking_status_code(self, auth_session: requests.Session, created_booking: dict):
        """Проверяет, что статус код ответа равен 200."""
        response = auth_session.get(
            url=f"{API_BASE_URL}/booking/{created_booking['id']}"
        )
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    @allure.story("Получение бронирования")
    @allure.title("Ответ содержит все обязательные поля")
    def test_get_booking_all_fields_present(self, auth_session: requests.Session, created_booking: dict):
        """Проверяет, что все поля присутствуют в ответе."""
        response = auth_session.get(
            url=f"{API_BASE_URL}/booking/{created_booking['id']}"
        )
        data = response.json()
        assert "firstname" in data
        assert "lastname" in data
        assert "totalprice" in data
        assert "depositpaid" in data
        assert "bookingdates" in data
        assert "checkin" in data["bookingdates"]
        assert "checkout" in data["bookingdates"]
        assert "additionalneeds" in data

    @allure.story("Получение бронирования")
    @allure.title("Данные полученного бронирования совпадают с созданными")
    def test_get_booking_data_matches_payload(self, auth_session: requests.Session, created_booking: dict):
        """Проверяет, что данные в ответе совпадают с теми что отправляли при создании."""
        response = auth_session.get(
            url=f"{API_BASE_URL}/booking/{created_booking['id']}"
        )
        data = response.json()
        payload = created_booking["payload"]
        assert data["firstname"] == payload["firstname"]
        assert data["lastname"] == payload["lastname"]
        assert data["totalprice"] == payload["totalprice"]
        assert data["depositpaid"] == payload["depositpaid"]
        assert data["bookingdates"]["checkin"] == payload["bookingdates"]["checkin"]
        assert data["bookingdates"]["checkout"] == payload["bookingdates"]["checkout"]
        assert data["additionalneeds"] == payload["additionalneeds"]

    @allure.story("Получение несуществующего бронирования")
    @allure.title("Получение бронирования с несуществующим ID возвращает 404")
    def test_get_booking_not_found(self, auth_session: requests.Session):
        """Проверяет, что запрос с несуществующим ID возвращает 404."""
        response = auth_session.get(
            url=f"{API_BASE_URL}/booking/999999"
        )
        assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}"


@allure.feature("Booking API")
class TestUpdateBooking:
    """Тесты для PUT /booking/:id"""

    @allure.story("Обновление бронирования")
    @allure.title("Успешное обновление бронирования возвращает статус 200")
    def test_update_booking_status_code(self, auth_session: requests.Session, created_booking: dict,
                                        booking_payload: dict):
        """Проверяет, что статус код ответа равен 200."""
        response = auth_session.put(
            url=f"{API_BASE_URL}/booking/{created_booking['id']}",
            json=booking_payload
        )
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    @allure.story("Обновление бронирования")
    @allure.title("Данные в ответе совпадают с обновлёнными")
    def test_update_booking_data_matches_payload(self, auth_session: requests.Session, created_booking: dict,
                                                 booking_payload: dict):
        """Проверяет, что данные в ответе совпадают с обновлёнными."""
        response = auth_session.put(
            url=f"{API_BASE_URL}/booking/{created_booking['id']}",
            json=booking_payload
        )
        data = response.json()
        assert data["firstname"] == booking_payload["firstname"]
        assert data["lastname"] == booking_payload["lastname"]
        assert data["totalprice"] == booking_payload["totalprice"]
        assert data["depositpaid"] == booking_payload["depositpaid"]
        assert data["bookingdates"]["checkin"] == booking_payload["bookingdates"]["checkin"]
        assert data["bookingdates"]["checkout"] == booking_payload["bookingdates"]["checkout"]
        assert data["additionalneeds"] == booking_payload["additionalneeds"]

    @allure.story("Обновление бронирования без авторизации")
    @allure.title("Обновление бронирования без токена возвращает 403")
    def test_update_booking_without_token(self, created_booking: dict, booking_payload: dict):
        """Проверяет, что запрос без токена возвращает 403."""
        session = requests.Session()
        session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        response = session.put(
            url=f"{API_BASE_URL}/booking/{created_booking['id']}",
            json=booking_payload
        )
        assert response.status_code == 403, f"Ожидался статус 403, получен {response.status_code}"

    @allure.story("Обновление бронирования с невалидными данными")
    @allure.title("Лишнее поле не появляется в ответе при обновлении")
    def test_update_booking_extra_field(self, auth_session: requests.Session, created_booking: dict,
                                        booking_payload: dict):
        """Проверяет, что лишнее поле не появляется в ответе."""
        payload = booking_payload.copy()
        payload["extra_field"] = "лишнее поле"
        response = auth_session.put(
            url=f"{API_BASE_URL}/booking/{created_booking['id']}",
            json=payload
        )
        data = response.json()
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        assert "extra_field" not in data, "Лишнее поле не должно появляться в ответе"

    @allure.story("Обновление бронирования с невалидными данными")
    @allure.title("Обновление бронирования со строкой в поле totalprice возвращает ошибку")
    @pytest.mark.xfail(reason="Баг API: сервер принимает строку вместо числа в поле totalprice и возвращает 200")
    def test_update_booking_invalid_type(self, auth_session: requests.Session, created_booking: dict,
                                         booking_payload: dict):
        """Проверяет поведение API при передаче строки вместо числа в totalprice."""
        payload = booking_payload.copy()
        payload["totalprice"] = "не число"
        response = auth_session.put(
            url=f"{API_BASE_URL}/booking/{created_booking['id']}",
            json=payload
        )
        assert response.status_code != 200, f"API не должен принимать строку в поле totalprice, получен статус {response.status_code}"


@allure.feature("Booking API")
class TestDeleteBooking:
    """Тесты для DELETE /booking/:id"""

    @allure.story("Удаление бронирования")
    @allure.title("Успешное удаление бронирования возвращает статус 201")
    def test_delete_booking_status_code(self, auth_session: requests.Session, created_booking: dict):
        """Проверяет, что удаление бронирования возвращает 201."""
        response = auth_session.delete(
            url=f"{API_BASE_URL}/booking/{created_booking['id']}"
        )
        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"
