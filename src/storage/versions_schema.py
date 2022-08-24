from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer
from .create_tables import Base


class Versions(Base):
    __tablename__ = "versions"

    __tableargs__ = {"comment": "Таблица маркеров версий данных"}

    version_marker = Column(
        Integer, primary_key=True, comment="Число, обозначающее версию данных"
    )

    vk_group_general_data_version = relationship(
        "VkGroupsGeneralData", backref="vk_group_general_data_version_marker"
    )

    vk_group_age_data_version = relationship(
        "VkGroupsAgeData", backref="vk_group_age_data_version_marker"
    )

    vk_users_following_groups_data_version = relationship(
        "VkUsersFollowingGroups", backref="vk_users_following_groups_version_marker"
    )

    def __repr__(self):
        return f"MARKER: {self.version_marker}"
