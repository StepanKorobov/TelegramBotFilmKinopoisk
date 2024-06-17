from telebot.types import ReplyKeyboardMarkup

from utils.create_button_reply import create_button_reply
from utils.misc.get_type_genre_country_list import get_field_dict


premiere_dict = get_field_dict()   # берём словарь фильтров
premiere_list = [i_date for i_date in premiere_dict.keys()]     # создаём словарь из названий ключей для копки


def search_button_reply() -> ReplyKeyboardMarkup:
    """Функция создающая клавиатуру со списком фильтров"""
    keyboard = create_button_reply(button_list=premiere_list, button_int_row=2)

    return keyboard
