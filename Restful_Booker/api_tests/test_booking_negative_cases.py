from data.constants import BASE_URL

class TestBookingsNegativeCases:
    def test_get_not_created_booking(self, auth_session):
        get_booking = auth_session.get(f"{BASE_URL}/booking/12500000")
        assert get_booking.status_code == 404, "Найдена не существующая бронь."

    def test_try_create_booking_without_all_required_fields(self, auth_session, create_booking_without_all_required_fields):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=create_booking_without_all_required_fields)
        assert create_booking.status_code == 400, "Создано бронирование, хотя в body были не все поля."

    def test_try_create_booking_with_values_of_wrong_type_in_fields(self, auth_session, create_booking_with_values_of_wrong_type_in_fields):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=create_booking_with_values_of_wrong_type_in_fields)
        assert create_booking.status_code == 400, "Создано бронирование, хотя значения у полей в body были не корректные."

    def test_try_to_update_not_created_booking(self, auth_session, booking_update_data):
        create_booking = auth_session.put(f"{BASE_URL}/booking/12500000", json=booking_update_data)
        assert create_booking.status_code == 404, "Обновлено бронирование которое не было создано."

    def test_try_to_update_booking_with_none_values_in_fields(self, auth_session, booking_data, booking_update_data_with_none_values_in_fiels):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        update_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=booking_update_data_with_none_values_in_fiels)
        assert update_booking.status_code == 400, "Бронирование обновлено, хотя у некоторых полей новое значение - none."

        get_booking_after_update_try = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking_after_update_try.status_code == 200, "Бронь не найдена"

        assert get_booking_after_update_try.json()["firstname"] == booking_data[
            "firstname"], "Заданная фамилия не совпадает"
        assert get_booking_after_update_try.json()["lastname"] == booking_data[
            "lastname"], "Заданное имя не совпадает"
        assert get_booking_after_update_try.json()["totalprice"] == booking_data[
            "totalprice"], "Заданная цена не совпадает"
        assert get_booking_after_update_try.json()["depositpaid"] == booking_data[
            "depositpaid"], "Уплачен ли депозит не совпадает"
        assert get_booking_after_update_try.json()["bookingdates"]["checkin"] == booking_data["bookingdates"][
            "checkin"], "Дата заселения не совпадает"
        assert get_booking_after_update_try.json()["bookingdates"]["checkout"] == booking_data["bookingdates"][
            "checkout"], "Дата выселения не совпадает"
        assert get_booking_after_update_try.json()["additionalneeds"] == booking_data[
            "additionalneeds"], "Дополнительные услуги не совпадают"

    def test_try_to_update_booking_without_authorization(self, session_without_auth, booking_data, booking_update_data):
        create_booking = session_without_auth.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        get_booking = session_without_auth.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        update_booking = session_without_auth.put(f"{BASE_URL}/booking/{booking_id}",
                                          json=booking_update_data)
        assert update_booking.status_code == 401, "Бронирование обновлено, хотя в запросе не был передан токен."

        get_booking_after_update_try = session_without_auth.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking_after_update_try.status_code == 200, "Бронь не найдена"
        assert get_booking_after_update_try.json()["firstname"] == booking_data[
            "firstname"], "Заданная фамилия не совпадает"
        assert get_booking_after_update_try.json()["lastname"] == booking_data[
            "lastname"], "Заданное имя не совпадает"
        assert get_booking_after_update_try.json()["totalprice"] == booking_data[
            "totalprice"], "Заданная цена не совпадает"
        assert get_booking_after_update_try.json()["depositpaid"] == booking_data[
            "depositpaid"], "Уплачен ли депозит не совпадает"
        assert get_booking_after_update_try.json()["bookingdates"]["checkin"] == booking_data["bookingdates"][
            "checkin"], "Дата заселения не совпадает"
        assert get_booking_after_update_try.json()["bookingdates"]["checkout"] == booking_data["bookingdates"][
            "checkout"], "Дата выселения не совпадает"
        assert get_booking_after_update_try.json()["additionalneeds"] == booking_data[
            "additionalneeds"], "Дополнительные услуги не совпадают"
