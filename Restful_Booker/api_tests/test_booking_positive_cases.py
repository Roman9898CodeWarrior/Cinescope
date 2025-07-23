from data.constants import BASE_URL

class TestBookingsPositiveCases:
    def test_create_booking(self, auth_session, booking_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data["totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

        # Проверяем, что бронирование больше недоступно
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 404, "Бронь не удалилась"

    def test_update_booking(self, auth_session, booking_data, booking_update_data):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data[
            "firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"

        update_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=booking_update_data)
        assert update_booking.status_code == 200, "Бронь не обновилась."

        get_booking_after_update = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking_after_update.status_code == 200, "Бронь не найдена"
        assert get_booking_after_update.json()["firstname"] == booking_update_data["firstname"], "Заданная фамилия не совпадает"
        assert get_booking_after_update.json()["lastname"] == booking_update_data["lastname"], "Заданное имя не совпадает"
        assert get_booking_after_update.json()["totalprice"] == booking_update_data["totalprice"], "Заданная цена не совпадает"
        assert get_booking_after_update.json()["depositpaid"] == booking_update_data["depositpaid"], "Уплачен ли депозит не совпадает"
        assert get_booking_after_update.json()["bookingdates"]["checkin"] == booking_update_data["bookingdates"]["checkin"], "Дата заселения не совпадает"
        assert get_booking_after_update.json()["bookingdates"]["checkout"] == booking_update_data["bookingdates"]["checkout"], "Дата выселения не совпадает"
        assert get_booking_after_update.json()["additionalneeds"] == booking_update_data["additionalneeds"], "Дополнительные услуги не совпадают"

    def test_partial_update_booking(self, auth_session, booking_data, booking_partial_update_data, booking_update_data):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data[
            "firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"

        update_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=booking_partial_update_data)
        assert update_booking.status_code == 200, "Бронь не обновилась."

        get_booking_after_update = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking_after_update.status_code == 200, "Бронь не найдена"
        assert get_booking_after_update.json()["firstname"] == booking_update_data["firstname"], "Заданная фамилия не совпадает"
        assert get_booking_after_update.json()["lastname"] == booking_update_data["lastname"], "Заданное имя не совпадает"
        assert get_booking_after_update.json()["totalprice"] == booking_data["totalprice"], "Заданная цена не совпадает"
        assert get_booking_after_update.json()["depositpaid"] == booking_data["depositpaid"], "Уплачен ли депозит не совпадает"
        assert get_booking_after_update.json()["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"], "Дата заселения не совпадает"
        assert get_booking_after_update.json()["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"], "Дата выселения не совпадает"
        assert get_booking_after_update.json()["additionalneeds"] == booking_update_data["additionalneeds"], "Дополнительные услуги не совпадают"

