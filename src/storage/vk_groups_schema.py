from sqlalchemy.orm import relationship
from sqlalchemy import Column, Text, Integer, BigInteger, ForeignKey

from .create_tables import Base


class VkGroups(Base):
    __tablename__ = "vk_groups"

    __tableargs__ = {
        "comment": "Таблица основных данных о группах, привязанных к моменту обновления"
    }

    true_group_id = Column(
        BigInteger,
        primary_key=True,
        unique=True,
        comment="Настоящий id группы, состоящий из цифр",
    )

    groups_data = relationship("VkGroupsGeneralData", backref="group_true_id")
    groups_followers = relationship("VkUsersFollowingGroups", backref="group_id")


class VkGroupsGeneralData(Base):
    __tablename__ = "vk_groups_data"

    __tableargs__ = {
        "comment": "Таблица основных данных о группах, привязанных к моменту обновления"
    }

    version_marker = Column(
        Integer, ForeignKey("versions.version_marker"), primary_key=True
    )

    true_group_id = Column(
        BigInteger, ForeignKey("vk_groups.true_group_id"), primary_key=True
    )

    title = Column(Text, nullable=False, comment="Название группы")

    screen_name = Column(
        Text, nullable=False, comment="Короткое имя сообщества в адресной строке"
    )

    actual_members_count = Column(
        Integer, nullable=False, comment="Настоящее количество подписчиков"
    )

    processed_members_count = Column(
        Integer,
        nullable=False,
        comment="Количество подписчиков, обработанных через API",
    )

    total_men = Column(
        Integer, nullable=False, comment="Всего мужчин среди подписчиков"
    )

    total_women = Column(
        Integer, nullable=False, comment="Всего женщин среди подписчиков"
    )

    total_users_with_age = Column(
        Integer,
        nullable=False,
        comment="Всего пользователей с полным возрастом, обработанных через API",
    )

    all_ages_dict = Column(
        Text,
        nullable=False,
        comment="Словарь {age: num}, где age - определенный возраст, а num - число подписчиков данного возраста",
    )

    men_ages_dict = Column(
        Text,
        nullable=False,
        comment="Словарь {age: num}, где age - определенный возраст, а num - число подписчиков-мужчин данного возраста",
    )

    women_ages_dict = Column(
        Text,
        nullable=False,
        comment="Словарь {age: num}, где age - определенный возраст, а num - число подписчиков-женщин данного возраста",
    )

    total_men_with_ages = Column(
        Integer, nullable=False, comment="Всего мужчин с указанным полным возрастом"
    )

    total_women_with_ages = Column(
        Integer, nullable=False, comment="Всего женщин с указанным полным возрастом"
    )
