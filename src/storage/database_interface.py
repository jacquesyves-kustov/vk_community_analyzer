from json import loads

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert

from data_processing import get_groups_data
from data_processing import UsersListHandler
from .vk_users_schema import VkUsersGeneralData, VkUsersFollowingGroups
from .vk_groups_schema import VkGroupsAgeData, VkGroupsGeneralData
from .tg_users_schema import TgUsers


class DatabaseInterface:
    LOWER_AGE_LIMIT = 0
    UPPER_AGE_LIMIT = 50

    @staticmethod
    def add_new_tg_user(user_tg_id: int, user_tg_first_name: str, session: Session):
        new_tg_user = TgUsers(
            tg_user_id=user_tg_id, tg_user_first_name=user_tg_first_name
        )

        session.add(new_tg_user)

        try:
            session.commit()
        except IntegrityError:
            session.rollback()

    @staticmethod
    def __create_new_groups_data_rows(
        group_screen_name: str, new_group_data: dict
    ) -> VkGroupsGeneralData:
        """
        Создает новые строки в таблицы VkUsersGeneralData, VkUsersFollowingGroups.

        :param group_screen_name:
        :param new_group_data:
        :return:
        """
        new_group = VkGroupsGeneralData(
            true_group_id=new_group_data["true_group_id"],
            title=new_group_data["title"],
            screen_name=group_screen_name,
            actual_members_count=new_group_data["members_num"],
            processed_members_count=len(new_group_data["members_lst"]),
            total_men=new_group_data["total_men"],
            total_women=new_group_data["total_women"],
        )

        new_group_age_data = VkGroupsAgeData(
            total_users_with_age=new_group_data["total_users_with_age"],
            all_ages_dict=str(new_group_data["all_ages_dict"]),
            men_ages_dict=str(new_group_data["men_ages_dict"]),
            women_ages_dict=str(new_group_data["women_ages_dict"]),
            total_men_with_ages=new_group_data["total_men_with_age"],
            total_women_with_ages=new_group_data["total_women_with_age"],
        )

        new_group.groups_age_data.append(new_group_age_data)

        return new_group

    @classmethod
    def add_new_group(cls, group_name, session: Session) -> bool:
        """
        Функция, которая добавляет в таблицы данные о группе
        Версия данных будет совпадать с актуальной.
        """
        print(f" >>> {group_name} is being added!")

        # Получаем словарь всех данных о паблике
        new_group_data = get_groups_data(group_name)

        if "error" in new_group_data:
            return False

        # Добавляем новую группу
        new_group = cls.__create_new_groups_data_rows(group_name, new_group_data)
        session.add(new_group)

        try:
            session.commit()
        except IntegrityError:
            session.rollback()

        # Добавляем новых юзеров
        # {'true_user_id': int, 'bdate': 'DD.MM.YYYY', 'sex': int, 'first_name': str, 'last_name': str}
        stmt = insert(VkUsersGeneralData).values(new_group_data["members_lst"])
        stmt = stmt.on_conflict_do_nothing(index_elements=["true_user_id"])
        session.execute(stmt)

        #
        following_groups_data = [
            {
                "true_group_id": new_group_data["true_group_id"],
                "true_user_id": user_d["true_user_id"],
            }
            for user_d in new_group_data["members_lst"]
        ]
        # Добавляем данные о подписках
        stmt = insert(VkUsersFollowingGroups).values(following_groups_data)
        stmt = stmt.on_conflict_do_nothing(
            index_elements=["true_user_id", "true_group_id"]
        )
        session.execute(stmt)

        print(f" >>> {group_name} has been added!")
        return True

    @classmethod
    def get_groups_data(cls, short_name: str, session: Session) -> dict:
        """
        Запрос данных о группе из БД.

        :param short_name: Короткий идентификатор группы в адресной строке.
        :param session: Подключение к БД.
        :return: Словарь с данными о группе.
        """
        q = (
            session.query(VkGroupsGeneralData, VkGroupsAgeData)
            .join(VkGroupsAgeData)
            .filter(VkGroupsGeneralData.screen_name == short_name)
            .first()
        )

        res_d = dict()

        if q is None:
            res_d["error"] = "error"
            return res_d

        res_d["title"] = q[0].title
        res_d["screen_name"] = q[0].screen_name
        res_d["actual_members_count"] = q[0].actual_members_count
        res_d["processed_members_count"] = q[0].processed_members_count
        res_d["total_men"] = q[0].total_men
        res_d["total_women"] = q[0].total_women
        res_d["total_users_with_age"] = q[1].total_users_with_age
        res_d["total_men_with_ages"] = q[1].total_men_with_ages
        res_d["total_women_with_ages"] = q[1].total_women_with_ages

        # Словари сохранены в бд в виде строки '{"42": 123}'
        res_d["all_ages_dict"] = loads(q[1].all_ages_dict.replace("'", '"'))
        res_d["all_ages_dict"] = UsersListHandler.filter_age_dict(
            res_d["all_ages_dict"], cls.LOWER_AGE_LIMIT, cls.UPPER_AGE_LIMIT
        )

        res_d["men_ages_dict"] = loads(q[1].men_ages_dict.replace("'", '"'))
        res_d["men_ages_dict"] = UsersListHandler.filter_age_dict(
            res_d["men_ages_dict"], cls.LOWER_AGE_LIMIT, cls.UPPER_AGE_LIMIT
        )

        res_d["women_ages_dict"] = loads(q[1].women_ages_dict.replace("'", '"'))
        res_d["women_ages_dict"] = UsersListHandler.filter_age_dict(
            res_d["women_ages_dict"], cls.LOWER_AGE_LIMIT, cls.UPPER_AGE_LIMIT
        )

        return res_d

    @staticmethod
    def is_group_in_database(group_screen_name: str, session: Session) -> bool:
        """
        Проверяем, находится ли передаваемое слово в таблице уникальных слов

        :return: True, если данные о группе уже занесены в БД.
        """
        result = (
            session.query(VkGroupsGeneralData)
            .filter(VkGroupsGeneralData.screen_name == group_screen_name)
            .first()
        )

        return result is not None
