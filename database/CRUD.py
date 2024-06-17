from typing import List, Tuple
from peewee import DoesNotExist

from database.models import User, History, QueryResult, FilterData


def store_data_user(user_id: int, username: str, first_name: str, last_name: str) -> None:
    """
    Функция записывающая пользователя в User

    :param user_id: id пользователя в телеграмме
    :type: int
    :param username: Ник в телеграмме
    :type: str
    :param first_name: Имя в телеграмме
    :type: str
    :param last_name: Фамилия в телеграмме
    :type: str
    """
    User.create(
        user_id=user_id,
        username=username,
        first_name=first_name,
        last_name=last_name
    )


def receive_data_user(user_id: int) -> bool:
    """
    Функция проверяющая наличия пользователя в User

    :param user_id: id пользователя в телеграмме
    :type: int
    :return: True or False
    :rtype: bool
    """
    try:
        User.get_by_id(user_id)
        return True
    except DoesNotExist:
        return False


def store_data_history(user_id: int, title: str) -> None:
    """
    Функция записывающая id пользователя и краткое описание его действия в History

    :param user_id: id пользователя в телеграмме
    :type: int
    :param title: краткое описание действия пользователя (Время, команда, фильтр)
    :type: str
    """
    History.create(
        user_id=user_id,
        title=title
    )


def receive_data_history_last(user_id: int) -> int:
    """
    Функция возвращает последнее id истории для конкретного пользователя (нужно, что бы в будущем записать id истории в QueryResult)

    :param user_id: id пользователя в телеграмме
    :type: int
    :return: возвращает последний id истории поиска по id пользователя
    :rtype: int
    """
    user = User.get_or_none(User.user_id == user_id)

    histories_last = user.stories.order_by(-History.history_id).get()
    result: int = int(histories_last.history_id)

    return result


def receive_data_histories(user_id: int, count_limit: int = 10) -> List[Tuple]:
    """
    Функция возвращающая историю поиска

    :param user_id: id пользователя в телеграмме
    :type: int
    :param count_limit: лимит по количество историй поиска (по умолчанию 10)
    :type: int
    :return: возвращает список из историй поиска
    :rtype: List[Tuple]
    """
    user = User.get_or_none(User.user_id == user_id)

    histories: List = user.stories.order_by(-History.history_id).limit(count_limit)
    result: List[Tuple] = [(i_person.history_id, i_person.created_at, i_person.title)
                           for i_person in reversed(histories)]

    return result


def store_data_query_result(history_id: int, user_id: int, poster: str, text: str) -> None:
    """
    Функция для записи результатов поиска в QueryResult

    :param history_id:  id истории поиска (нужно для того, что бы вре результаты поиска были прикреплены к одному id истории,
    например топ фильмов выдаст 20 результатов, все они будут под одним id истории)
    :type: int
    :param user_id: id пользователя в телеграмме
    :type: int
    :param poster: url постера
    :type: str
    :param text: текст, который был отправлен пользователю под результатом
    :type: str
    """
    QueryResult.create(
        user_id=user_id,
        history_id=history_id,
        poster=poster,
        text=text
    )


def receive_data_query_result(user_id: int, history_id: int) -> List:
    """
    Функция, которая выдает все результаты запроса по id истории

    :param user_id: id пользователя в телеграмме
    :type: int
    :param history_id: id истории
    :type: int
    :return: возвращает список из результатов запроса
    :rtype: List
    """
    if History.get_or_none(History.user_id == user_id):
        history = History.get_or_none(History.history_id == history_id)
        query_result: List = history.query_result.order_by(-QueryResult.query_id).limit(20)
        result: List[Tuple] = [(i_query_result.poster, i_query_result.text)
                               for i_query_result in reversed(query_result)]

        return result


def store_data_filter(user_id: str, rating_min: str, rating_max: str,
                      year_min: str, year_max: str,
                      type_film: str, genre: str, country: str) -> None:
    """
    Функция записывающая параметры фильтра в FilterData

    :param user_id: id пользователя в телеграмме
    :type: str
    :param rating_min: минимальный рейтинг
    :type: str
    :param rating_max: максимальный рейтинг
    :type: str
    :param year_min: минимальный год
    :type: str
    :param year_max: максимальный год
    :type: str
    :param type_film: тип (фильм, мультфильм, сериал и т.д)
    :type: str
    :param genre: жанр
    :type: str
    :param country: страна
    :type: str
    """
    FilterData.create(
        user_id=user_id,
        rating_min=rating_min,
        rating_max=rating_max,
        year_min=year_min,
        year_max=year_max,
        type_film=type_film,
        genre=genre,
        country=country
    )


def store_data_filter_set_default(user_id: int, today_year: str) -> None:
    """
    Функция для установки стандартно фильтра, записывает в FilterData

    :param user_id: id пользователя в телеграмме
    :type: str
    :param today_year: текущий год
    :type: str
    """
    FilterData.create(
        user_id=user_id,
        rating_min="5.0",
        rating_max="10.0",
        year_min="2000",
        year_max=today_year,
        type_film="Все",
        genre="Все",
        country="Все"
    )


def update_data_filter(user_id: int, rating_min: int, rating_max: int,
                       year_min: int, year_max: int,
                       type_film: str, genre: str, country: str) -> None:
    """
    Функция для обновления фильтра пользователя в FilterData

    :param user_id: id пользователя в телеграмме
    :type: str
    :param rating_min: минимальный рейтинг
    :type: str
    :param rating_max: максимальный рейтинг
    :type: str
    :param year_min: минимальный год
    :type: str
    :param year_max: максимальный год
    :type: str
    :param type_film: тип (фильм, мультфильм, сериал и т.д)
    :type: str
    :param genre: жанр
    :type: str
    :param country: страна
    :type: str
    """
    user = User.get_or_none(User.user_id == user_id)
    filter_data: FilterData = user.filter_data.order_by(-FilterData.filter_id).get()
    filter_data.rating_min = rating_min
    filter_data.rating_max = rating_max
    filter_data.year_min = year_min
    filter_data.year_max = year_max
    filter_data.type_film = type_film
    filter_data.genre = genre
    filter_data.country = country
    filter_data.save()


def receive_data_filter(user_id: int) -> List:
    """
    Функция для получения текущих настроек фильтра

    :param user_id: id пользователя в телеграмме
    :type: str
    :return: список параметров фильтра
    :rtype: List
    """
    user = User.get_or_none(User.user_id == user_id)
    filter_data = user.filter_data.order_by(-FilterData.filter_id).get()
    result: List = [filter_data.rating_min, filter_data.rating_max, filter_data.year_min, filter_data.year_max,
                    filter_data.type_film, filter_data.genre, filter_data.country]

    return result
