import allure

from constants.constants import MOVIES_URL, MOVIES_ENDPOINT
from API.custom_requester import CustomRequester

class MoviesAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session, MOVIES_URL)

    @allure.step("Получение всех фильмов по фильтру.")
    def get_filtered_movies(self, min_price, max_price, locations, published, expected_status=200, page_size=20):
        response = self.send_request(
            method="GET",
            endpoint=MOVIES_ENDPOINT,
            expected_status=expected_status,
            params={'minPrice': min_price, 'maxPrice': max_price, 'locations': locations, 'published': published, 'pageSize': page_size},
        )

        return response.json()
