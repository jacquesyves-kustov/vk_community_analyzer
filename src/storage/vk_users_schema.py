from sqlalchemy.orm import relationship
from sqlalchemy import Column, Text, Integer, ForeignKey
from .create_tables import Base


class VkUsers(Base):
    __tablename__ = "vk_users"

    __tableargs__ = {"comment": "Таблица уникальных юзеров ВК в БД"}

    true_user_id = Column(Text, primary_key=True)

    vk_users_general_data = relationship("VkUsersGeneralData", backref="users_true_id")
    vk_users_following_groups = relationship(
        "VkUsersFollowingGroups", backref="true_id"
    )

    def __repr__(self):
        return f"USER TRUE ID: {self.true_user_id}"


class VkUsersGeneralData(Base):
    __tablename__ = "vk_users_general_data"

    __tableargs__ = {"comment": "Таблица основной информации о юзерах ВК"}

    true_user_id = Column(Text, ForeignKey("vk_users.true_user_id"), primary_key=True)

    bdate = Column(Text, nullable=True)

    sex = Column(Integer, nullable=True)

    first_name = Column(Text, nullable=False)

    last_name = Column(Text, nullable=False)


class VkUsersFollowingGroups(Base):
    __tablename__ = "vk_users_following_groups"

    __tableargs__ = {"comment": "Таблица подписок юзеров ВК с учетом версий"}

    version_marker = Column(
        Integer, ForeignKey("versions.version_marker"), primary_key=True
    )

    true_user_id = Column(Text, ForeignKey("vk_users.true_user_id"), primary_key=True)

    true_group_id = Column(
        Text, ForeignKey("vk_unique_groups.true_group_id"), primary_key=True
    )
