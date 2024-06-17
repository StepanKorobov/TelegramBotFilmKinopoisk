from typing import List, Dict

from database.CRUD import receive_data_filter
from utils.misc.move_type_translate import movie_type


def get_param_from_filter(user_id: int) -> Dict:
    """
    Функция возвращает словарь параметров фильтра пользователя

    :param user_id: id пользователя в телеграмме
    :type: str
    :return: возвращает словарь параметров фильтра
    :rtype: List
    """
    param_filter = receive_data_filter(user_id=user_id)     # получаем параметры фильтра пользователя
    param_filter_prepared = [i_param if i_param != "Все" else "!" for i_param in param_filter]
    param = {
        'rating.kp': f'{param_filter_prepared[0]}-{param_filter_prepared[1]}',
        'year': f'{param_filter_prepared[2]}-{param_filter_prepared[3]}',
        'type': f'{movie_type(mov_type=param_filter_prepared[4], lang="eng")}',
        'genres.name': f"{param_filter_prepared[5].lower()}",
        'countries.name': f"{param_filter_prepared[6]}"
    }

    return param
