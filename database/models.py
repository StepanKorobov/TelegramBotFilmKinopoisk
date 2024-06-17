import os

from datetime import datetime
from peewee import (
    AutoField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
)

abs_path_db = os.path.abspath(os.path.join("database", "movie_bot.db"))
db = SqliteDatabase(abs_path_db)    # создаём БД


class BaseModel(Model):
    """Базовый класс. Определяет, базу данных для всех наследуемых от него таблиц"""
    class Meta:
        database = db


class User(BaseModel):
    """Дочерний класс. Определяет, поля таблицы users"""
    user_id = IntegerField(primary_key=True)
    username = CharField()
    first_name = CharField()
    last_name = CharField(null=True)

    class Meta:
        order_by = "user_id"    # автоматическая сортировка по полю user_id


class History(BaseModel):
    """Дочерний класс. Определяет, поля таблицы history"""
    history_id = AutoField()
    user_id = ForeignKeyField(User, backref="stories")
    created_at = DateTimeField(default=datetime.now())
    title = CharField()

    class Meta:
        order_by = "history_id"    # автоматическая сортировка по полю history_id


class QueryResult(BaseModel):
    """Дочерний класс. Определяет, поля таблицы querryresult"""
    query_id = AutoField()
    user_id = IntegerField()
    history_id = ForeignKeyField(History, backref="query_result")
    poster = CharField()
    text = CharField()

    class Meta:
        order_by = "history_id"    # автоматическая сортировка по полю history_id


class FilterData(BaseModel):
    filter_id = AutoField()
    user_id = ForeignKeyField(User, backref="filter_data")
    rating_min = CharField()
    rating_max = CharField()
    year_min = CharField()
    year_max = CharField()
    type_film = CharField()
    genre = CharField()
    country = CharField()


def create_models():
    """Функция создающая таблицы (если таблицы уже есть, они не будут созданы заново)"""
    with db:
        tables = [User, History, QueryResult, FilterData]
        db.create_tables(tables)


if __name__ == "__main__":
    create_models()
