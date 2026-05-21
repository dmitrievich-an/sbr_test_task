import random
from datetime import date, timedelta

from faker import Faker

from constants import ADDITIONAL_NEEDS

fake = Faker()


def generate_user() -> dict:
    """Генерирует случайные данные для регистрации пользователя через UI."""
    return {
        "username": fake.user_name(),
        "password": fake.password(length=10),
    }


def generate_booking() -> dict:
    """Генерирует случайные данные для бронирования."""
    today = date.today()
    year_later = today + timedelta(days=365)

    checkin = fake.date_between(start_date=today, end_date=year_later)
    checkout = fake.date_between(
        start_date=checkin + timedelta(days=1),
        end_date=year_later,
    )

    return {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": random.randrange(200, 9901, 100),
        "depositpaid": random.choice([True, False]),
        "bookingdates": {
            "checkin": checkin.strftime("%Y-%m-%d"),
            "checkout": checkout.strftime("%Y-%m-%d"),
        },
        "additionalneeds": random.choice(ADDITIONAL_NEEDS),
    }


if __name__ == "__main__":
    print(generate_booking()["firstname"])
    print(generate_booking())
    print(generate_user()["username"])
    print(generate_user()["password"])

