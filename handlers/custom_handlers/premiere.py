from telebot.types import Message, ReplyKeyboardRemove
from loguru import logger
import time

from loader import bot
from utils import site_api_handler, message_film_description
from utils.misc.get_type_genre_country_list import get_premier_date, get_premier_date_revers
from config_data.config import URL, HEADERS
from database.CRUD import receive_data_user, store_data_history, receive_data_history_last, store_data_query_result
from keyboards.reply.start import start_button
from keyboards.reply.premiere import premiere_button_reply
from states.premiere import UserDatePremier


premiere_dict = get_premier_date()  # получаем словарь с датами премьер
premiere_dict_revers = get_premier_date_revers()  # получаем обратный словарь (ключи и значения поменяны местами)


@bot.message_handler(commands=["premiere"],)
def premiere_command(message: Message) -> None:
    """Функция, которая запускает сценарий поиска кинопремьер"""
    user_id = message.from_user.id
    logger.info("user {user_id}, use command '/premiere'".format(user_id=user_id))  # записываем информацию о действии в лог

    if receive_data_user(user_id=user_id):  # проверяем, есть ли пользователь в таблице User
        bot.set_state(user_id=message.from_user.id, state=UserDatePremier.premier_date_selection, chat_id=message.chat.id)
        bot.send_message(chat_id=message.chat.id, text="Выберете год и месяц премьеры:", reply_markup=premiere_button_reply())
    else:
        bot.send_message(chat_id=message.from_user.id, text="Для того, что бы начать введите '/start' или нажмите кнопку СТАРТ", reply_markup=start_button())


@bot.message_handler(state=UserDatePremier.premier_date_selection)
def premiere_date(message: Message) -> None:
    """Функция, отслеживающая выбор даты"""
    if not (message.text in premiere_dict.keys()):
        bot.send_message(chat_id=message.chat.id, text="Выберете дату кинопремьеры, нажав на одну из кнопок снизу:", reply_markup=premiere_button_reply())
    else:
        with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
            data["date"] = premiere_dict[message.text]

        bot.set_state(user_id=message.from_user.id, state=UserDatePremier.count_selection, chat_id=message.chat.id)
        bot.send_message(chat_id=message.chat.id, text="Введите количество результатов (максимально 20):", reply_markup=ReplyKeyboardRemove())


param = {
        "notNullFields": "premiere.russia"
    }


@bot.message_handler(state=UserDatePremier.count_selection)
def get_premiere(message: Message):
    """Функция, которая отправляет запрос к API для получения кинопремьер"""
    if not message.text.isdigit():  # проверяем на число
        bot.send_message(chat_id=message.chat.id, text="Количество фильмов не может содержать буквы")
    elif not (0 < int(message.text) < 21):  # проверяем диапазон
        bot.send_message(chat_id=message.chat.id, text="Количество фильмов должно быть от 1 до 20")
    else:
        user_id = message.from_user.id

        with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
            data["count"] = int(message.text)
            param["limit"] = data["count"]
            param["premiere.russia"] = data["date"]
        response = site_api_handler.get_films(method="GET", url=URL, headers=HEADERS, params=param, type_list="movie")

        if isinstance(response, dict):  # если словарь, значит мы получили ответ от API в функции get_films
            data = response
            result = [data["docs"][i] for i in range(len(data["docs"]))]

            titles = "*Команда:* '_premiere_', {date_premiere}, результатов: {count_result}".format(
                date_premiere=premiere_dict_revers[param["premiere.russia"]], count_result=param["limit"])  # описание для истории

            try:
                store_data_history(user_id=user_id, title=titles)  # записываем описание действия в таблицу History
                last_history_id = receive_data_history_last(
                    user_id=user_id)  # получаем id последней записи текущего пользователя из History
            except Exception as exc:
                logger.error("{message_err}, type:{type_err}".format(message_err=exc, type_err=type(exc)))    # записываем исключение в лог

            for i, i_film in enumerate(result):
                poster = message_film_description.film_poster(data=i_film)  # получаем постер для фильма
                text = message_film_description.full_film_message(
                    data=i_film)  # получаем полную информацию о фильме из ответа API

                try:
                    store_data_query_result(history_id=last_history_id, user_id=user_id, poster=poster,
                                            text=text)  # записываем результат запроса в QueryResult
                except Exception as exc:
                    logger.error("{message_err}, type:{type_err}".format(message_err=exc, type_err=type(exc)))    # записываем исключение в лог

                bot.send_photo(chat_id=message.chat.id, photo=poster, caption=text, parse_mode="Markdown")
                time.sleep(1.3)     # пауза, что бы не спамить(ботом могут пользоваться несколько людей, работе не мешает)
        else:
            bot.send_message(chat_id=message.chat.id,
                             text="У меня возникли небольшие трудности, попробуйте ещё раз через 1 минуту.")

        bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)
