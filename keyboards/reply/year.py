from telebot.types import ReplyKeyboardMarkup
from datetime import datetime

from utils.create_button_reply import create_button_reply

today_year = int(str(datetime.today())[0:4])    # получаем текущий год
years_list = [str(i_year) for i_year in range(1974, today_year + 1)]    # создаем список годо с 1974 по текущий


def year_button_reply() -> ReplyKeyboardMarkup:
    """Функция создающая клавиатуру со списком годов"""
    keyboard = create_button_reply(button_list=years_list, button_int_row=3)

    return keyboard
