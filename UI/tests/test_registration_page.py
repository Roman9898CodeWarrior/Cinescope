import time

import allure
import pytest

from UI.pages.сinescop_registration_page import CinescopRegisterPage


@pytest.mark.ui
@allure.tag('ui')
@allure.label("owner", "Roman")
@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Register")
class TestRegisterPage:
   @allure.title("Проведение успешной регистрации")
   def test_register_by_ui(self, fixture_data_for_user_registration, page):
        full_name = fixture_data_for_user_registration['fullName']
        email = fixture_data_for_user_registration['email']
        password = fixture_data_for_user_registration['password']
        password_repeat = fixture_data_for_user_registration['passwordRepeat']

        register_page = CinescopRegisterPage(page)

        register_page.open_registration_page()

        register_page.register(full_name, email, password, password_repeat)

        register_page.assert_was_redirect_to_login_page()

        register_page.assert_allert_was_pop_up()

        time.sleep(2)

