from telebot.handler_backends import State, StatesGroup


# 1. выбор рейтинга
# 2. выбор количества фильмов в запросе
class UserRatingSelection(StatesGroup):
    """Клас состояний пользователя """
    rating_selection = State()
    count_selection = State()
