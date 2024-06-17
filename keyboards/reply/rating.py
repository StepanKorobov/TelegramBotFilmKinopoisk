from telebot.types import ReplyKeyboardMarkup

from utils.create_button_reply import create_button_reply


ratings_list = [str(i_rating/10) for i_rating in range(0, 105, 5)]  # создаём список из рейтингов


def rating_button_reply() -> ReplyKeyboardMarkup:
    """Функция создающая клавиатуру с рейтингом"""
    keyboard = create_button_reply(button_list=ratings_list, button_int_row=3)

    return keyboard
