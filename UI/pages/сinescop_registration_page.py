from playwright.sync_api import Page

from UI.base_page import BasePage


class CinescopRegisterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}register"

        self.full_name_input = page.get_by_role("textbox", name="Имя Фамилия Отчество")
        self.email_input = page.get_by_role("textbox", name="Email")
        self.password_input = page.get_by_role("textbox", name="Пароль", exact=True)
        self.repeat_password_input = page.get_by_role("textbox", name="Повторите пароль")
        self.register_button = page.get_by_role("button", name="Зарегистрироваться")
        self.sign_button = page.get_by_role("link", name="Войти")

    #-------------------------------------------------------------------------------------------
    # Локальные методы взаимодействия с элементами на странице.
    def open_registration_page(self):
        self.open_url(self.url)

        #self.make_screenshot_and_attach_to_allure()

    def register(self, full_name: str, email: str, password: str, confirm_password: str):
        self.enter_text_to_element(self.full_name_input, full_name)
        self.enter_text_to_element(self.email_input, email)
        self.enter_text_to_element(self.password_input, password)
        self.enter_text_to_element(self.repeat_password_input, confirm_password)

        #self.make_screenshot_and_attach_to_allure()

        self.click_element(self.register_button)

    # -------------------------------------------------------------------------------------------
    # Локальные проверки.
    def assert_was_redirect_to_login_page(self):
        self.wait_redirection_to_url(f"{self.home_url}login")

        #self.make_screenshot_and_attach_to_allure()

    def assert_allert_was_pop_up(self):
        self.check_pop_up_element_with_text("Подтвердите свою почту")


