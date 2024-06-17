from typing import  List, Dict

from utils.misc.move_type_translate import movie_type


def _genres_film(genre_list: list[dict]) -> str:
    """
    Функция для получения жанров

    :param genre_list: список содержащий словари из названий жанров
    :type: list[dict]
    :return: строку, в которой указанны жанры через запятую
    :rtype: str
    """
    genre_lst = list()

    for i_genre in genre_list:
        genre_lst.append(i_genre['name'])

    genre_str = ", ".join(genre_lst)

    return genre_str


def _countries_film(countries_list: List[Dict]) -> str:
    """
    Функция для получения стран

    :param countries_list: список содержащий словари из названий стран
    :type: list[dict]
    :return: строку, в которой указанны страны через запятую
    :rtype: str
    """
    countries_lst = list()

    for i_countries in countries_list:
        countries_lst.append(i_countries['name'])

    countries_str = ", ".join(countries_lst)

    return countries_str


def full_film_message(data: Dict, sym_limit: int = 512) -> str:
    """
    Функция формирующая сообщение с полным описанием фильма

    :param sym_limit: Принимает ограничение в количестве символов(если их больше, то в конце текста появится многоточие)
    :type: int
    :param data: принимает словарь из списка (который получаем в ответе от API)
    :type: dict
    :return: возвращает строку с полным описание фильма
    :rtype: str
    """
    message_text = "*{name_rus}{name_eng}*\n\n" \
                   "Кинопоиск: {rating_kinopoisk}\nIMDb: {rating_IMDb}\nThemoviedb: {rating_Themoviedb}\n\n" \
                   "Тип: _{type}_\n" \
                   "Жанр: _{genre}_\n" \
                   "Год: _{year}_\n" \
                   "Страна: _{countries}_\n\n" \
                   "{description}".format(
        name_rus=data['name'], name_eng=" ({})".format(data['alternativeName']) if data['alternativeName'] else ".",
        rating_kinopoisk=data['rating']['kp'], rating_IMDb=data['rating']['imdb'],
        rating_Themoviedb=data['rating']['filmCritics'],
        type=movie_type(mov_type=data["type"], lang="rus"),
        genre=_genres_film(genre_list=data['genres']),
        year=data['year'],
        countries=_countries_film(countries_list=data['countries']),
        description=data['description']
    )

    if len(message_text) >= sym_limit:
        message_text = "".join((message_text[0:sym_limit-3], "..."))

    return message_text


def short_film_message(data: Dict) -> str:
    """
        Функция формирующая сообщение с кратким описанием фильма

        :param data: принимает словарь из списка (который получаем в ответе от API)
        :type: dict
        :return: возвращает строку с кратким описание фильма
        :rtype: str
    """
    message_text = "*{name}* | " \
                   "{type} | " \
                   "kp: {rating_kinopoisk} | " \
                   "{year} | " \
                   "{countries} | " \
                   "{genre}".format(
        name=data['name'],
        type=movie_type(mov_type=data["type"], lang="rus"),
        rating_kinopoisk=data['rating']['kp'],
        year=data['year'],
        countries=_countries_film(countries_list=data['countries']),
        genre=_genres_film(genre_list=data['genres']),
    )

    return message_text


class NotNullPoster(BaseException):
    pass


def film_poster(data: Dict) -> str:
    """
    Функция для получения постера к фильму

    :param data: словарь содержащий постер (ответ от API)
    :type: dict
    :return: возвращает строку со ссылкой на постер
    :rtype: str
    """
    poster = data['poster']['previewUrl']

    return poster
