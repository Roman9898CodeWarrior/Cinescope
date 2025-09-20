import time

import allure
import pytest

from UI.pages.сinescop_authentication_page import CinescopAuthencticatePage


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Login")
@pytest.mark.ui
class TestloginPage:
   @allure.title("Тест на успешную аутентификацию.")
   def test_authenticate_by_ui(self, get_registered_user_data_from_response_request_of_registration_response, page):
      registered_user_data = get_registered_user_data_from_response_request_of_registration_response
      authentication_page = CinescopAuthencticatePage(page)

      authentication_page.open_authentication_page()
      authentication_page.login(registered_user_data['email'], registered_user_data['password'])

      authentication_page.assert_was_redirect_to_home_page()
      authentication_page.make_screenshot_and_attach_to_allure()
      authentication_page.assert_allert_was_pop_up()

      time.sleep(2)





