from telebot.types import ReplyKeyboardMarkup

from utils.create_button_reply import create_button_reply
from utils.misc.get_type_genre_country_list import get_types_list


types_list = get_types_list()   # получаем список типов


def type_button_reply() -> ReplyKeyboardMarkup:
    """Функция создающая клавиатуру со списком типов"""
    keyboard = create_button_reply(button_list=types_list, button_int_row=3)

    return keyboard
