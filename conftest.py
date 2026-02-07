import requests
import pytest
from faker import Faker
from requests import session
from constants import BASE_URL, HEADERS, BOOKING_PATH
from custom_requester.custom_requester import CustomRequester

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

@pytest.fixture(scope="session")
def requester():
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

@pytest.fixture(scope="session")
def booking_id(requester, booking_data):
    response = requester.send_request(
        method = "POST",
        endpoint = BOOKING_PATH,
        data = booking_data,
        expected_status = 200
    )
    booking_id = response.json().get("bookingid")
    return booking_id