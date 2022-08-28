from datetime import datetime, date
from clients.vk_api import VkApiClient


def get_groups_data(group_name: str) -> dict:
    """
    Обращение к VK API для получения всех данных о группе и обработка этих данных.

    :param group_name: Короткий идентификатор группы в адресной строке.
    """
    group_data = dict()

    # Получаем истинное количество подписчиков, идентификатор и имя в адресной строке
    (
        group_data["members_num"],  # int
        group_data["true_group_id"],  # int
        group_data["title"],  # str
    ) = VkApiClient.get_members_number(group_name)

    if group_data["members_num"] == "error":
        return {"error": "error"}

    # Генерируем словарь с данными о подписчиках
    # {'id': int, 'bdate': 'DD.MM.YYYY', 'sex': int, 'first_name': str, 'last_name': str}
    group_data["members_lst"] = VkApiClient.get_total_members_list(group_name)

    # Сохраняем число мужчин и женщин
    group_data["total_men"] = UsersListHandler.get_members_number_by_sex(
        group_data["members_lst"], 2
    )

    group_data["total_women"] = UsersListHandler.get_members_number_by_sex(
        group_data["members_lst"], 1
    )

    # Сохраняем общее число людей с возрастом
    group_data["total_users_with_age"] = UsersListHandler.get_number_of_users_with_age(
        group_data["members_lst"]
    )

    # Получаем словари {возраст: число людей} для:
    # Всех подписчиков
    group_data["all_ages_dict"] = UsersListHandler.get_dict_of_users_age(
        group_data["members_lst"]
    )

    # Всех мужчин
    group_data["men_ages_dict"] = UsersListHandler.get_users_age_dict_by_sex(
        group_data["members_lst"], 2
    )

    # Всех женщин
    group_data["women_ages_dict"] = UsersListHandler.get_users_age_dict_by_sex(
        group_data["members_lst"], 1
    )

    # Получаем общее число мужчин с возрастом
    group_data["total_men_with_age"] = UsersListHandler.get_total_number_in_age_dict(
        group_data["men_ages_dict"]
    )

    # Получаем общее число женщин с возрастом
    group_data["total_women_with_age"] = UsersListHandler.get_total_number_in_age_dict(
        group_data["women_ages_dict"]
    )

    return group_data


class UsersListHandler:
    @staticmethod
    def get_members_number_by_sex(data: list, sex: int) -> int:
        """
        :param data: список словарей с данными о пользователях.
        :param sex: число, обозначающее пол (1 - женский, 2 - мужской).
        :return: int - число людей пола 'sex' в списке подписчиков.
        """
        if type(data) != list:
            return 0

        number = 0

        for user_dict in data:
            if user_dict["sex"] == sex:
                number += 1

        return number

    @staticmethod
    def __is_user_have_age(user_d: dict) -> bool:
        """
        :param user_d: словарь данных юзера.
        :return: True, если у юзера известна полная дата рождения, иначе - False.
        """
        if "bdate" in user_d:
            if user_d["bdate"].count(".") == 2:
                return True

        return False

    @classmethod
    def get_number_of_users_with_age(cls, users: list) -> int:
        """
        :param users: Список словарей с данными о пользователях.
        :return: Возвращает число подписчиков с полной датой рождения
        """
        if type(users) != list:
            return 0

        counter = 0

        for user_d in users:
            if cls.__is_user_have_age(user_d):
                counter = counter + 1

        return counter

    @classmethod
    def get_dict_of_users_age(cls, users: list) -> dict:
        """
        :param users: список словарей с данными о юзерах.
        :return: Словарь {возраст: количество людей в списке}.
        """
        res = dict()

        if type(users) != list:
            return res

        for user_d in users:
            if cls.__is_user_have_age(user_d):
                age = str(cls.get_users_age(user_d["bdate"]))
                res[age] = res.get(age, 0) + 1

        res = dict(sorted(res.items()))
        return res

    @classmethod
    def get_users_age_dict_by_sex(cls, users: list, sex: int) -> dict:
        """
        :param users: Список словарей с данными о юзерах.
        :param sex: Число для обозначения пола (1 - женский, 2 - мужской).
        :return: Возвращает словарь {возраст: количество людей в списке}.
        """
        res = dict()

        if type(users) != list:
            return res

        for user_d in users:
            if cls.__is_user_have_age(user_d) and user_d["sex"] == sex:
                age = str(cls.get_users_age(user_d["bdate"]))
                res[str(age)] = res.get(age, 0) + 1

        res = dict(sorted(res.items()))
        return res

    @staticmethod
    def get_users_age(bd: str) -> int:
        """
        :param bd: Строка формата DD.MM.YYYY
        :return: Число полных лет юзера
        """

        bd = bd.split(".")
        users_bd = date(int(bd[2]), int(bd[1]), int(bd[0]))
        now = datetime.today().date()
        diff = now - users_bd

        return diff.days // 365

    @staticmethod
    def get_total_number_in_age_dict(
        age_dict: dict, lower_limit: int = 0, upper_limit: int = 999
    ) -> int:
        """
        :param age_dict: Словарь в формате {Возраст: число людей}.
        :param lower_limit: Нижний порог, от которого будут подсчитываться люди (не включительно).
        :param upper_limit: Верхний порог, до которого будут подсчитываться люди (не включительно).
        :return: Число людей с возрастом в диапазоне [lower_limit, upper_limit]
        """
        if type(age_dict) != dict:
            return 0

        if lower_limit == 0 and upper_limit == 999:
            return sum(age_dict.values())

        res = 0
        for age in age_dict:
            if lower_limit < age < upper_limit:
                res = res + age_dict[age]

        return res

    @staticmethod
    def filter_age_dict(
        users_age_data: dict, lower_limit: int = 0, upper_limit: int = 999
    ) -> dict:
        res = dict()

        for age in users_age_data:
            if lower_limit < int(age) < upper_limit:
                res[int(age)] = users_age_data[age]

        els = list(res.items())
        min_key = els[0]
        max_key = els[-1]

        for age in range(min_key[0], max_key[0]):
            res.setdefault(age, 0)

        res = dict(sorted(res.items()))
        return res
