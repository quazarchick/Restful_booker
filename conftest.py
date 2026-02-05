import requests
import pytest
from faker import Faker
from requests import session

from constants import BASE_URL, HEADERS

faker = Faker()

@pytest.fixture(scope="session")
def auth_session():
    session = requests.Session()
    session.headers.update(HEADERS)

    response = requests.post(f'{BASE_URL}/auth', headers=HEADERS,
    json = {
        "username": "admin",
        "password": "password123"
    })
    assert response.status_code == 200, 'Ошибка авторизации'
    token = response.json().get("token")
    assert token is not None, "В ответе не оказалось токена"

    session.headers.update({"Cookie": f"token={token}"})
    return session

@pytest.fixture
def booking_data():
    return {
            "firstname": "Ryan",
            "lastname": "Gosling",
            "totalprice": 150000,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-04-05",
                "checkout": "2024-04-08"
            },
            "additionalneeds": "Piano"
        }