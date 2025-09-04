import allure

class TestWithAllure:
    @allure.step("Проверка сложения чисел {a} и {b}")
    def check_addition(self, a, b, expected):
        with allure.step(f"Сложение {a} и {b}"):
            result = a + b
        with allure.step(f"Проверка результата {result} == {expected}"):
            assert result == expected

    def test_addition(self):
        self.check_addition(2, 2, 4)
        self.check_addition(3, 5, 8)