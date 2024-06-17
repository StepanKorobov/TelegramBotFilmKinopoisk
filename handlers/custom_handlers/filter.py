from telebot.types import Message, ReplyKeyboardRemove
from loguru import logger
import datetime
import re

from loader import bot
from states.filter_settings import UserFilterSettings
from keyboards.reply import rating, year, type_movie, genre, country
from database.CRUD import update_data_filter, receive_data_user
from keyboards.reply.start import start_button
from utils.misc import get_type_genre_country_list


today_year = int(str(datetime.datetime.today())[0:4])    # текущий год
text_rating_input_checking = re.compile(r"\d{1,2}[.]\d")    # паттерн для рейтинга
text_year_input_checking = re.compile(r"\d{4}")    # паттерн для года

type_list = get_type_genre_country_list.get_types_list()    # список типов
genre_lst = get_type_genre_country_list.get_genre_list()    # список жанров
country_list = get_type_genre_country_list.get_country_list()   # список стран


@bot.message_handler(commands=["filter"])
def filter_settings(message: Message) -> None:
    """Функция для запуска событий настройки фильтра пользователя"""
    logger.info("user {user_id}, use command '/filter'".format(user_id=message.from_user.id))  # записываем информацию о действии в лог

    if receive_data_user(user_id=message.from_user.id):    # проверяем, есть ли пользователь в таблице User
        bot.set_state(user_id=message.from_user.id, state=UserFilterSettings.rating_min, chat_id=message.chat.id)
        bot.send_message(chat_id=message.chat.id, text="Выберите минимальный рейтинг:", reply_markup=rating.rating_button_reply())
    else:
        bot.send_message(chat_id=message.chat.id, text="Для того, что бы начать введите '/start' или нажмите кнопку СТАРТ", reply_markup=start_button())


@bot.message_handler(state=UserFilterSettings.rating_min)
def get_rating_min(message: Message) -> None:
    """Функция обработки ввода минимального рейтинга"""
    with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
        if not text_rating_input_checking.match(message.text):    # проверяем корректность ввода
            bot.send_message(chat_id=message.chat.id, text="Рейтинг должен быть в формате '7.5' (число точка число)")
        elif not (0 <= float(message.text) <= 10):    # проверяем диапазон ввода
            bot.send_message(chat_id=message.chat.id, text="Рейтинг должен быть в диапазоне от 0.0 до 10.0")
        else:
            bot.send_message(chat_id=message.chat.id, text="Введите максимальный рейтинг:")
            bot.set_state(user_id=message.from_user.id, state=UserFilterSettings.rating_max, chat_id=message.chat.id)
            data["rating_min"] = message.text


@bot.message_handler(state=UserFilterSettings.rating_max)
def get_rating_max(message: Message) -> None:
    """Функция для обработки ввода максимального рейтинга"""
    with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
        if not text_rating_input_checking.match(message.text):  # проверяем корректность ввода
            bot.send_message(chat_id=message.chat.id, text="Рейтинг должен быть в формате '7.5' (число точка число)")
        elif not (0 <= float(message.text) <= 10):  # проверяем диапазон ввода
            bot.send_message(chat_id=message.chat.id, text="Рейтинг должен быть в диапазоне от 0.0 до 10.0")
        elif not (float(message.text) >= float(data["rating_min"])):  # проверяем максимальный рейтинг, что бы он не был меньше минимального
            bot.send_message(chat_id=message.chat.id, text="Максимальный рейтинг должен быть больше или равен минимальному")
        else:
            bot.send_message(chat_id=message.chat.id, text="Введите минимальный год:", reply_markup=year.year_button_reply())
            bot.set_state(user_id=message.from_user.id, state=UserFilterSettings.year_min, chat_id=message.chat.id)
            data["rating_max"] = message.text


@bot.message_handler(state=UserFilterSettings.year_min)
def get_rating_max(message: Message) -> None:
    """Функция для обработки ввода минимального года"""
    with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
        if not text_year_input_checking.findall(message.text):  # проверяем корректность ввода
            bot.send_message(chat_id=message.chat.id, text="Год не должен содержать букв, и может состоять только из 4х цифр")
        elif not (1974 <= int(message.text) <= today_year):  # проверяем диапазон ввода
            bot.send_message(chat_id=message.chat.id, text="Год должен быть в диапазоне от 1974 до {}".format(today_year))
        else:
            bot.send_message(chat_id=message.chat.id, text="Введите максимальный год:")
            bot.set_state(user_id=message.from_user.id, state=UserFilterSettings.year_max, chat_id=message.chat.id)
            data["year_min"] = message.text


@bot.message_handler(state=UserFilterSettings.year_max)
def get_rating_max(message: Message) -> None:
    """Функция для обработки ввода максимального года"""
    with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
        if not text_year_input_checking.findall(message.text):  # проверяем корректность ввода
            bot.send_message(chat_id=message.chat.id, text="Год не должен содержать букв, и может состоять только из 4х цифр")
        elif not (1974 <= int(message.text) <= today_year):  # проверяем диапазон ввода
            bot.send_message(chat_id=message.chat.id, text="Год должен быть в диапазоне от 1974 до {}".format(today_year))
        elif not (message.text >= data["year_min"]):    # проверяем максимальный рейтинг, что бы он не был меньше минимального
            bot.send_message(chat_id=message.chat.id, text="Максимальный год должен быть больше или равен минимальному")
        else:
            bot.send_message(chat_id=message.chat.id, text="Введите тип:", reply_markup=type_movie.type_button_reply())
            bot.set_state(user_id=message.from_user.id, state=UserFilterSettings.content_type, chat_id=message.chat.id)
            data["year_max"] = message.text


@bot.message_handler(state=UserFilterSettings.content_type)
def get_rating_max(message: Message) -> None:
    """Функция проверки ввода типа"""
    if message.text not in type_list:   # проверяем наличие типа
        bot.send_message(chat_id=message.chat.id, text="К сожалению не нашёл данный тип в своём списке, все имеющиеся типы находятся снизу")
    else:
        bot.send_message(chat_id=message.chat.id, text="Введите жанр:", reply_markup=genre.genre_button_reply())
        bot.set_state(user_id=message.from_user.id, state=UserFilterSettings.genre, chat_id=message.chat.id)
        with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
            data["type_movie"] = message.text


@bot.message_handler(state=UserFilterSettings.genre)
def get_rating_max(message: Message) -> None:
    """Функция проверки ввода жанра"""
    if message.text not in genre_lst:   # проверяем наличие жанра
        bot.send_message(chat_id=message.chat.id, text="К сожалению не нашёл данный жанр в своём списке, все имеющиеся жанры находятся снизу")
    else:
        bot.send_message(chat_id=message.chat.id, text="Введите страну:", reply_markup=country.country_button_reply())
        bot.set_state(user_id=message.from_user.id, state=UserFilterSettings.country, chat_id=message.chat.id)
        with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
            data["genre"] = message.text


@bot.message_handler(state=UserFilterSettings.country)
def get_rating_max(message: Message) -> None:
    if message.text not in country_list:   # проверяем наличие страны
        bot.send_message(chat_id=message.chat.id, text="К сожалению не нашёл данную страну в своём списке, все имеющиеся страны находятся снизу")
    else:
        with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
            data["country"] = message.text

        user_id = message.from_user.id
        update_data_filter(user_id=user_id, rating_min=data["rating_min"], rating_max=data["rating_max"],
                           year_min=data["year_min"], year_max=data["year_max"],
                           type_film=data["type_movie"], genre=data["genre"], country=data["country"])  # обновляем таблицу FilterData

        text = "*Новые настройки фильтра сохранены:*\n" \
               "*Рейтинг:* _от {rating_min} до {rating_max}_\n" \
               "*Год:* _с {year_min} по {year_max}_\n" \
               "*Тип:* _{type_movie}_\n" \
               "*Жанр:* _{genre}_\n" \
               "*Страна:* _{country}_".format(
                        rating_min=data["rating_min"], rating_max=data["rating_max"],
                        year_min=data["year_min"], year_max=data["year_max"],
                        type_movie=data["type_movie"], genre=data["genre"], country=data["country"]
                    )

        bot.send_message(chat_id=message.chat.id, text=text, parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())
        bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)
