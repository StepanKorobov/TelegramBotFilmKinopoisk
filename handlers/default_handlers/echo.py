from telebot.types import Message

from loader import bot
from handlers.default_handlers.start import bot_start


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    if "привет" in message.text.lower():    # ищем слово 'привет' в тексте
        bot.send_message(chat_id=message.chat.id, text="Привет {}".format(message.from_user.full_name))
    elif message.text != "СТАРТ":   # если слово не "старт" выводим эхо
        bot.reply_to(
            message, "Эхо без состояния или фильтра.\n" f"Сообщение: {message.text}"
        )
    else:     # если слово старт слово 'Старт' (нужно для стартовой кнопки)
        bot_start(message)
