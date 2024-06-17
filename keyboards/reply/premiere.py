from telebot.types import ReplyKeyboardMarkup

from utils.create_button_reply import create_button_reply
from utils.misc.get_type_genre_country_list import get_premier_date


premiere_dict = get_premier_date()   # берём словарь премьер
premiere_list = [i_date for i_date in premiere_dict.keys()]     # создаём словарь из названий ключей для копки


def premiere_button_reply() -> ReplyKeyboardMarkup:
    """Функция создающая клавиатуру со списком премьер"""
    keyboard = create_button_reply(button_list=premiere_list, button_int_row=3)

    return keyboard
