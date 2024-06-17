from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.misc.get_type_genre_country_list import get_top_movie_dick_rus


top_list = get_top_movie_dick_rus()


def top_movie_button() -> InlineKeyboardMarkup:
    """Функция создающая inline кнопку по топам фильмов"""
    keyboard = InlineKeyboardMarkup()
    buttons_in_row = 2
    buttons_added = []
    for i_key, i_value in top_list.items():
        # добавляем элементы в список, который будет будущей строкой
        buttons_added.append(InlineKeyboardButton(text=i_key, callback_data=i_value))

        # проверяем размер списка
        if len(buttons_added) == buttons_in_row:
            # если размер равен количеству кнопок в строке, то добавляем на форму используя распаковку аргументов
            keyboard.add(*buttons_added)
            buttons_added = []
    else:
        # в случае если количество кнопок не делиться на количество строк без остатка, добавляем оставшиеся кнопки
        keyboard.add(*buttons_added)
        buttons_added = []

    return keyboard
