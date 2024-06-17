from telebot.types import ReplyKeyboardMarkup

from utils.create_button_reply import create_button_reply
from utils.misc.get_type_genre_country_list import get_genre_list


genre_list = get_genre_list()   # берём список жанров


def genre_button_reply() -> ReplyKeyboardMarkup:
    """Функция создающая клавиатуру со списком жанров"""
    keyboard = create_button_reply(button_list=genre_list, button_int_row=3)

    return keyboard
