from telebot.types import Message, ReplyKeyboardRemove
from loguru import logger
import time

from loader import bot
from utils import site_api_handler, message_film_description
from utils.misc.get_param_from_filter import get_param_from_filter
from utils.misc.filter_description import get_filter_description
from utils.misc.get_type_genre_country_list import get_field_dict, get_field_dict_revers
from config_data.config import URL, HEADERS
from database.CRUD import receive_data_user, store_data_history, receive_data_history_last, store_data_query_result
from keyboards.reply.start import start_button
from keyboards.reply.search_param import search_button_reply
from states.search_by_filter import SearchMovieByFilter


field_dict = get_field_dict()   # получаем словарь с параметрами поиска
field_dict_revers = get_field_dict_revers()     # получаем обратный словарь (ключи и значения поменяны местами)


@bot.message_handler(commands=["search_filter"])
def search_movie_by_filter(message: Message) -> None:
    """Функция запускает события по поиску фильмов используя фильтр пользователя"""
    user_id = message.from_user.id
    logger.info("user {user_id}, use command '/search_filter'".format(user_id=user_id))  # записываем информацию о действии в лог

    if receive_data_user(user_id=user_id):  # проверяем, есть ли пользователь в таблице User
        bot.set_state(user_id=message.from_user.id, state=SearchMovieByFilter.movie_search, chat_id=message.chat.id)
        bot.send_message(chat_id=message.chat.id, text="Выберете как мне отсортировать фильмы: ", reply_markup=search_button_reply())
    else:
        bot.send_message(chat_id=message.chat.id, text="Для того, что бы начать введите '/start' или нажмите кнопку СТАРТ", reply_markup=start_button())


@bot.message_handler(state=SearchMovieByFilter.movie_search)
def search_movie_by_filter(message: Message):
    """Функция обрабатывает выбранную сортировку"""
    if not (message.text in field_dict):
        bot.send_message(chat_id=message.chat.id, text="Вы можете выбрать вариант нажав на кнопку снизу")
    else:
        bot.send_message(chat_id=message.chat.id, text="Введите количество фильмов (Максимум 20): ", reply_markup=ReplyKeyboardRemove())
        bot.set_state(user_id=message.from_user.id, state=SearchMovieByFilter.movie_count, chat_id=message.chat.id)
        with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
            data["sort_field"] = field_dict[message.text]


@bot.message_handler(state=SearchMovieByFilter.movie_count)
def search_movie_by_filter(message: Message):
    """Функция делающая запрос к API с заданными параметрами"""
    if not message.text.isdigit():  # проверяем на число
        bot.send_message(chat_id=message.chat.id, text="Нужно писать только цифры")
    elif not (0 < int(message.text) < 21):   # проверяем диапазон
        bot.send_message(chat_id=message.chat.id, text="Введите диапазон количества фильмов от 1 до 20")
    else:
        user_id = message.from_user.id

        with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
            sort_field = data["sort_field"]

        param = get_param_from_filter(user_id=user_id)
        param["limit"] = message.text   # параметр лимита по количество фильмов при запросе
        param["sortField"] = sort_field[:-1]   # в переменной два значения вид сортировки и тип, записываем вид в параметры
        if sort_field[-1] == "+":   # в переменной два значения вид сортировки и тип, проверяем тип
            param["sortType"] = "-1"
        else:
            param["sortType"] = "1"

        response = site_api_handler.get_films(timeout=10, method="GET", url=URL, headers=HEADERS, params=param, type_list="movie")

        if isinstance(response, dict) and (response["docs"]):  # если словарь, и он не пустой, значит мы получили ответ от API в функции get_films
            data = response
            result = [data["docs"][i] for i in range(len(data["docs"]))]

            user_filter = get_filter_description(user_id=user_id)   # загружаем фильтр пользователя
            titles = "*Команда: *'_searchfilter_', {user_filter}, сортировка: {sort_type}, результатов: {count_result}".format(
                user_filter=user_filter, sort_type=field_dict_revers[sort_field], count_result=param["limit"])

            try:
                store_data_history(user_id=user_id, title=titles)  # записываем описание действия в таблицу History
                last_history_id = receive_data_history_last(user_id)  # получаем id последней записи текущего пользователя из History
            except Exception as exc:
                logger.error("{message_err}, type:{type_err}".format(message_err=exc, type_err=type(exc)))    # записываем исключение в лог

            for i, i_film in enumerate(result):
                poster = message_film_description.film_poster(i_film)  # получаем постер для фильма
                text = message_film_description.full_film_message(i_film)  # получаем полную информацию о фильме из ответа API

                if poster is not None:  # если постер отсутствует, отправляем обычное сообщение
                    bot.send_photo(chat_id=message.chat.id, photo=poster, caption=text, parse_mode="Markdown")
                else:
                    poster = "None"  # нужно, что бы при извлечении истории всё было корректно
                    logger.warning("The 'poster' field value is empty")  # записываем информацию об отсутствии постера в лог
                    bot.send_message(chat_id=message.chat.id, text=text, parse_mode="Markdown")

                try:
                    store_data_query_result(history_id=last_history_id, user_id=user_id, poster=poster, text=text)  # записываем результат запроса в QueryResult
                except Exception as exc:
                    logger.error("{message_err}, type:{type_err}".format(message_err=exc, type_err=type(exc)))  # записываем исключение в лог

                time.sleep(1.3)     # пауза, что бы не спамить(ботом могут пользоваться несколько людей, работе не мешает)
        elif (response is None) or (response == 400) or (data.get("docs", None) is None):     # если API ответил что-то из этого, значит он ничего не нашёл
            bot.send_message(chat_id=message.chat.id, text="К сожалению я ничего не нашёл по вашему фильтру.")
        else:
            bot.send_message(chat_id=message.chat.id, text="У меня возникли небольшие трудности, попробуйте ещё раз через 1 минуту.")

        bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)
