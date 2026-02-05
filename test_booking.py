import requests
from constants import BASE_URL, HEADERS


class TestBookings:
    def test_create_booking(self, auth_session, booking_data):

        #Создание бронирования
        create_booking = auth_session.post(f'{BASE_URL}/booking', json=booking_data)
        assert create_booking.status_code == 200, 'Ошибка создания бронирования'
        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор бронирования не найден"
        assert create_booking.json()["booking"]["firstname"] == "Ryan", "Имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == 150000, "Заданная стоимость не совпадает"

        #Получение бронирования
        get_booking = auth_session.get(f'{BASE_URL}/booking/{booking_id}')
        assert get_booking.status_code == 200, "Бронирование не получено"
        assert get_booking.json()["lastname"] == "Gosling", "Фамилия не совпадает"

        #Удаление бронирования
        delete_booking = auth_session.delete(f'{BASE_URL}/booking/{booking_id}')
        assert delete_booking.status_code == 201, "Удаление не произошло"
        get_booking = auth_session.get(f'{BASE_URL}/booking/{booking_id}')
        assert get_booking.status_code == 404, "Удаления не произошло"

        #Обновление бронирования
        create_booking = auth_session.post(f'{BASE_URL}/booking', json=booking_data)
        update_data = {
            "firstname": "James",
            "lastname": "Gandolfini",
            "totalprice": 150000,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-04-05",
                "checkout": "2024-04-08"
            },
            "additionalneeds": "Piano"
        }
        booking_id = create_booking.json().get("bookingid")
        update_booking = auth_session.put(f'{BASE_URL}/booking/{booking_id}', json=update_data)
        assert update_booking.status_code == 200, "Обновление не произошло"
        get_booking = auth_session.get(f'{BASE_URL}/booking/{booking_id}')
        assert update_booking.json()["firstname"] == "James", "Имя не обновлено"
        assert update_booking.json()["lastname"] == "Gandolfini", "Фамилия не обновлена"

        #Частичное обновление бронирования

        create_booking = auth_session.post(f'{BASE_URL}/booking', json=booking_data)
        update_data = {
            "totalprice": 200000
        }
        booking_id = create_booking.json().get("bookingid")
        update_booking = auth_session.patch(f'{BASE_URL}/booking/{booking_id}', json=update_data)
        assert update_booking.status_code == 200, "Обновление не произошло"
        get_booking = auth_session.get(f'{BASE_URL}/booking/{booking_id}')
        assert update_booking.json()["totalprice"] == 200000, "Стоимость не обновлена"

    def test_create_booking_negative(self, auth_session, booking_data):
        #Создание бронирования с неверным типом данных в firstname
        bad_data = {
            "firstname": 123,
            "lastname": "Gandolfini",
            "totalprice": 150000,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-04-05",
                "checkout": "2024-04-08"
            },
            "additionalneeds": "Piano"
        }
        create_booking = auth_session.post(f'{BASE_URL}/booking', json=bad_data)
        assert create_booking.status_code == 500, 'Бронирование создано'

        #Получение бронирования с несуществующим номером
        get_booking = auth_session.post(f'{BASE_URL}/booking/12345')
        assert get_booking.status_code == 404, 'Бронирование найдено'

        #Изменение бронирования с неполными данными в теле запроса
        create_booking = auth_session.post(f'{BASE_URL}/booking', json=booking_data)
        assert create_booking.status_code == 200, "Бронирование создано"
        booking_id = create_booking.json().get("bookingid")
        incomplete_data = {
            "firstname" : "James",
            "lastname" : "Brown",
            "totalprice" : 111
        }
        update_booking = auth_session.put(f'{BASE_URL}/booking/{booking_id}', json=incomplete_data)
        assert update_booking.status_code == 400, "Бронирование обновлено"

        #Удаление несуществующего бронирования
        delete_booking = auth_session.delete(f'{BASE_URL}/booking/past')
        assert delete_booking.status_code == 405, "Бронирование удалено"

        #Частичное обновление без указания bookingid
        partial_upd_booking = auth_session.patch(f'{BASE_URL}/booking', json=booking_data)
        assert partial_upd_booking.status_code == 404, "Бронирование частично обновлено"