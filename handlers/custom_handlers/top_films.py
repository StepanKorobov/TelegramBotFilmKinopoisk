from telebot.types import Message
from loguru import logger
import time

from loader import bot
from utils import site_api_handler, message_film_description
from utils.misc.get_type_genre_country_list import get_top_movie_dick_eng
from config_data.config import URL, HEADERS
from database.CRUD import receive_data_user, store_data_history, receive_data_history_last, store_data_query_result
from keyboards.reply.start import start_button
from keyboards.inline.top_movie import top_movie_button
from states.top_movie import UserRatingSelection


top_movie_list = get_top_movie_dick_eng()   # словарь из топ фильмов


@bot.message_handler(commands=["top_films"])
def bot_start(message: Message):
    """Функция, которая запускает событие для вывода топа фильмов"""
    user_id = message.from_user.id
    logger.info("user {user_id}, use command '/top_films'".format(user_id=user_id))     # записываем информацию о действии в лог

    if receive_data_user(user_id=user_id):  # проверяем, есть ли пользователь в таблице User
        bot.set_state(user_id=message.from_user.id, state=UserRatingSelection.rating_selection, chat_id=message.chat.id)
        bot.send_message(chat_id=message.chat.id, text="Выберете рейтинг:", reply_markup=top_movie_button())
    else:
        bot.send_message(chat_id=message.chat.id, text="Для того, что бы начать введите '/start' или нажмите кнопку СТАРТ", reply_markup=start_button())


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """Функция отлавливания inline кнопок"""
    with bot.retrieve_data(call.from_user.id) as data:
        data["type"] = call.data
        bot.set_state(user_id=call.from_user.id, state=UserRatingSelection.count_selection, chat_id=call.message.chat.id)
        text = "Вы выбрали: *{top_type}*.".format(top_type=top_movie_list[data["type"]])
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=text, parse_mode="Markdown")
        bot.send_message(chat_id=call.message.chat.id, text="Введите количество результатов (максимально 20): ")


@bot.message_handler(state=UserRatingSelection.rating_selection)
def history_get_num(message: Message) -> None:
    """Функция сообщает пользователю, о необходимости выбрать вариант"""
    bot.send_message(chat_id=message.chat.id, text="Вы можете выбрать вариант, из сообщения выше.")


param = {
        "page": 1,
        "notNullFields": "lists",
        "sortField": "lists",
        "sortType": "1"
    }


@bot.message_handler(state=UserRatingSelection.count_selection)
def history_get_num(message: Message) -> None:
    """Функция делающая запрос API и выводящая кинопремьеры"""
    if not message.text.isdigit():  # проверяем на число
        bot.send_message(chat_id=message.chat.id, text="Нужно написать только цифры")
    elif not (0 < int(message.text) < 21):   # проверяем диапазон
        bot.send_message(chat_id=message.chat.id, text="Введите количества фильмов в диапазоне от 1 до 20")
    else:
        user_id = message.from_user.id

        with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
            data["count"] = int(message.text)
            param["limit"] = data["count"]
            param["lists"] = data["type"]

        response = site_api_handler.get_films(method="GET", url=URL, headers=HEADERS, params=param, type_list="movie")  # делаем запрос

        if isinstance(response, dict):  # если словарь, значит мы получили ответ от API в функции get_films
            data = response

            result = [data["docs"][i] for i in range(len(data["docs"]))]

            titles = "*Команда: *'_topfilms_', рейтинг: {type_film}, результатов: {count_result}".format(
                type_film=top_movie_list[param["lists"]], count_result=param["limit"])  # описание для истории

            try:
                store_data_history(user_id=user_id, title=titles)  # записываем описание действия в таблицу History
                last_history_id = receive_data_history_last(user_id=user_id)  # получаем id последней записи текущего пользователя из History
            except Exception as exc:
                logger.error("{message_err}, type:{type_err}".format(message_err=exc, type_err=type(exc)))    # записываем исключение в лог

            for i, i_film in enumerate(result):
                poster = message_film_description.film_poster(data=i_film)  # получаем постер для фильма
                text = message_film_description.full_film_message(data=i_film)  # получаем полную информацию о фильме из ответа API

                tex_top = "".join(("Рейтинг: {rating}. Место: {num}\n\n".format(rating=top_movie_list[param["lists"]], num=i+1), text))  # добавляем в описание название рейтинга и место

                try:
                    store_data_query_result(history_id=last_history_id, user_id=user_id, poster=poster, text=tex_top)  # записываем результат запроса в QueryResult
                except Exception as exc:
                    logger.error("{message_err}, type:{type_err}".format(message_err=exc, type_err=type(exc)))    # записываем исключение в лог

                bot.send_photo(chat_id=message.chat.id, photo=poster, caption=tex_top, parse_mode="Markdown")
                time.sleep(1.3)     # пауза, что бы не спамить(ботом могут пользоваться несколько людей, работе не мешает)
        else:
            bot.send_message(chat_id=message.chat.id, text="У меня возникли небольшие трудности, попробуйте ещё раз через 1 минуту.")

        bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)
