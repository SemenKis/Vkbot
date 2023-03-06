import vk_api
from vk_api.longpoll import VkLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

info = "vk1.a.RKO2gWR9ag17jto7h0a4L8NXnhsKjeKHOI28ngZGVVbRf_-U70aSeNjT34IdXsxXB" \
       "cOmq33sTlcFDph02zJ7y-KeRg9pWvVbvcgc55WE1XrUzxC2jNAq8ThVvgHvrW_u0" \
       "avk_g4pHk0qXa-k_oF78ukSzI6biLaSZfo-ID446uN36BiEKiCkxecTgNjQpdBPJCD2B52" \
       "sQHBOCvjuzW0kNg"

group_id = '217493616'

vk_session = vk_api.VkApi(token=info)
long_poll = VkLongPoll(vk_session, wait=0, group_id=group_id)
vk = vk_session.get_api()


def back_admin_button():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Назад в меню', color=VkKeyboardColor.NEGATIVE)
    return keyboard


def start_administrator_buttons():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Список студентов', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Список мероприятий', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Показать обратную связь', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Выйти из админ аккаунта', color=VkKeyboardColor.SECONDARY)
    return keyboard


def events_buttons():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('В академии', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Вне академии', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Показать все мероприятия')
    keyboard.add_line()
    keyboard.add_button('Назад в меню', color=VkKeyboardColor.NEGATIVE)
    return keyboard


def feedback_buttons():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Удалить все записи', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Назад в меню', color=VkKeyboardColor.NEGATIVE)
    return keyboard


def edit_internal_events_buttons():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Удалить все внутренние мероприятия', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button('Назад в меню', color=VkKeyboardColor.POSITIVE)
    return keyboard


def edit_external_events_buttons():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Удалить все внешние мероприятия', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button('Назад в меню', color=VkKeyboardColor.POSITIVE)
    return keyboard


def show_internal_signed_users_button(event_id):
    keyboard = VkKeyboard(one_time=False, inline=True)
    keyboard.add_callback_button(label="Показать участников", color=VkKeyboardColor.POSITIVE,
                                 payload={"type": "show_internal_signed_users",
                                          "event_id": event_id})
    return keyboard


def show_external_signed_users_button(event_id):
    keyboard = VkKeyboard(one_time=False, inline=True)
    keyboard.add_callback_button(label="Показать участников", color=VkKeyboardColor.POSITIVE,
                                 payload={"type": "show_external_signed_users",
                                          "event_id": event_id})
    return keyboard
