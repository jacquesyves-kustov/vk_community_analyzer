from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert

from data_processing import get_groups_data
from storage.vk_users_schema import VkUsersGeneralData, VkUsersFollowingGroups
from storage.vk_groups_schema import VkGroupsAgeData, VkGroupsGeneralData


class DataCollector:
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

        # Создаем новый объект для таблицы групп и основных данных о них
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
    def add_new_group(cls, group_name, session: Session) -> None:
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
