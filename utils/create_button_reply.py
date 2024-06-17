from typing import List

from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def create_button_reply(button_list: List, button_int_row: int = 1) -> ReplyKeyboardMarkup:
    """
    Функция генерирующая кнопки типа reply

    :param button_list: принимает список из названий кнопок
    :type: List
    :param button_int_row: количество кнопок в одной строке (максимум 3)
    :type: int
    :return: возвращает клавиатуру из кнопок
    :rtype: ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup()
    buttons_in_row = button_int_row
    buttons_added = []
    for i_button_name in button_list:
        # добавляем элементы в список, который будет будущей строкой
        buttons_added.append(KeyboardButton(text=i_button_name))

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
