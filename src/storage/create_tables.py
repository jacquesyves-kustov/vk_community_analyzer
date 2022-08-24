from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from config import POSTGRES_CONNECTION_STR


Base = declarative_base()


def create_database() -> None:
    """
    Функция, которая инициализирует все таблицы
    """

    db_engine = create_engine(POSTGRES_CONNECTION_STR, echo=False)
    Base.metadata.create_all(db_engine)


def get_database_session() -> Session:
    """
    :return: Объект БД-сессии.
    """

    db_engine = create_engine(POSTGRES_CONNECTION_STR, echo=True)
    session = Session(db_engine, future=True)

    return session


db_session = get_database_session()
