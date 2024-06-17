from datetime import datetime
from loguru import logger

from telebot.types import Message, ReplyKeyboardRemove
from loader import bot
from database.CRUD import store_data_user, receive_data_user, store_data_filter_set_default


@bot.message_handler(commands=["start"],)
def bot_start(message: Message):
    """
    Функция команды /start, проверяет есть ли пользователь в БД, если нет,
    то создаёт запись в User и записывает стандартные настройки фильтра в FilterData

    :param message: /start
    :type: Message
    """
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    # Проверяем наличие пользователя в таблице User
    if receive_data_user(user_id):
        # Пользователь найден, говорим, что рады его снова видеть
        bot.send_message(chat_id=message.chat.id, text="Рад снова видеть тебя, {fullname}!".format(
            fullname=message.from_user.full_name), reply_markup=ReplyKeyboardRemove())

    else:
        # Пользователь не найден, записываем его в User и выставляем дефолтный фильтр с текущей датой в FilterDate
        store_data_user(user_id=user_id, username=username, first_name=first_name, last_name=last_name)
        today_year = str(datetime.today())[0:4]     # текущая дата для фильтра
        store_data_filter_set_default(user_id=user_id, today_year=today_year)   # устанавливаем стандартный фильтр для пользователя
        bot.send_message(chat_id=message.chat.id,
                         text="Привет, {fullname}! Я кинобот, могу найти для вас фильмы по фильтру или рейтингу, а так же показать грядущие кинопремьеры.".format(
                            fullname=message.from_user.full_name), reply_markup=ReplyKeyboardRemove())
        logger.info("new user {user_id} was successfully added to the User table".format(user_id=user_id))     # добавляем в лог успешно добавленного пользователя
