from buttons_configuration.buttons_settings import *
from user.user import User
from buttons_configuration.administrator_buttons import *
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.exceptions import ApiError
import sqlite3
import threading

conn = sqlite3.connect("data/Vkusers.db", check_same_thread=False)
cursor = conn.cursor()

# token = "vk1.a.RKO2gWR9ag17jto7h0a4L8NXnhsKjeKHOI28ngZGVVbRf_-U70aSeNjT34IdXsxXB" \
#        "cOmq33sTlcFDph02zJ7y-KeRg9pWvVbvcgc55WE1XrUzxC2jNAq8ThVvgHvrW_u0" \
#        "avk_g4pHk0qXa-k_oF78ukSzI6biLaSZfo-ID446uN36BiEKiCkxecTgNjQpdBPJCD2B52" \
#        "sQHBOCvjuzW0kNg"

token = "vk1.a.hIatFd3JMvAWu-1vh683tq4Nr3IvZ_eiFenuRoAQqYTkg5epWKnt" \
        "M6AsQPLWp0na_xIUkjzGmvfThnB_QxHBXn3i7mHYEvss8v7VYyUzjwqOfE85dvWp" \
        "7PCrgeRHAbXnVf0G_DBkcu4jwcbtpCKntf0mbuHrurVqAf5wzW77GdcAC5R6eB-Hs-ca" \
        "I0eOb7AU2xWeOHuuRGebsSDXVfNIBw"

# group_id = '217493616'

group_id = '182779876'

vk_session = vk_api.VkApi(token=token)
long_poll = VkLongPoll(vk_session, wait=0, group_id=group_id)
bot_longpoll = VkBotLongPoll(vk_session, group_id)
vk = vk_session.get_api()

commands = ["Меню волонтёра", "Назад"]

print(f"active threads - {threading.active_count()}")
try:
    for event in bot_longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            # print(event.obj.message)
            if event.from_user:
                new_user = User()
                new_user.user_data['user_id'] = event.obj.message['from_id']
                print(event.obj.message['from_id'])
                print(f"active threads - {threading.active_count()}")

                if event.obj.message['text'] in ["Start", "start", "Начать", "начать"]:
                    def start():
                        vk.messages.send(
                            user_id=event.obj.message['from_id'],
                            message="Добро пожаловать!, Тебя приветствует бот волонтёрского сектора РАНХиГС! \n"
                                    "Ты можешь зарегистрироватся в нашей системе\n",
                            random_id=0,
                            keyboard=start_buttons().get_keyboard(),
                        )


                    threading.Thread(target=start).start()

                if event.obj.message['text'] in commands:
                    cursor.execute(f"UPDATE users SET (allow_to_edit, allow_to_edit_name, allow_to_edit_age,"
                                   f"allow_to_edit_course, allow_to_edit_faculty, allow_to_edit_department,"
                                   f"allow_to_edit_size, allow_to_send_feedback) = (?,?,?,?,?,?,?,?) "
                                   f"WHERE user_id = {new_user.user_data.get('user_id')}",
                                   (False, False, False, False, False, False, False, False))
                    conn.commit()


                    def menu():
                        vk.messages.send(
                            user_id=new_user.user_data.get('user_id'),
                            message="Главное меню",
                            random_id=0,
                            keyboard=markup().get_keyboard()
                        )


                    threading.Thread(target=menu).start()

                if event.obj.message['text'] == "Регистрация":
                    def registration():
                        new_user.handlers.get('Регистрация')()


                    threading.Thread(target=registration).start()

                if event.obj.message['text'] == "Личный кабинет":
                    def account():
                        new_user.handlers.get('Личный кабинет')()


                    threading.Thread(target=account).start()

                if event.obj.message['text'] == "Редактировать":
                    def edit_account():
                        new_user.handlers.get('Редактировать')()


                    threading.Thread(target=edit_account).start()

                edit_name = cursor.execute(f"SELECT allow_to_edit, allow_to_edit_name FROM users WHERE user_id = "
                                           f"{new_user.user_data.get('user_id')}").fetchall()
                edit_age = cursor.execute(f"SELECT allow_to_edit, allow_to_edit_age FROM users WHERE user_id = "
                                          f"{new_user.user_data.get('user_id')}").fetchall()
                edit_course = cursor.execute(f"SELECT allow_to_edit, allow_to_edit_course FROM users WHERE user_id = "
                                             f"{new_user.user_data.get('user_id')}").fetchall()
                edit_faculty = cursor.execute(f"SELECT allow_to_edit, allow_to_edit_faculty FROM users WHERE user_id = "
                                              f"{new_user.user_data.get('user_id')}").fetchall()
                edit_department = cursor.execute(f"SELECT allow_to_edit, allow_to_edit_department FROM users WHERE "
                                                 f"user_id = {new_user.user_data.get('user_id')}").fetchall()
                edit_size = cursor.execute(f"SELECT allow_to_edit, allow_to_edit_size FROM users WHERE user_id = "
                                           f"{new_user.user_data.get('user_id')}").fetchall()

                if event.obj.message['text'] == "Показать профиль":
                    new_user.handlers.get('Показать профиль')()

                if edit_name == [(1, 1)]:
                    cursor.execute(f"UPDATE users SET (user_name, allow_to_edit_name) = (?,?) WHERE user_id = "
                                   f"{new_user.user_data.get('user_id')}", (event.obj.message['text'], False))
                    conn.commit()
                    vk.messages.send(
                        user_id=new_user.user_data.get('user_id'),
                        message="Имя обновлено",
                        random_id=0,
                        keyboard=edit_account_buttons().get_keyboard()
                    )

                if event.obj.message['text'] == "a":
                    new_user.handlers.get('a')()

                if edit_age == [(1, 1)]:
                    cursor.execute(f"UPDATE users SET (user_age, allow_to_edit_age) = (?,?) WHERE user_id = "
                                   f"{new_user.user_data.get('user_id')}", (event.obj.message['text'], False))
                    conn.commit()
                    vk.messages.send(
                        user_id=new_user.user_data.get('user_id'),
                        message="возраст обновлён",
                        random_id=0,
                        keyboard=edit_account_buttons().get_keyboard()
                    )

                if event.obj.message['text'] == "b":
                    new_user.handlers.get('b')()

                if edit_course == [(1, 1)]:
                    cursor.execute(f"UPDATE users SET (course, allow_to_edit_course) = (?,?) WHERE user_id = "
                                   f"{new_user.user_data.get('user_id')}", (event.obj.message['text'], False))
                    conn.commit()
                    vk.messages.send(
                        user_id=new_user.user_data.get('user_id'),
                        message="Номер курса обновлён",
                        random_id=0,
                        keyboard=edit_account_buttons().get_keyboard()
                    )

                if event.obj.message['text'] == "c":
                    new_user.handlers.get('c')()

                if edit_faculty == [(1, 1)]:
                    cursor.execute(f"UPDATE users SET (faculty, allow_to_edit_faculty) = (?,?) WHERE user_id = "
                                   f"{new_user.user_data.get('user_id')}", (event.obj.message['text'], False))
                    conn.commit()
                    vk.messages.send(
                        user_id=new_user.user_data.get('user_id'),
                        message="Направление обновлено",
                        random_id=0,
                        keyboard=edit_account_buttons().get_keyboard()
                    )

                if event.obj.message['text'] == "d":
                    new_user.handlers.get('d')()

                if edit_department == [(1, 1)]:
                    cursor.execute(f"UPDATE users SET (department, allow_to_edit_department) = (?,?) WHERE user_id = "
                                   f"{new_user.user_data.get('user_id')}", (event.obj.message['text'], False))
                    conn.commit()
                    vk.messages.send(
                        user_id=new_user.user_data.get('user_id'),
                        message="Факультет обновлён",
                        random_id=0,
                        keyboard=edit_account_buttons().get_keyboard()
                    )

                if event.obj.message['text'] == "e":
                    new_user.handlers.get('e')()

                if edit_size == [(1, 1)]:
                    cursor.execute(f"UPDATE users SET (size, allow_to_edit_size) = (?,?) WHERE user_id = "
                                   f"{new_user.user_data.get('user_id')}", (event.obj.message['text'], False))
                    conn.commit()
                    vk.messages.send(
                        user_id=new_user.user_data.get('user_id'),
                        message="Размер одежды обновлён",
                        random_id=0,
                        keyboard=edit_account_buttons().get_keyboard()
                    )

                if event.obj.message['text'] == "f":
                    new_user.handlers.get('f')()

                send_feedback = cursor.execute(f"SELECT allow_to_send_feedback FROM users WHERE user_id = "
                                               f"{new_user.user_data.get('user_id')}").fetchall()
                try:
                    if send_feedback[0][0] == 1:
                        cursor.execute(f"INSERT INTO feedback (from_user, text) VALUES (?,?) ",
                                       (new_user.user_data.get('user_id'), event.obj.message['text']))
                        cursor.execute(f"UPDATE users SET allow_to_send_feedback = (?) WHERE "
                                       f"user_id = {new_user.user_data.get('user_id')}", (False,))
                        conn.commit()
                        vk.messages.send(
                            user_id=new_user.user_data.get('user_id'),
                            message="Спасибо! Твою обратную связь обязательно прочитают)",
                            random_id=0,
                            keyboard=markup().get_keyboard()
                        )
                except IndexError:
                    print(f"Index error from feedback")

                if event.obj.message['text'] == "Обратная связь":
                    def feedback():
                        new_user.handlers.get('Обратная связь')()


                    threading.Thread(target=feedback, name="feedback").start()

                if event.obj.message['text'] == "Запланированные":
                    def planned_events():
                        try:
                            new_user.handlers.get('Запланированные')(event.obj.message['from_id'])
                        except IndexError as i_e:
                            print(i_e)


                    threading.Thread(target=planned_events).start()

                if event.obj.message['text'] == "В Академии":
                    def in_academy():
                        new_user.handlers.get('В Академии')()


                    threading.Thread(target=in_academy, name="in_academy").start()

                if event.obj.message['text'] == "Вне Академии":
                    def out_academy():
                        new_user.handlers.get('Вне Академии')()


                    threading.Thread(target=out_academy, name="out_academy").start()

                if event.obj.message['text'] == "Ближайшие мероприятия":
                    new_user.handlers.get('Ближайшие мероприятия')()

                if event.obj.message['text'] == "Я администратор":
                    def admin():
                        if str(new_user.user_data.get('user_id')) in ['321229758', '341373623', '524292535']:
                            new_user.handlers.get('Я администратор')()
                        else:
                            vk.messages.send(
                                user_id=new_user.user_data.get('user_id'),
                                message="Ты не администратор!\n",
                                random_id=0,
                                keyboard=markup().get_keyboard(),
                            )


                    threading.Thread(target=admin).start()

                if event.obj.message['text'] == "Список студентов":
                    def list_of_students():
                        new_user.handlers.get('Список студентов')()


                    threading.Thread(target=list_of_students).start()

                if event.obj.message['text'] == "Показать все мероприятия":
                    new_user.handlers.get('Показать все мероприятия')()

                if event.obj.message['text'] == "Удалить все внешние мероприятия":
                    new_user.handlers.get('Удалить все внешние мероприятия')()

                if event.obj.message['text'] == "Удалить все внутренние мероприятия":
                    new_user.handlers.get('Удалить все внутренние мероприятия')()

                internal_event = cursor.execute(f"SELECT allow_to_add_internal_event FROM users WHERE user_id"
                                                f" = {new_user.user_data.get('user_id')}").fetchall()
                external_event = cursor.execute(f"SELECT allow_to_add_external_event FROM users WHERE user_id"
                                                f" = {new_user.user_data.get('user_id')}").fetchall()

                try:
                    if int(internal_event[0][0]) == 1:
                        if event.obj.message['text'] == "Назад в меню":
                            cursor.execute(f"UPDATE users SET allow_to_add_internal_event = (?) WHERE "
                                           f"user_id = {new_user.user_data.get('user_id')}", (False,))
                            conn.commit()
                        else:
                            cursor.execute(f"INSERT INTO internal_events (event_text) VALUES (?)",
                                           (event.obj.message['text'],))
                            vk.messages.send(
                                user_id=event.obj.message['from_id'],
                                message=f"Мероприятие добавлено!",
                                random_id=0,
                                keyboard=events_buttons().get_keyboard(),
                            )
                            cursor.execute(f"UPDATE users SET allow_to_add_internal_event = (?) WHERE "
                                           f"user_id = {new_user.user_data.get('user_id')}", (False,))
                            conn.commit()

                    if int(external_event[0][0]) == 1:
                        if event.obj.message['text'] == "Назад в меню":
                            cursor.execute(f"UPDATE users SET allow_to_add_external_event = (?) WHERE "
                                           f"user_id = {new_user.user_data.get('user_id')}", (False,))
                            conn.commit()
                        else:
                            cursor.execute(f"INSERT INTO external_events (event_text) VALUES (?)",
                                           (event.obj.message['text'],))
                            vk.messages.send(
                                user_id=event.obj.message['from_id'],
                                message=f"Мероприятие добавлено!",
                                random_id=0,
                                keyboard=events_buttons().get_keyboard(),
                            )
                            cursor.execute(f"UPDATE users SET allow_to_add_external_event = (?) WHERE "
                                           f"user_id = {new_user.user_data.get('user_id')}", (False,))
                            conn.commit()

                except IndexError as ie:
                    print(ie)

                if event.obj.message['text'] == "Назад в меню":
                    new_user.handlers.get('Назад в меню')()

                if event.obj.message['text'] == "В академии":
                    new_user.handlers.get('В академии')()

                if event.obj.message['text'] == "Вне академии":
                    new_user.handlers.get('Вне академии')()

                if event.obj.message['text'] == "Список мероприятий":
                    def list_of_events():
                        new_user.handlers.get('Список мероприятий')()


                    threading.Thread(target=list_of_events).start()

                if event.obj.message['text'] == "Показать обратную связь":
                    new_user.dataBase.show_feedback()

                if event.obj.message['text'] == "Удалить все записи":
                    new_user.dataBase.delete_feedback()

                if event.obj.message['text'] == "Выйти из админ аккаунта":
                    new_user.handlers.get('Выйти из админ аккаунта')()

        if event.type == VkBotEventType.MESSAGE_EVENT:

            # sign up on Events
            print(f"active threads - {threading.active_count()}")

            new_user = User()
            new_user.user_data['user_id'] = event.obj.peer_id

            if event.object.payload.get('type') == "sign_up_external_button":
                try:
                    def sign_up_on_external_event():
                        event_id = event.object.payload.get('event_id')
                        vk.messages.edit(
                            peer_id=event.obj.peer_id,
                            message=f"{event.object.payload.get('event_id')}) "
                                    f"{new_user.dataBase.show_external_event(event.object.payload.get('event_id'))}",
                            conversation_message_id=event.obj.conversation_message_id,
                            keyboard=cancel_external_appointment(event.object.payload.get('event_id')).get_keyboard(),
                        )
                        new_user.dataBase.sign_up_external_event(event.obj.peer_id, event_id)


                    threading.Thread(target=sign_up_on_external_event, name="sign_up_on_external_event").start()
                except ApiError as ae:
                    print(ae)
                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message=f"В данный момент бот отправляет слишком много сообщений, "
                                f"поэтому он не может обработать твой запрос(\n"
                                f"Просим подождать пару минут, заранее извиняемся",
                        random_id=0
                    )

            if event.object.payload.get('type') == "external_cancellation":
                def cancel_external_event():
                    new_user.dataBase.cancel_external_event_appointment(event.obj.peer_id,
                                                                        event.object.payload.get('event_id'))
                    vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=f"{event.object.payload.get('event_id')}) "
                                f"{new_user.dataBase.show_external_event(event.object.payload.get('event_id'))}",
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=sign_up_external_button(event.object.payload.get('event_id')).get_keyboard(),
                    )


                threading.Thread(target=cancel_external_event, name="cancel_external_event").start()

            if event.object.payload.get('type') == "sign_up_internal_button":
                try:
                    def sign_up_on_internal_event():
                        event_id = event.object.payload.get('event_id')
                        vk.messages.edit(
                            peer_id=event.obj.peer_id,
                            message=f"{event.object.payload.get('event_id')}) "
                                    f"{new_user.dataBase.show_internal_event(event.object.payload.get('event_id'))}",
                            conversation_message_id=event.obj.conversation_message_id,
                            keyboard=cancel_internal_appointment(event.object.payload.get('event_id')).get_keyboard(),
                        )
                        new_user.dataBase.sign_up_internal_event(event.obj.peer_id, event_id)


                    threading.Thread(target=sign_up_on_internal_event, name="sign_up_on_internal_event").start()
                except ApiError as ae:
                    print(ae)
                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message=f"В данный момент бот отправляет слишком много сообщений, "
                                f"поэтому он не может обработать твой запрос(\n"
                                f"Просим подождать пару минут, заранее извиняемся",
                        random_id=0
                    )

            if event.object.payload.get('type') == "internal_cancellation":
                def cancel_internal_event():
                    new_user.dataBase.cancel_internal_event_appointment(event.obj.peer_id,
                                                                        event.object.payload.get('event_id'))
                    vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message=f"{event.object.payload.get('event_id')}) "
                                f"{new_user.dataBase.show_internal_event(event.object.payload.get('event_id'))}",
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=sign_up_internal_button(event.object.payload.get('event_id')).get_keyboard(),
                    )


                threading.Thread(target=cancel_internal_event, name="cancel_internal_event").start()

            # Show sign users

            if event.object.payload.get('type') == "show_internal_signed_users":
                try:
                    def show_internal_event_signed_users():
                        event_id = event.object.payload.get('event_id')
                        vk.messages.edit(
                            peer_id=event.obj.peer_id,
                            message=f"{event_id}) {new_user.dataBase.show_internal_event(event_id)} \n\n"
                                    f"Список участников ⬇️ \n\n",
                            conversation_message_id=event.obj.conversation_message_id,
                        )
                        new_user.dataBase.show_internal_singed_users(event_id)


                    threading.Thread(target=show_internal_event_signed_users).start()

                except ApiError as ae:
                    print(ae)
                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message=f"В данный момент бот отправляет слишком много сообщений, "
                                f"поэтому он не может обработать твой запрос(\n"
                                f"Просим подождать пару минут, заранее извиняемся",
                        random_id=0
                    )

            if event.object.payload.get('type') == "show_external_signed_users":
                try:
                    def show_external_event_signed_users():
                        event_id = event.object.payload.get('event_id')
                        vk.messages.edit(
                            peer_id=event.obj.peer_id,
                            message=f"{event_id}) {new_user.dataBase.show_external_event(event_id)} \n\n"
                                    f"Список участников ⬇️ \n\n",
                            conversation_message_id=event.obj.conversation_message_id,
                        )
                        new_user.dataBase.show_external_singed_users(event_id)


                    threading.Thread(target=show_external_event_signed_users).start()

                except ApiError as ae:
                    print(ae)
                    vk.messages.send(
                        peer_id=event.obj.peer_id,
                        message=f"В данный момент бот отправляет слишком много сообщений, "
                                f"поэтому он не может обработать твой запрос(\n"
                                f"Просим подождать пару минут, заранее извиняемся",
                        random_id=0
                    )


except KeyboardInterrupt as kb:
    print("Остановка")
