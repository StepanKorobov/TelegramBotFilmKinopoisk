from telebot.types import ReplyKeyboardMarkup

from utils.create_button_reply import create_button_reply
from utils.misc.get_type_genre_country_list import get_country_list


country_list = get_country_list()  # берём список стран


def country_button_reply() -> ReplyKeyboardMarkup:
    """Функция создающая клавиатуру со списком стран"""
    keyboard = create_button_reply(button_list=country_list, button_int_row=3)

    return keyboard
