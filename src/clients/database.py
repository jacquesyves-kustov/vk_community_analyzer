import sqlalchemy.orm.session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert

from data_processing import get_groups_data
from storage.data_versions_schema import Versions
from storage.vk_users_schema import VkUsersGeneralData, VkUsersFollowingGroups
from storage.vk_groups_schema import VkGroups, VkGroupsGeneralData


class DataCollector:
    DATA_VERSION = 0

    @classmethod
    def __increase_data_version(cls) -> None:
        """
        Перед каждым регулярным обновлением, изменяется значение для версии данных
        """
        # TODO: БЕРИ ПОСЛЕДНЮЮ ЗАПИСЬ ИЗ БД И УВЕЛИЧИВАЙ НА ЕДИНИЦУ!!!!

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
    ) -> VkGroupsGeneralData:
        """
        Создает новые строки в таблицы VkUsersGeneralData, VkUsersFollowingGroups.

        :param group_screen_name:
        :param new_group_data:
        :return:
        """

        new_group = VkGroups(true_group_id=new_group_data["true_group_id"])

        # Создаем новый объект для таблицы групп и основных данных о них
        new_group_data = VkGroupsGeneralData(
            version_marker=cls.DATA_VERSION,
            title=new_group_data["title"],
            screen_name=group_screen_name,
            actual_members_count=new_group_data["members_num"],
            processed_members_count=len(new_group_data["members_lst"]),
            total_men=new_group_data["total_men"],
            total_women=new_group_data["total_women"],
            total_users_with_age=new_group_data["total_users_with_age"],
            all_ages_dict=str(new_group_data["all_ages_dict"]),
            men_ages_dict=str(new_group_data["men_ages_dict"]),
            women_ages_dict=str(new_group_data["women_ages_dict"]),
            total_men_with_ages=new_group_data["total_men_with_age"],
            total_women_with_ages=new_group_data["total_women_with_age"],
        )

        new_group.groups_data.append(new_group_data)

        return new_group

    @classmethod
    def add_new_group(cls, group_name, session: sqlalchemy.orm.Session) -> None:
        """
        Функция, которая добавляет в таблицы данные о группе
        Версия данных будет совпадать с актуальной.
        """
        print(f" >>> {group_name} is being added!")

        # Получаем словарь всех данных о паблике
        new_group_data = get_groups_data(group_name)

        # Добавляем новую группу
        new_group = cls.create_new_groups_data_rows(group_name, new_group_data)
        session.add(new_group)
        session.commit()

        # Добавляем новых юзеров
        # {'true_user_id': int, 'bdate': 'DD.MM.YYYY', 'sex': int, 'first_name': str, 'last_name': str}
        stmt = insert(VkUsersGeneralData).values(new_group_data["members_lst"])
        stmt = stmt.on_conflict_do_nothing(index_elements=["true_user_id"])
        session.execute(stmt)

        # Добавляем данные о подписках
        user_following_groups_data = list()

        for user_d in new_group_data["members_lst"]:
            d = dict()
            d["version_marker"] = cls.DATA_VERSION
            d["true_user_id"] = str(user_d["true_user_id"])
            d["true_group_id"] = str(new_group_data["true_group_id"])
            user_following_groups_data.append(d)

        stmt = insert(VkUsersFollowingGroups).values(user_following_groups_data)
        stmt = stmt.on_conflict_do_nothing(
            index_elements=["version_marker", "true_user_id", "true_group_id"]
        )
        session.execute(stmt)

        print(f" >>> {group_name} has been added!")

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
