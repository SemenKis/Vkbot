import requests
import sqlite3
import time
from vk_api import VkApi
from buttons_configuration.buttons_settings import *
from buttons_configuration.administrator_buttons import *
import threading

# token = "vk1.a.RKO2gWR9ag17jto7h0a4L8NXnhsKjeKHOI28ngZGVVbRf_-U70aSeNjT34IdXsxXB" \
#         "cOmq33sTlcFDph02zJ7y-KeRg9pWvVbvcgc55WE1XrUzxC2jNAq8ThVvgHvrW_u0" \
#         "avk_g4pHk0qXa-k_oF78ukSzI6biLaSZfo-ID446uN36BiEKiCkxecTgNjQpdBPJCD2B52" \
#         "sQHBOCvjuzW0kNg"

token = "vk1.a.hIatFd3JMvAWu-1vh683tq4Nr3IvZ_eiFenuRoAQqYTkg5epWKnt" \
        "M6AsQPLWp0na_xIUkjzGmvfThnB_QxHBXn3i7mHYEvss8v7VYyUzjwqOfE85dvWp" \
        "7PCrgeRHAbXnVf0G_DBkcu4jwcbtpCKntf0mbuHrurVqAf5wzW77GdcAC5R6eB-Hs-ca" \
        "I0eOb7AU2xWeOHuuRGebsSDXVfNIBw"

vk_session = VkApi(token=token)
vk = vk_session.get_api()

conn = sqlite3.connect("data/Vkusers.db", check_same_thread=False)

lock = threading.Lock()


class UserDatabase:
    def __init__(self, user_data):
        self.user_data = user_data
        self.cursor = conn.cursor()

    # Create an account for users

    def create_account(self):
        print(f"[{threading.current_thread().name}] - {self.user_data.get('user_id')}")
        req = requests.get(f"https://api.vk.com/method/users.get?user_ids="
                           f"{self.user_data.get('user_id')}&fields=bdate&"
                           f"access_token={token}&v=5.131")

        req2 = requests.get(f"https://api.vk.com/method/users.get?user_ids="
                            f"{self.user_data.get('user_id')}&fields=domain&"
                            f"access_token={token}&v=5.131")

        response = req.json()['response'][0]
        domain = req2.json()['response'][0].get('domain')

        self.user_data["user_name"] = f"{response.get('first_name')} {response.get('last_name')}"
        self.user_data["user_link"] = f"https://vk.com/{domain}"

        print(self.user_data)

        self.cursor.execute(f"SELECT user_id FROM users WHERE user_id = {self.user_data.get('user_id')}")
        if self.cursor.fetchone() is None:
            self.cursor.execute(f"INSERT INTO users (user_id, user_name, allow_to_edit, user_link) "
                                f"VALUES (?,?,?,?)",
                                (self.user_data.get('user_id'), self.user_data.get('user_name'), False,
                                 self.user_data.get('user_link')))
            conn.commit()

            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message="Ты успешно зарегистрировался!\n",
                random_id=0,
                keyboard=markup().get_keyboard(),
            )
        else:
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message="Ты уже есть в системе!\n",
                random_id=0,
                keyboard=markup().get_keyboard(),
            )

    # Check if user's account exists

    def check_user_existing_status(self):
        res = self.cursor.execute(f"SELECT user_id FROM users WHERE user_id"
                                  f" = {self.user_data.get('user_id')}").fetchall()
        return res

    # Show user's rating

    def show_rating(self):
        print(f"[{threading.current_thread().name}] - {self.user_data.get('user_id')}")
        vk.messages.send(
            user_id=self.user_data.get('user_id'),
            message=f"Ваш рейтинг {0}",
            random_id=0,
            keyboard=markup().get_keyboard(),
        )

    # feedback

    def get_feedback(self):
        if not self.check_user_existing_status():
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message="Тебе необходимо зарегистрироватся!",
                random_id=0,
                keyboard=start_buttons().get_keyboard()
            )
        else:
            self.cursor.execute(f"UPDATE users SET allow_to_send_feedback = (?) WHERE "
                                f"user_id = {self.user_data.get('user_id')}", (True,))
            conn.commit()
            print(f"[{threading.current_thread().name}] - {self.user_data.get('user_id')}")
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message="Напиши пожалуйста:\n"
                        "1. В каких мероприятиях Вы участвовали?\n"
                        "2. Что Вам больше всего понравилось?\n"
                        "3. Жалобы/ пожелания\n",
                random_id=0,
                keyboard=feedback().get_keyboard()
            )

    # Show user's account

    def show_user_account(self):
        data = self.cursor.execute(f"SELECT * FROM users WHERE user_id = "
                                   f"{self.user_data.get('user_id')}").fetchall()
        if not data:
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message=f"Тебе необходимо зарегистрироваться!",
                random_id=0,
                keyboard=start_buttons().get_keyboard(),
            )
        else:
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message=f"Твой личный кабинет: \n\n"
                        f"ФИО: {data[0][2]} \n"
                        f"Возраст: {data[0][3]} \n"
                        f"Курс: {data[0][4]} \n"
                        f"Направление: {data[0][5]} \n"
                        f"Факультет: {data[0][6]} \n"
                        f"Размер одежды: {data[0][7]} \n",
                random_id=0,
                keyboard=show_account().get_keyboard()
            )

    def show_user_profile(self):
        if int(self.check_permission(self.user_data.get('user_id'))) == 1:
            data = self.cursor.execute(f"SELECT * FROM users WHERE user_id = "
                                       f"{self.user_data.get('user_id')}").fetchall()[0]
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message=f"a) ФИО: {data[2]} \n"
                        f"b) Возраст: {data[3]} \n"
                        f"c) Курс: {data[4]} \n"
                        f"d) Направление: {data[5]} \n"
                        f"e) Факультет: {data[6]} \n"
                        f"f) Размер одежды: {data[7]} \n",
                random_id=0,
                keyboard=edit_account_buttons().get_keyboard()
            )

    # Allow user to adit his account

    def allow_to_edit_account(self):
        self.cursor.execute(f"UPDATE users SET allow_to_edit = (?) WHERE user_id = {self.user_data.get('user_id')}",
                            (True,))
        conn.commit()
        data = self.cursor.execute(f"SELECT * FROM users WHERE user_id = "
                                   f"{self.user_data.get('user_id')}").fetchall()[0]
        vk.messages.send(
            user_id=self.user_data.get('user_id'),
            message=f"Что ты хочешь изменить?\n\n"
                    f"a) ФИО: {data[2]} \n"
                    f"b) Возраст: {data[3]} \n"
                    f"c) Курс: {data[4]} \n"
                    f"d) Направление: {data[5]} \n"
                    f"e) Факультет: {data[6]} \n"
                    f"f) Размер одежды: {data[7]} \n",
            random_id=0,
            keyboard=edit_account_buttons().get_keyboard()
        )
        return True

    def check_permission(self, user_id):
        req = self.cursor.execute(f"SELECT allow_to_edit FROM users WHERE user_id = {user_id}").fetchall()[0][0]
        return req

    def allow_to_edit_name(self):
        if int(self.check_permission(self.user_data.get('user_id'))) == 1:
            self.cursor.execute(f"UPDATE users SET allow_to_edit_name = (?) WHERE user_id = "
                                f"{self.user_data.get('user_id')}", (True,))
            conn.commit()
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message="Введи корректное ФИО)",
                random_id=0,
                keyboard=edit_account_buttons().get_keyboard()
            )

    def allow_to_edit_age(self):
        if int(self.check_permission(self.user_data.get('user_id'))) == 1:
            self.cursor.execute(f"UPDATE users SET allow_to_edit_age = (?) WHERE user_id = "
                                f"{self.user_data.get('user_id')}", (True,))
            conn.commit()
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message="Сколько тебе лет?",
                random_id=0,
                keyboard=edit_account_buttons().get_keyboard()
            )

    def allow_to_edit_course(self):
        if int(self.check_permission(self.user_data.get('user_id'))) == 1:
            self.cursor.execute(f"UPDATE users SET allow_to_edit_course = (?) WHERE user_id = "
                                f"{self.user_data.get('user_id')}", (True,))
            conn.commit()
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message="На каком курсе ты обучаешься?",
                random_id=0,
                keyboard=edit_account_buttons().get_keyboard()
            )

    def allow_to_edit_faculty(self):
        if int(self.check_permission(self.user_data.get('user_id'))) == 1:
            self.cursor.execute(f"UPDATE users SET allow_to_edit_faculty = (?) WHERE user_id = "
                                f"{self.user_data.get('user_id')}", (True,))
            conn.commit()
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message="На каком направлении ты учишься?",
                random_id=0,
                keyboard=edit_account_buttons().get_keyboard()
            )

    def allow_to_edit_department(self):
        if int(self.check_permission(self.user_data.get('user_id'))) == 1:
            self.cursor.execute(f"UPDATE users SET allow_to_edit_department = (?) WHERE user_id = "
                                f"{self.user_data.get('user_id')}", (True,))
            conn.commit()
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message="На каком факультете ты учишься?",
                random_id=0,
                keyboard=edit_account_buttons().get_keyboard()
            )

    def allow_to_edit_size(self):
        if int(self.check_permission(self.user_data.get('user_id'))) == 1:
            self.cursor.execute(f"UPDATE users SET allow_to_edit_size = (?) WHERE user_id = "
                                f"{self.user_data.get('user_id')}", (True,))
            conn.commit()
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message="Какой у тебя размер одежды?",
                random_id=0,
                keyboard=edit_account_buttons().get_keyboard()
            )

    # show events

    def show_events_button(self):
        data = self.cursor.execute(f"SELECT * FROM users WHERE user_id = {self.user_data.get('user_id')}").fetchall()
        if not data:
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message=f"Тебе необходимо зарегистрироваться!",
                random_id=0,
                keyboard=start_buttons().get_keyboard(),
            )
        else:
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message="✨",
                random_id=0,
                keyboard=show_events().get_keyboard(),
            )

    # show planned events

    def show_planned_events(self, user_id):
        req = self.cursor.execute(f"SELECT * FROM internal_events_users WHERE user_id = {user_id}").fetchall()
        req2 = self.cursor.execute(f"SELECT * FROM external_events_users WHERE user_id = {user_id}").fetchall()
        if not req:
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message=f"Ты не зарегистрировался ни на одно событие в Академии)",
                random_id=0,
                keyboard=show_events().get_keyboard(),
            )
        else:
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message=f"В Академии ⬇️",
                random_id=0,
                keyboard=show_events().get_keyboard(),
            )
            for event in req:
                event_text = self.cursor.execute(f"SELECT event_text FROM internal_events "
                                                 f"WHERE event_id = {event[0]}").fetchall()
                vk.messages.send(
                    user_id=self.user_data.get('user_id'),
                    message=f"{event_text[0][0]}",
                    random_id=0,
                    keyboard=show_events().get_keyboard(),
                )

        if not req2:
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message=f"Ты не зарегистрировался ни на одно событие вне Академии)",
                random_id=0,
                keyboard=show_events().get_keyboard(),
            )
        else:
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message=f"Вне Академии ⬇️",
                random_id=0,
                keyboard=show_events().get_keyboard(),
            )
            for event in req2:
                event_text = self.cursor.execute(
                    f"SELECT event_text FROM external_events WHERE event_id = {event[0]}").fetchall()
                vk.messages.send(
                    user_id=self.user_data.get('user_id'),
                    message=f"{event_text[0][0]}",
                    random_id=0,
                    keyboard=show_events().get_keyboard(),
                )

    # Callback event обработка (show event)

    def show_internal_events(self):
        request = self.cursor.execute("SELECT * FROM internal_events").fetchall()
        if not request:
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message=f"Никаких мероприятий в Академии не запланировано",
                random_id=0,
                keyboard=show_events().get_keyboard(),
            )
        else:
            for event in request:
                vk.messages.send(
                    user_id=self.user_data.get('user_id'),
                    message=f"{event[0]}) "
                            f"{event[1]} \n",
                    random_id=0,
                    keyboard=sign_up_internal_button(event[0]).get_keyboard(),
                )

    def show_external_events(self):
        request = self.cursor.execute("SELECT * FROM external_events").fetchall()
        if not request:
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message=f"Никаких мероприятий вне Академии не запланировано",
                random_id=0,
                keyboard=show_events().get_keyboard(),
            )
        else:
            for event in request:
                vk.messages.send(
                    user_id=self.user_data.get('user_id'),
                    message=f"{event[0]}) "
                            f"{event[1]} \n",
                    random_id=0,
                    keyboard=sign_up_external_button(event[0]).get_keyboard(),
                )

    # made an appointment for internal event

    def sign_up_internal_event(self, user_id, event_id):
        req = self.cursor.execute(f"SELECT * FROM internal_events_users WHERE id = {event_id} AND "
                                  f"user_id = {user_id}").fetchall()
        if not req:
            self.cursor.execute(f"INSERT INTO internal_events_users VALUES (?,?)", (event_id, user_id))
            conn.commit()
        else:
            vk.messages.send(
                peer_id=self.user_data.get('user_id'),
                message=f"Ты уже зарегистрировался на это мероприятие !",
                random_id=0
            )

    def show_internal_event(self, event_id):
        print(f"[{threading.current_thread().name}] - {self.user_data.get('user_id')}")
        req = self.cursor.execute(f"SELECT event_text FROM internal_events WHERE event_id = {event_id}").fetchall()
        return req[0][0]

    # made an appointment for external event

    def sign_up_external_event(self, user_id, event_id):
        req = self.cursor.execute(f"SELECT * FROM external_events_users WHERE id = {event_id} AND "
                                  f"user_id = {user_id}").fetchall()
        if not req:
            self.cursor.execute(f"INSERT INTO external_events_users VALUES (?,?)", (event_id, user_id))
            conn.commit()
        else:
            vk.messages.send(
                peer_id=self.user_data.get('user_id'),
                message=f"Ты уже зарегистрировался на это мероприятие !",
                random_id=0,
            )

    def show_external_event(self, event_id):
        print(f"[{threading.current_thread().name}] - {self.user_data.get('user_id')}")
        req = self.cursor.execute(f"SELECT event_text FROM external_events WHERE event_id = {event_id}").fetchall()
        return req[0][0]

    # cancel appointment

    def cancel_internal_event_appointment(self, user_id, event_id):
        print(f"[{threading.current_thread().name}] - {self.user_data.get('user_id')}")
        self.cursor.execute(f"DELETE FROM internal_events_users WHERE id = {event_id} AND user_id = {user_id}")
        conn.commit()

    def cancel_external_event_appointment(self, user_id, event_id):
        print(f"[{threading.current_thread().name}] - {self.user_data.get('user_id')}")
        self.cursor.execute(f"DELETE FROM external_events_users WHERE id = {event_id} AND user_id = {user_id}")
        conn.commit()

    # Admin account

    def set_admin(self):
        self.cursor.execute(f"UPDATE users SET is_admin = (?) WHERE "
                            f"user_id = {self.user_data.get('user_id')}", (True,))
        conn.commit()
        vk.messages.send(
            user_id=self.user_data.get('user_id'),
            message="Добро пожаловать в админ-панель!\n",
            random_id=0,
            keyboard=start_administrator_buttons().get_keyboard(),
        )

    # show all registered users (Admin account)

    def show_users(self):
        if int(self.check_admin_status()) == 1:
            request = self.cursor.execute("SELECT user_id, user_name, user_age, course, faculty,"
                                          "department, size, user_link FROM users").fetchall()
            for user in request:
                vk.messages.send(
                    user_id=self.user_data.get('user_id'),
                    message=f"ФИО: {user[1]} \n"
                            f"Возраст: {user[2]} \n"
                            f"Курс: {user[3]} \n"
                            f"Направление: {user[4]} \n"
                            f"Факультет: {user[5]} \n"
                            f"Размер одежды: {user[6]} \n"
                            f"{user[7]}",
                    random_id=0,
                )

    # Add new internal event (Admin account)

    def in_academy(self):
        if int(self.check_admin_status()) == 1:
            self.cursor.execute(f"UPDATE users SET allow_to_add_internal_event = (?) WHERE "
                                f"user_id = {self.user_data.get('user_id')}", (True,))
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message=f"Введи новое мероприятие",
                random_id=0,
                keyboard=edit_internal_events_buttons().get_keyboard(),
            )
            conn.commit()

    # Delete all internal events

    def delete_internal_events(self):
        if int(self.check_admin_status()) == 1:
            self.cursor.execute("DELETE FROM internal_events")
            self.cursor.execute("DELETE FROM internal_events_users")
            self.cursor.execute(f"UPDATE users SET allow_to_add_internal_event = (?) WHERE "
                                f"user_id = {self.user_data.get('user_id')}", (False,))
            conn.commit()
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message=f"Мероприятия удалены",
                random_id=0,
                keyboard=events_buttons().get_keyboard(),
            )

    # Add new external event (Admin account)

    def out_academy(self):
        if int(self.check_admin_status()) == 1:
            self.cursor.execute(f"UPDATE users SET allow_to_add_external_event = (?) WHERE "
                                f"user_id = {self.user_data.get('user_id')}", (True,))
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message=f"Введи новое мероприятие",
                random_id=0,
                keyboard=edit_external_events_buttons().get_keyboard(),
            )
            conn.commit()

    # Delete all external events (Admin account)

    def delete_external_events(self):
        if int(self.check_admin_status()) == 1:
            self.cursor.execute("DELETE FROM external_events")
            self.cursor.execute("DELETE FROM external_events_users")
            self.cursor.execute(f"UPDATE users SET allow_to_add_external_event = (?) WHERE "
                                f"user_id = {self.user_data.get('user_id')}", (False,))
            conn.commit()
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message=f"Мероприятия удалены",
                random_id=0,
                keyboard=events_buttons().get_keyboard(),
            )

    def show_user_link(self, user_id):
        req = self.cursor.execute(f"SELECT user_link FROM users WHERE user_id = {user_id}").fetchall()
        return req[0][0]

    # Show all events with signed users (Admin account)

    def show_admin_events(self):
        if int(self.check_admin_status()) == 1:
            req = self.cursor.execute(f"SELECT event_id, event_text FROM internal_events").fetchall()
            req2 = self.cursor.execute(f"SELECT event_id, event_text FROM external_events").fetchall()
            if not req:
                vk.messages.send(
                    user_id=self.user_data.get('user_id'),
                    message=f"Ты не добавил ни одного события в Академии)",
                    random_id=0,
                    keyboard=events_buttons().get_keyboard(),
                )
            else:
                vk.messages.send(
                    user_id=self.user_data.get('user_id'),
                    message=f"В Академии ⬇️",
                    random_id=0,
                    keyboard=events_buttons().get_keyboard(),
                )
                for event in req:
                    vk.messages.send(
                        user_id=self.user_data.get('user_id'),
                        message=f"{event[0]}) {event[1]}",
                        random_id=0,
                        keyboard=show_internal_signed_users_button(event[0]).get_keyboard(),
                    )

            if not req2:
                vk.messages.send(
                    user_id=self.user_data.get('user_id'),
                    message=f"Ты не добавил ни одного события вне Академии)",
                    random_id=0,
                    keyboard=events_buttons().get_keyboard(),
                )
            else:
                vk.messages.send(
                    user_id=self.user_data.get('user_id'),
                    message=f"Вне Академии ⬇️",
                    random_id=0,
                    keyboard=events_buttons().get_keyboard(),
                )
                for event in req2:
                    vk.messages.send(
                        user_id=self.user_data.get('user_id'),
                        message=f"{event[0]}) {event[1]}",
                        random_id=0,
                        keyboard=show_external_signed_users_button(event[0]).get_keyboard(),
                    )

    # Show users signed for internal event (Admin account)

    def show_internal_singed_users(self, event_id):
        req = self.cursor.execute(f"SELECT id, user_id FROM internal_events_users WHERE "
                                  f"id = {event_id}").fetchall()

        def show_user_data(user_id):
            data = self.cursor.execute(f'SELECT * FROM users WHERE user_id = {user_id}').fetchall()
            text = f" ФИО: {data[0][2]} \n Возраст: {data[0][3]} \n Курс: {data[0][4]} \n" \
                   f" Направление: {data[0][5]} \n Факультет: {data[0][6]} \n Размер одежды: {data[0][7]}"
            return text

        if not req:
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message=f"На это событие пока никто не зарегистрировался(",
                random_id=0,
                keyboard=events_buttons().get_keyboard(),
            )
        else:
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message=f"Пользователи, зарегистрированные на события в Академии: ",
                random_id=0,
                keyboard=events_buttons().get_keyboard(),
            )
            for user_data in req:
                vk.messages.send(
                    user_id=self.user_data.get('user_id'),
                    message=f"{user_data[0]}) - номер мероприятия\n"
                            f"{show_user_data(user_data[1])}\n"
                            f" {self.show_user_link(user_data[1])}",
                    random_id=0,
                    keyboard=events_buttons().get_keyboard(),
                )

    # Show users signed for external event (Admin account)

    def show_external_singed_users(self, event_id):
        req = self.cursor.execute(f"SELECT id, user_id FROM external_events_users WHERE "
                                  f"id = {event_id}").fetchall()

        def show_user_data(user_id):
            data = self.cursor.execute(f'SELECT * FROM users WHERE user_id = {user_id}').fetchall()[0]
            text = f" ФИО: {data[2]} \n Возраст: {data[3]} \n Курс: {data[4]} \n" \
                   f" Направление: {data[5]} \n Факультет: {data[6]} \n Размер одежды: {data[7]}"
            return text

        if not req:
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message=f"На это событие пока никто не зарегистрировался(",
                random_id=0,
                keyboard=events_buttons().get_keyboard(),
            )
        else:
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message=f"Пользователи, зарегистрированные на события вне Академии: ",
                random_id=0,
                keyboard=events_buttons().get_keyboard(),
            )
            for user_data in req:
                vk.messages.send(
                    user_id=self.user_data.get('user_id'),
                    message=f"{user_data[0]}) - номер мероприятия\n"
                            f"{show_user_data(user_data[1])}\n"
                            f" {self.show_user_link(user_data[1])}",
                    random_id=0,
                    keyboard=events_buttons().get_keyboard(),
                )

    # Show menu of events (Admin account)

    def show_list_of_events(self):
        if int(self.check_admin_status()) == 1:
            conn.commit()
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message=f"Выбери тип мероприятия",
                random_id=0,
                keyboard=events_buttons().get_keyboard(),
            )

    # Delete feedback
    def delete_feedback(self):
        if int(self.check_admin_status()) == 1:
            self.cursor.execute("DELETE FROM feedback")
            conn.commit()
            vk.messages.send(
                user_id=self.user_data.get('user_id'),
                message="Все записи удалены",
                random_id=0,
                keyboard=start_administrator_buttons().get_keyboard(),
            )

    # Show feedback (Admin account)
    def show_feedback(self):
        if int(self.check_admin_status()) == 1:
            def user_data(user_id):
                data = self.cursor.execute(f"SELECT user_name, user_link FROM users WHERE user_id = {user_id}").fetchall()
                return data[0]
            req = self.cursor.execute("SELECT * FROM feedback").fetchall()
            if not req:
                vk.messages.send(
                    user_id=self.user_data.get('user_id'),
                    message=f"Никто не написал обратную связь(",
                    random_id=0,
                    keyboard=feedback_buttons().get_keyboard(),
                )
            else:
                for item in req:
                    vk.messages.send(
                        user_id=self.user_data.get('user_id'),
                        message=f"Сообщение от {user_data(item[1])[0]} \n"
                                f"{user_data(item[1])[1]}\n\n"
                                f"{item[2]}",
                        random_id=0,
                        keyboard=feedback_buttons().get_keyboard(),
                    )

    # Check if it's admin-user or not (Admin account)

    def check_admin_status(self):
        res = self.cursor.execute(f"SELECT is_admin FROM users WHERE user_id"
                                  f" = {self.user_data.get('user_id')}").fetchall()
        return res[0][0]

    # Remove admin status (Admin account)

    def remove_admin_status(self):
        self.cursor.execute(f"UPDATE users SET is_admin = (?) WHERE "
                            f"user_id = {self.user_data.get('user_id')}", (False,))
        self.cursor.execute(f"UPDATE users SET allow_to_add_internal_event = (?) WHERE "
                            f"user_id = {self.user_data.get('user_id')}", (False,))
        self.cursor.execute(f"UPDATE users SET allow_to_add_external_event = (?) WHERE "
                            f"user_id = {self.user_data.get('user_id')}", (False,))
        conn.commit()
        vk.messages.send(
            user_id=self.user_data.get('user_id'),
            message=f"Главное меню",
            random_id=0,
            keyboard=markup().get_keyboard(),
        )
