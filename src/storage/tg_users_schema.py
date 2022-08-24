from sqlalchemy import Column, Text, BigInteger

from .create_tables import Base


class TgUsers(Base):
    __tablename__ = "tg_users"

    __tableargs__ = {"comment": "Список идентификаторов уникальных юзеров приложения"}

    tg_user_id = Column(BigInteger, primary_key=True)

    tg_user_first_name = Column(Text, nullable=False)
