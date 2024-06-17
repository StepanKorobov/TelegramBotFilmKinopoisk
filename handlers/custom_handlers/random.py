from telebot.types import Message, ReplyKeyboardRemove
from loguru import logger

from loader import bot
from utils import site_api_handler, message_film_description
from config_data.config import URL, HEADERS
from database.CRUD import store_data_history, receive_data_history_last, store_data_query_result, receive_data_user
from utils.misc.get_param_from_filter import get_param_from_filter
from keyboards.reply.start import start_button


@bot.message_handler(commands=["random"])
def random_film(message: Message) -> None:
    """Функция, которая отправляет запрос к API для получения случайного фильма, используя фильтр пользователя"""
    user_id = message.from_user.id
    logger.info("user {user_id}, use command '/random'".format(user_id=user_id))  # записываем информацию о действии в лог

    if receive_data_user(user_id=user_id): # проверяем, есть ли пользователь в таблице User
        bot.delete_state(user_id=user_id, chat_id=message.chat.id)  # убираем статус, так как пользователь мог выполнять сценарий команды

        param = get_param_from_filter(user_id=user_id)  # получаем параметры фильтра пользователя
        response = site_api_handler.get_films(timeout=10, method="GET", url=URL, headers=HEADERS, params=param,
                                              type_list="movie/random")     # делаем запрос к API для получения случайного фильма используя фильтр пользователя

        if isinstance(response, dict):  # если словарь, значит мы получили ответ от API в функции get_films
            data = response

            poster = message_film_description.film_poster(data=data)  # получаем постер для фильма
            text = message_film_description.full_film_message(data=data)     # получаем полную информацию о фильме из ответа API
            title = message_film_description.short_film_message(data=data)       # краткая информация о фильме
            title = "".join(("*Команда:* '_random_', краткое описание:\n", title))       # информация для записи в таблицу History

            if poster is not None:  # если постер отсутствует, отправляем обычное сообщение
                bot.send_photo(chat_id=message.chat.id, photo=poster, caption=text, parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())
            else:
                poster = "None"    # нужно, что бы при извлечении истории всё было корректно
                logger.warning("The 'poster' field value is empty")     # записываем информацию об отсутствии постера в лог
                bot.send_message(chat_id=message.chat.id, text=text, parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())

            try:    # отлавливаем ошибки при записи
                store_data_history(user_id=user_id, title=title)    # записываем описание действия в таблицу History
                last_history_id = receive_data_history_last(user_id=user_id)    # получаем id последней записи текущего пользователя из History
                store_data_query_result(history_id=last_history_id, user_id=user_id, poster=poster, text=text)    # записываем результат запроса в QueryResult
            except Exception as exc:
                logger.error("{message_err}, type:{type_err}".format(message_err=exc, type_err=type(exc)))    # записываем исключение в лог
                store_data_query_result(history_id=last_history_id, user_id=user_id, poster="None", text=text)  # записываем результат запроса в QueryResult
        elif (response is None) or (response == 400):     # если API ответил что-то из этого, значит он ничего не нашёл
            bot.send_message(chat_id=message.chat.id, text="К сожалению я ничего не нашёл по вашему фильтру.")
        else:
            bot.send_message(chat_id=message.chat.id, text="У меня возникли небольшие трудности, попробуйте ещё раз через 1 минуту.")
    else:
        bot.send_message(chat_id=message.from_user.id, text="Для того, что бы начать введите '/start' или нажмите кнопку СТАРТ", reply_markup=start_button())
