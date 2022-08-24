import sqlalchemy.orm.session
from sqlalchemy.exc import IntegrityError
from .versions_schema import Versions
from .vk_users_schema import VkUsers, VkUsersGeneralData, VkUsersFollowingGroups
from .vk_groups_schema import VkUniqueGroups, VkGroupsGeneralData, VkGroupsAgeData
from data_fetcher import get_groups_data


class DataCollector:
    DATA_VERSION = 0

    @classmethod
    def __increase_data_version(cls) -> None:
        """
        Перед каждым регулярным обновлением, изменяется значение для версии данных
        """

        cls.DATA_VERSION += 1

    @classmethod
    def create_default_version_marker(cls, session: sqlalchemy.orm.Session) -> None:
        """
        Создает первую строчку в таблице версий. Вызывать после
        """

        first_version_marker = Versions(version_marker=cls.DATA_VERSION)
        session.add(first_version_marker)
        session.commit()

    @classmethod
    def create_new_groups_data_rows(
        cls, group_screen_name: str, new_group_data: dict
    ) -> VkUniqueGroups:
        """
        Создает новые строки в таблицы VkUsers, VkUsersGeneralData, VkUsersFollowingGroups

        :param group_screen_name:
        :param new_group_data: {'id': 7293143, 'bdate': '28.8.1975', 'sex': 2, 'first_name': 'Андрей', 'last_name': 'Галь'}
        :return:
        """

        # Создаем новый объект для таблицы уникальных групп
        new_group = VkUniqueGroups(true_group_id=new_group_data["true_group_id"])

        # Создаем новый объект для таблицы основных данных
        new_group_general_data = VkGroupsGeneralData(
            version_marker=cls.DATA_VERSION,
            title=new_group_data["title"],
            screen_name=group_screen_name,
            actual_members_count=new_group_data["members_num"],
            processed_members_count=len(new_group_data["members_lst"]),
            total_men=new_group_data["total_men"],
            total_women=new_group_data["total_women"],
        )

        # Создаем новый объект для таблицы данных о возрасте
        new_group_age_data = VkGroupsAgeData(
            version_marker=cls.DATA_VERSION,
            total_users_with_age=new_group_data["total_users_with_age"],
            all_ages_dict=str(new_group_data["all_ages_dict"]),
            men_ages_dict=str(new_group_data["men_ages_dict"]),
            women_ages_dict=str(new_group_data["women_ages_dict"]),
            total_men_with_ages=new_group_data["total_men_with_age"],
            total_women_with_ages=new_group_data["total_women_with_age"],
        )

        new_group.groups_general_data.append(new_group_general_data)
        new_group.groups_age_data.append(new_group_age_data)

        return new_group

    @classmethod
    def create_new_vk_user_data_rows(cls, user_d: dict, true_group_id: str) -> VkUsers:
        """
        Создает новые строки в таблицы VkUsers, VkUsersGeneralData, VkUsersFollowingGroups

        :param user_d: {'id': 7293143, 'bdate': '28.8.1975', 'sex': 2, 'first_name': 'Андрей', 'last_name': 'Галь'}
        :param true_group_id:
        :return:
        """

        new_user = VkUsers(true_user_id=user_d["id"])

        new_user_general_data = VkUsersGeneralData(
            bdate=user_d["bdate"],
            sex=user_d["sex"],
            first_name=user_d["first_name"],
            last_name=user_d["last_name"],
        )

        new_user_following_group = VkUsersFollowingGroups(
            version_marker=cls.DATA_VERSION,
            true_user_id=str(user_d["id"]),
            true_group_id=true_group_id,
        )

        new_user.vk_users_general_data.append(new_user_general_data)
        new_user.vk_users_following_groups.append(new_user_following_group)

        return new_user

    @classmethod
    def add_new_group(cls, group_name, session: sqlalchemy.orm.Session) -> None:
        """
        Функция, которая добавляет в таблицы данные о группе
        Версия данных будет совпадать с актуальной.
        """

        new_group_data = get_groups_data(group_name)
        new_group = cls.create_new_groups_data_rows(group_name, new_group_data)

        session.add(new_group)

        # Создаем новые строки в таблицах юзеров
        for user_d in new_group_data["members_lst"]:
            if bool(
                session.query(VkUsers)
                .filter(VkUsers.true_user_id == str(user_d["id"]))
                .first()
            ):
                continue

            new_user = cls.create_new_vk_user_data_rows(
                user_d, new_group_data["true_group_id"]
            )
            session.add(new_user)

        try:
            session.commit()

        except IntegrityError:
            session.rollback()

    @classmethod
    def update_groups_data(cls):
        # Увеличь счетчик версий.
        cls.__increase_data_version()

        # Для каждой группы в таблице уникальных групп:
        #   Добавь данные о группе с версией.

    @staticmethod
    def __update_group_data() -> None:
        pass

    @staticmethod
    def get_all_groups_ids_list(session: sqlalchemy.orm.Session):
        res = list()

        return res

    @staticmethod
    def get_users_intersection(*args, session: sqlalchemy.orm.Session):
        pass
