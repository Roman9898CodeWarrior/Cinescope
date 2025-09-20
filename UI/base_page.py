import allure
from playwright.sync_api import Page

from UI.action_page import PageAction


class BasePage(PageAction):
    def __init__(self, page: Page):
        super().__init__(page)
        self.home_url = "https://dev-cinescope.coconutqa.ru/"

        self.go_to_home_page_button = page.get_by_role("link", name="Cinescope")
        self.go_to_all_movies_page_button = page.get_by_role("link", name="Все фильмы")

    @allure.step("Переход на главную страницу, из шапки сайта")
    def go_to_home_page(self):
        self.click_element(self.go_to_home_page_button)
        self.wait_redirect_for_url(self.home_url)

    @allure.step("Переход на страницу 'Все фильмы, из шапки сайта'")
    def go_to_all_movies(self):
        self.click_element(self.go_to_all_movies_page_button)
        self.wait_redirect_for_url(f"{self.home_url}movies")