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


def back_button():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
    return keyboard


def start_buttons():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Регистрация', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Меню волонтёра', color=VkKeyboardColor.NEGATIVE)
    return keyboard


def markup():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Личный кабинет', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Ближайшие мероприятия', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Обратная связь', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Я администратор', color=VkKeyboardColor.SECONDARY)
    return keyboard


def show_events():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('В Академии', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Вне Академии', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Запланированные', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
    return keyboard


def feedback():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
    return keyboard


def show_rating():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
    return keyboard


def show_account():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Редактировать', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
    return keyboard


def edit_account_buttons():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('a', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('b', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('c', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('d', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('e', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('f', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Показать профиль', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)
    return keyboard


def sign_up_internal_button(event_id):
    keyboard = VkKeyboard(one_time=False, inline=True)
    keyboard.add_callback_button(label="Записаться ✅", color=VkKeyboardColor.POSITIVE,
                                 payload={"type": "sign_up_internal_button",
                                          "event_id": event_id})
    return keyboard


def sign_up_external_button(event_id):
    keyboard = VkKeyboard(one_time=False, inline=True)
    keyboard.add_callback_button(label="Записаться ✅", color=VkKeyboardColor.POSITIVE,
                                 payload={"type": "sign_up_external_button",
                                          "event_id": event_id})
    return keyboard


def cancel_external_appointment(event_id):
    keyboard = VkKeyboard(one_time=False, inline=True)
    keyboard.add_callback_button(label="Отменить ❌", color=VkKeyboardColor.NEGATIVE,
                                 payload={"type": "external_cancellation",
                                          "event_id": event_id})
    return keyboard


def cancel_internal_appointment(event_id):
    keyboard = VkKeyboard(one_time=False, inline=True)
    keyboard.add_callback_button(label="Отменить ❌", color=VkKeyboardColor.NEGATIVE,
                                 payload={"type": "internal_cancellation",
                                          "event_id": event_id})
    return keyboard
