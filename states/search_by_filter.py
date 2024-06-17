from telebot.handler_backends import State, StatesGroup


# 1. поиск фильма по фильтру
class SearchMovieByFilter(StatesGroup):
    """Клас состояний пользователя"""
    movie_search = State()
    movie_count = State()