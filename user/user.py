from DB.DBclass import UserDatabase
from buttons_configuration.administrator_buttons import *
from buttons_configuration.buttons_settings import *
from vk_api import VkApi
token = "vk1.a.RKO2gWR9ag17jto7h0a4L8NXnhsKjeKHOI28ngZGVVbRf_-U70aSeNjT34IdXsxXB" \
       "cOmq33sTlcFDph02zJ7y-KeRg9pWvVbvcgc55WE1XrUzxC2jNAq8ThVvgHvrW_u0" \
       "avk_g4pHk0qXa-k_oF78ukSzI6biLaSZfo-ID446uN36BiEKiCkxecTgNjQpdBPJCD2B52" \
       "sQHBOCvjuzW0kNg"

vk_session = VkApi(token=token)
vk = vk_session.get_api()


class User:
    quantity = 0

    def __init__(self):
        self.user_data = {
            "user_id": None,
        }
        self.dataBase = UserDatabase(self.user_data)

        self.handlers = {
            "Регистрация": self.dataBase.create_account,
            "Обратная связь": self.dataBase.get_feedback,
            "Ближайшие мероприятия": self.dataBase.show_events_button,
            "Запланированные": self.dataBase.show_planned_events,
            "В Академии": self.dataBase.show_internal_events,
            "Вне Академии": self.dataBase.show_external_events,
            "Я администратор": self.dataBase.set_admin,
            "Список студентов": self.dataBase.show_users,
            "Список мероприятий": self.dataBase.show_list_of_events,
            "В академии": self.dataBase.in_academy,
            "Вне академии": self.dataBase.out_academy,
            "Удалить все внешние мероприятия": self.dataBase.delete_external_events,
            "Удалить все внутренние мероприятия": self.dataBase.delete_internal_events,
            "Показать все мероприятия": self.dataBase.show_admin_events,
            "Назад в меню": self.back_admin_button,
            "Выйти из админ аккаунта": self.dataBase.remove_admin_status,
            "Личный кабинет": self.dataBase.show_user_account,
            "Показать профиль": self.dataBase.show_user_profile,
            "Редактировать": self.dataBase.allow_to_edit_account,
            "a": self.dataBase.allow_to_edit_name,
            "b": self.dataBase.allow_to_edit_age,
            "c": self.dataBase.allow_to_edit_course,
            "d": self.dataBase.allow_to_edit_faculty,
            "e": self.dataBase.allow_to_edit_department,
            "f": self.dataBase.allow_to_edit_size,
        }

    def back_admin_button(self):
        vk.messages.send(
            user_id=self.user_data.get('user_id'),
            message=f"Главное меню",
            random_id=0,
            keyboard=start_administrator_buttons().get_keyboard(),
        )
