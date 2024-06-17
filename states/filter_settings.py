from telebot.handler_backends import State, StatesGroup


# 1. рейтинг от
# 2. рейтинг до
# 3. год от
# 4. год до
# 5. тип
# 6. жанр
# 7. страна
class UserFilterSettings(StatesGroup):
    """Клас состояний пользователя"""
    rating_min = State()
    rating_max = State()
    year_min = State()
    year_max = State()
    content_type = State()
    genre = State()
    country = State()
