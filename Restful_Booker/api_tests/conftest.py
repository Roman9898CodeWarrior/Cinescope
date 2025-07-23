import pytest
import requests
from faker import Faker
from data.constants import HEADERS, BASE_URL

faker = Faker()

@pytest.fixture(scope="session")
def auth_session():
    session = requests.Session()
    session.headers.update(HEADERS)

    response = requests.post(
        f"{BASE_URL}/auth",
        headers=HEADERS,
        json={"username": "admin", "password": "password123"}
    )
    assert response.status_code == 200, "Ошибка авторизации"
    token = response.json().get("token")
    assert token is not None, "В ответе не оказалось токена"

    session.headers.update({"Cookie": f"token={token}"})
    return session

@pytest.fixture(scope="session")
def session_without_auth():
    session = requests.Session()
    session.headers.update(HEADERS)

    return session

@pytest.fixture
def booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=100000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Cigars"
    }

@pytest.fixture
def booking_update_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=100000),
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2024-04-23",
            "checkout": "2024-04-28"
        },
        "additionalneeds": "Massage"
    }

@pytest.fixture
def booking_partial_update_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "additionalneeds": "Extra meals"
    }

@pytest.fixture
def create_booking_without_all_required_fields():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "bookingdates": {
            "checkin": "2024-04-23",
            "checkout": "2024-04-28"
        },
        "additionalneeds": "Massage"
    }

@pytest.fixture
def create_booking_with_values_of_wrong_type_in_fields():
    return {
        "firstname": 1234,
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=100000),
        "depositpaid": 'False',
        "bookingdates": {
            "checkin": "2024-04-23",
            "checkout": "2024-04-28"
        },
        "additionalneeds": "Massage"
    }

@pytest.fixture
def booking_update_data_with_none_values_in_fiels():
    return {
        "firstname": faker.first_name(),
        "lastname": None,
        "totalprice": faker.random_int(min=100, max=100000),
        "depositpaid": None,
        "bookingdates": {
            "checkin": "2024-04-23",
            "checkout": "2024-04-28"
        },
        "additionalneeds": "Massage"
    }