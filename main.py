from loguru import logger

from loader import bot
from telebot.custom_filters import StateFilter
import handlers  # noqa
from utils.set_bot_commands import set_default_commands
from database.models import create_models


if __name__ == "__main__":
    create_models()
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    logger.info("bot started")
    bot.polling()
    logger.info("bot stopped")
