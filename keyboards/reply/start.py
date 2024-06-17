from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def start_button() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton("СТАРТ"))

    return keyboard
