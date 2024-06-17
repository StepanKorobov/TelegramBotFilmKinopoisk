from loguru import logger
from typing import Dict, Union
import requests


def _make_response(method: str, url: str, headers: Dict, params: Dict,
                   timeout: int = 10, success: int = 200) -> Union[requests.models.Response, int]:
    """
    Функция, которая производит запрос на сервер API

    :param method: Метод запроса GET или POST
    :param url: url API на который будет производиться запрос
    :param headers: передается ключ API и тип ресурса
    :param params: передаются параметры запроса
    :param timeout: время ожидания ответа от ресурса
    :param success: код успешного запроса
    :return: возвращает результат запроса, либо код ответа сервера
    :rtype: requests.models.Response, int
    """
    status_code = ""
    try:
        response = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            timeout=timeout
        )

        status_code = response.status_code

        if status_code == success:
            return response.json()
        elif status_code == 403:
            logger.critical("You have used up your daily limit on API requests, {status_code}, {message}".format(
              status_code=status_code, message=response.text
            ))
    except requests.exceptions.ReadTimeout as exc:  # ответ ждём дольше чем timeout
        logger.error("long response from the server: {message_err}, type:{type_err}".format(message_err=exc, type_err=type(exc)))
    except Exception as exc:
        logger.error("{message_err}, type:{type_err}".format(message_err=exc, type_err=type(exc)))  # записываем исключение в лог
    return status_code


def get_films(method: str, url: str, headers: Dict, params: Dict,
                       type_list: str, timeout: int = 10, func=_make_response) -> Union[requests.models.Response, int]:
    """
    Функция, для конструирования url и вызова функции высшего порядка

    :param method: Метод запроса GET или POST
    :param url: url API на который будет производиться запрос
    :param headers: передается ключ API и тип ресурса
    :param params: передаются параметры запроса
    :param type_list: вторя часть url, куда будем делать запрос
    :param timeout: время ожидания ответа от ресурса
    :param func: функция высшего порядка, в которую будем передавать параметры
    :return: возвращает результат запроса, либо код ответа сервера
    :rtype: requests.models.Response, int
    """
    url = "{0}/{1}".format(url, type_list)

    response = func(method=method, url=url, headers=headers, params=params, timeout=timeout)

    return response


def get_film_to_id(method: str, url: str, headers: Dict, params: Dict, id: str,
                       action: str, timeout: int = 10, func=_make_response) -> Union[requests.models.Response, int]:
    """
    Функция, для конструирования url и вызова функции высшего порядка
    Данная функция исключительно для поиска фильмов по ID

    :param method: Метод запроса GET или POST
    :param url: url API на который будет производиться запрос
    :param headers: передается ключ API и тип ресурса
    :param params: передаются параметры запроса
    :param id: ID фильма
    :param action: действие с фильмом
    :param timeout: время ожидания ответа от ресурса
    :param func: функция высшего порядка, в которую будем передавать параметры
    :return: возвращает результат запроса, либо код ответа сервера
    :rtype: requests.models.Response, int
    """
    url = "{0}/{1}/{2}".format(url, id, action)

    response = func(method=method, url=url, headers=headers, params=params, timeout=timeout)

    return response
