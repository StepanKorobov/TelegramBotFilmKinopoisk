from typing import List

from database.CRUD import receive_data_filter


def get_filter_description(user_id: int) -> str:
    """
    Функция краткое описание фильтра пользователя

    :param user_id: id пользователя в телеграмме
    :type: str
    :return: возвращает словарь параметров фильтра
    :rtype: List
    """
    param_filter = receive_data_filter(user_id=user_id)     # получаем параметры фильтра пользователя
    param_filter_prepared = [i_param  for i_param in param_filter]
    text = "рейтинг: {rating_min}-{ranting_max} | год {year_min}-{year_max} | тип: {type_movie} | жанр: {genre} | страна: {country}".format(
        rating_min=param_filter_prepared[0], ranting_max=param_filter_prepared[1],
        year_min=param_filter_prepared[2], year_max=param_filter_prepared[3],
        type_movie=param_filter_prepared[4], genre=param_filter_prepared[5],
        country=param_filter_prepared[6]
    )

    return text
