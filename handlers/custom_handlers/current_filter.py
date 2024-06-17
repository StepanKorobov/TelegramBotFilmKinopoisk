from telebot.types import Message
from loguru import logger
from loader import bot

from database.CRUD import receive_data_filter, receive_data_user
from keyboards.reply.start import start_button


@bot.message_handler(commands=["current_filter"])
def current_filter(message: Message):
    """Функция выводит пользователю параметры текущего фильтра"""
    user_id = message.from_user.id
    logger.info("user {user_id}, use command '/current_filter'".format(user_id=message.from_user.id))  # записываем информацию о действии в лог

    if receive_data_user(user_id):  # проверяем, есть ли пользователь в таблице User
        param_filter = receive_data_filter(user_id=user_id)     # получаем параметры фильтра
        param_filter_prepared = [i_param if i_param != "Все" else "!" for i_param in param_filter]  # извлекаем параметры в список

        text = "*Текущие настройки фильтра:*\n" \
               "*Рейтинг:* _от {rating_min} до {rating_max}_\n" \
               "*Год:* _с {year_min} по {year_max}_\n" \
               "*Тип:* _{type_movie}_\n" \
               "*Жанр:* _{genre}_\n" \
               "*Страна:* _{country}_".format(
                    rating_min=param_filter_prepared[0], rating_max=param_filter_prepared[1],
                    year_min=param_filter_prepared[2], year_max=param_filter_prepared[3],
                    type_movie="Все" if param_filter_prepared[4] == "!" else param_filter_prepared[4],
                    genre="Все" if param_filter_prepared[5] == "!" else param_filter_prepared[5],
                    country="Все" if param_filter_prepared[6] == "!" else param_filter_prepared[6])

        bot.send_message(chat_id=message.chat.id, text=text, parse_mode="Markdown")
    else:
        bot.send_message(chat_id=message.chat.id, text="Для того, что бы начать введите '/start' или нажмите кнопку СТАРТ", reply_markup=start_button())
