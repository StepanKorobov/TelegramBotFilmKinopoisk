from telebot.handler_backends import State, StatesGroup


# 1. просмотр истории
class UserHistoryView(StatesGroup):
    """Клас состояний пользователя"""
    history_view = State()
