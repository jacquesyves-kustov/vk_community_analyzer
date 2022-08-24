from sqlalchemy.orm import relationship
from sqlalchemy import Column, Text, Integer, BigInteger, ForeignKey

from .create_tables import Base


class VkUsersGeneralData(Base):
    __tablename__ = "vk_users"
    __tableargs__ = {"comment": "Таблица основной информации о юзерах ВК"}

    true_user_id = Column(BigInteger, primary_key=True, unique=True)
    bdate = Column(Text, nullable=True)
    sex = Column(Integer, nullable=True)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)

    vk_users_following_groups = relationship(
        "VkUsersFollowingGroups", backref="true_id"
    )


class VkUsersFollowingGroups(Base):
    __tablename__ = "vk_users_following_groups"
    __tableargs__ = {"comment": "Таблица подписок юзеров ВК с учетом версий"}

    version_marker = Column(
        Integer, ForeignKey("versions.version_marker"), primary_key=True
    )
    true_user_id = Column(
        BigInteger, ForeignKey("vk_users.true_user_id"), primary_key=True
    )
    true_group_id = Column(
        BigInteger, ForeignKey("vk_groups.true_group_id"), primary_key=True
    )
