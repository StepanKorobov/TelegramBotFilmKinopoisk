from telebot.handler_backends import State, StatesGroup


# 1. выбор даты премьеры
# 2. выбор количества фильмов в запросе
class UserDatePremier(StatesGroup):
    """Клас состояний пользователя """
    premier_date_selection = State()
    count_selection = State()
