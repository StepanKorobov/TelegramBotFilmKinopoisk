from telebot.types import Message
from loguru import logger

from loader import bot
from states.history_view import UserHistoryView
from database.CRUD import receive_data_histories, receive_data_query_result, receive_data_user
from keyboards.reply.start import start_button


@bot.message_handler(commands=["history"])
def history(message: Message) -> None:
    """Функция отправляющая историю запросов пользователю"""
    user_id = message.from_user.id
    logger.info("user {user_id}, use command '/history'".format(user_id=user_id))  # записываем информацию о действии в лог

    if receive_data_user(user_id=user_id):  # проверяем, есть ли пользователь в таблице User
        bot.set_state(user_id=message.from_user.id, state=UserHistoryView.history_view, chat_id=message.chat.id)
        history_list = receive_data_histories(user_id)  # извлекаем историю поиска из БД User

        if history_list:    # проверяем, есть ли у пользователя история запросов
            for i_id, i_history in enumerate(history_list):    # отправляем пользователю историю
                text = "({id}). Дата и время: {datetime}\n" \
                       "{title}".format(
                            id=i_id + 1,
                            datetime=str(i_history[1])[:-6],
                            title=i_history[2])

                bot.send_message(message.from_user.id, text, parse_mode="Markdown")

            bot.send_message(chat_id=message.chat.id, text="Введите номер интересующего вас варианта:")
        else:   # история запросов отсутствует, информируем пользователя
            bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)
            bot.send_message(chat_id=message.chat.id, text="Вы ещё ничего не искали, поэтому у вас нет истории поиска.")
    else:   # если не нашли пользователя, предлагаем авторизоваться
        bot.send_message(chat_id=message.chat.id, text="Для того, что бы начать введите '/start' или нажмите кнопку СТАРТ", reply_markup=start_button())


@bot.message_handler(state=UserHistoryView.history_view)
def history_get_num(message: Message) -> None:
    """Функция, которая отправляет пользователю результат(ы) запроса, нужно выбрать запрос"""
    user_id = message.from_user.id
    history_list = receive_data_histories(user_id=user_id)  # извлекаем историю поиска из БД User
    user_answer = message.text

    # проверяем правильно ли написал пользователь (должно быть числа в интервале от 1 до длины history_list)
    if not user_answer.isdigit():
        bot.send_message(chat_id=message.chat.id, text="Номер должен состоять только из цифр:")
    elif not (0 < int(user_answer) < len(history_list) + 1):
        bot.send_message(chat_id=message.chat.id, text="Нужно ввести число от 1 до {max_num_history}".format(max_num_history=len(history_list)))
    else:
        history_id = history_list[int(user_answer)-1][0]    # получаем id истории
        query_result_list = receive_data_query_result(user_id=user_id, history_id=history_id)   # извлекаем из БД QueryResult все результаты запроса по history_id

        for i_query_result in query_result_list:    # отправляем результаты запроса в чат
            if i_query_result[0] != "None":     # проверяем наличие постера
                bot.send_photo(chat_id=message.chat.id, photo=i_query_result[0], caption=i_query_result[1], parse_mode="Markdown")
            else:   # если постера нет, отправляем обычное сообщение
                bot.send_message(chat_id=message.chat.id, text=i_query_result[1], parse_mode="Markdown")

        bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)
