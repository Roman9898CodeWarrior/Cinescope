import pytest

class TestMoviesAPIPositive:
    @pytest.mark.parametrize("min_price,max_price,locations,published", [
        (300, 700, ['MSK'], 'false'),
        (600, 800, ['SPB'], 'true')
    ])
    def test_get_filtered_movies(self, api_manager, min_price, max_price, locations, published):
        get_filtered_movies_response = api_manager.movies_api.get_filtered_movies(min_price, max_price, locations, published)

        for movie in get_filtered_movies_response['movies']:
            assert movie['price'] in range(min_price, max_price + 1)
            assert movie['location'] in locations
            if published == 'false':
                assert movie['published'] == False
            else:
                assert movie['published'] == True