import allure
from playwright.sync_api import Page, expect, Locator


class PageAction:
    def __init__(self, page: Page):
        self.page = page

    # -------------------------------------------------------------------------------------------
    # Базовые методы взаимодействия с элементами на странице.
    @allure.step("Переход на страницу: {url}")
    def open_url(self, url: str):
        self.page.goto(url)

    @allure.step("Ввод текста '{text}' в поле '{locator}'")
    def enter_text_to_element(self, locator: Locator, text: str):
        locator.fill(text)

    @allure.step("Клик по элементу '{locator}'")
    def click_element(self, locator: Locator):
        locator.click()

    @allure.step("Ожидание загрузки страницы: {url}")
    def wait_redirection_to_url(self, url: str):
        self.page.wait_for_url(url)
        assert self.page.url == url, "Редирект на домашнюю старницу не произошел"

    @allure.step("Получение текста элемента: {locator}")
    def get_element_text(self, locator: Locator) -> str:
        return locator.text_content()

    @allure.step("Ожидание появления или исчезновения элемента: {locator}, state = {state}")
    def wait_for_element_to_be_visible_or_hidden(self, locator: Locator, state: str = "visible"):
        if state == 'visible':
            expect(locator).to_be_visible()
        else:
            expect(locator).to_be_hidden()

    '''
        @allure.step("Скриншот текущей страницы")
        def make_screenshot_and_attach_to_allure(self):
            screenshot_path = "screenshot.png"
            self.page.screenshot(path=screenshot_path, full_page=True)

            with open(screenshot_path, "rb") as file:
                allure.attach(file.read(), name="Screenshot", attachment_type=allure.attachment_type.PNG)
        '''

    # -------------------------------------------------------------------------------------------
    # Базовые проверки.
    @allure.step("Проверка всплывающего сообщения c текстом: {text}")
    def check_pop_up_element_with_text(self, text: str) -> bool:
        with allure.step("Проверка появления алерта с текстом: '{text}'"):
            expect(self.page.get_by_text(text)).to_be_visible()

        with allure.step("Проверка исчезновения алерта с текстом: '{text}'"):
            expect(self.page.get_by_text(text)).to_be_hidden()
