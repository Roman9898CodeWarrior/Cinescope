from datetime import datetime

import pytest

from db_requester.db_client import get_db_session
from models.db_tests_models.user_model import UserDBModel
from utils.data_generator import DataGenerator


@pytest.fixture(scope="module")
def db_session():
    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture(scope="module")
def db_session_with_adding_new_user_to_db():
    session = get_db_session()

    test_user = UserDBModel(
        id="test_id",
        email=DataGenerator.generate_valid_random_email(),
        full_name=DataGenerator.generate_random_name(),
        password=DataGenerator.generate_valid_random_password(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        verified=False,
        banned=False,
        roles="{USER}"
    )
    session.add(test_user)
    session.commit()

    yield session

    session.delete(test_user)
    session.commit()
    session.close()