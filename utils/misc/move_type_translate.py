movie_translate_rus = {
            "!": "!",
            "movie": "Фильм",
            "cartoon": "Мультфильм",
            "tv-series": "Сериал",
            "animated-series": "Анимация",
            "anime": "Аниме"
        }

movie_translate_eng = {
            "!": "!",
            "Фильм": "movie",
            "Мультфильм": "cartoon",
            "Сериал": "tv-series",
            "Анимация": "animated-series",
            "Аниме": "anime"
}


def movie_type(mov_type: str, lang: str) -> str:
    """
    Функция для замены типа фильма(заменяет только название) с английского на русский язык, и наоборот

    :param mov_type: тип фильма на английском языке
    :type: str
    :param lang: на кокой язык нужно сменить (rus, eng)
    :return: возвращает тип фильма на русском или английском языке
    :rtype: str
    """

    movie_translate = ""

    if lang == "rus":
        movie_translate = movie_translate_rus
    elif lang == "eng":
        movie_translate = movie_translate_eng

    if mov_type in movie_translate:
        return movie_translate[mov_type]

    return mov_type
#