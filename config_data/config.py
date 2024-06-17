import os
from loguru import logger
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
KINOPOISK_API_KEY = os.getenv("KINOPOISK_API_KEY")
URL = "https://api.kinopoisk.dev/v1.4"
HEADERS = {
    'X-API-KEY': KINOPOISK_API_KEY,
    'accept': 'application/json'
}
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("history", "Вывести историю запросов"),
    ("top_films", "Вывести топ фильмов"),
    ("premiere", "поиск кинопремьер"),
    ("random", "Вывести случайный фильм(использует фильтр)"),
    ("search_filter", "Поиск фильма по фильтру"),
    ("filter", "Настроить фильтр"),
    ("current_filter", "Посмотреть текущий фильтр")
)
path = os.path.abspath("log/debug.log")     # путь папки с логами
logger.add(path, format='{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}',
           level="DEBUG", rotation="100 KB", retention="10 days", compression="zip", serialize=True)     # конфигурация логов
