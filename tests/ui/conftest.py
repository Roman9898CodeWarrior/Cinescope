from venv import logger

import pytest
from pydantic import ValidationError

from common.Tools import Tools
from data.ui_tests_data.demoqa_data import DemoQaData
from models.ui_tests_models.demo_qa_data_for_student_registration_model import DataForStudentRegistrationModel
from resources.chromium_path import ChromiumPath

DEFAULT_UI_TIMEOUT = 30000


@pytest.fixture(scope="session")
def browser(playwright):
    browser = playwright.chromium.launch(executable_path=ChromiumPath.CHROMIUM_PATH, headless=False)
    yield browser
    browser.close()
    playwright.stop()


@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)
    yield context
    log_name = f"trace_{Tools.get_timestamp()}.zip"
    trace_path = Tools.files_dir('playwright_trace', log_name)
    context.tracing.stop(path=trace_path)
    context.close()


@pytest.fixture()
def page(context):
    page = context.new_page()
    yield page
    page.close()

@pytest.fixture()
def get_data_for_student_registration_form():
    try:
        student_data_for_registration_validated = DataForStudentRegistrationModel(**DemoQaData.get_valid_data_for_student_registration())
        return student_data_for_registration_validated
    except ValidationError as e:
        pytest.fail(f'Ошибка валидации: {e}')
        logger.info(f'Ошибка валидации: {e}')

'''
@pytest.fixture(autouse=True)
def page_error_handler(page):
    seen_errors = set()

    def handle_page_error(exception):
        key = f"{exception.message}\n{exception.stack}"
        if key not in seen_errors:
            seen_errors.add(key)
            print(f"\n🔥 Ошибка на фронте:\n{exception.message}\n{exception.stack}\n")
            raise Exception(f"Ошибка на фронте: {exception.message}")

    page.on("pageerror", handle_page_error)
    yield
    page.remove_listener("pageerror", handle_page_error)
'''