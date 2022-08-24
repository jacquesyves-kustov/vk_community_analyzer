import time

import requests
from requests import Response

from config import VK_TOKEN, VK_API_VER


class VkApiClient:
    VK_REQ_START = "https://api.vk.com/method/"
    VK_GROUP_GET_BY_ID = "groups.getById"
    VK_GROUP_GET_MEMBERS = "groups.getMembers"

    @classmethod
    def __send_get_request(cls, method: str, **kwargs) -> Response:
        """
        Метод для генерации запроса к VK API.

        :param method: Строка с методом VK API.
        :param **kwargs: Дополнительные параметры запроса.
        """

        payload = kwargs
        payload["access_token"] = VK_TOKEN
        payload["v"] = VK_API_VER

        r = requests.get(f"{cls.VK_REQ_START}{method}", params=payload)
        r.raise_for_status()

        return r

    @staticmethod
    def __sleep_decorator(func):
        """
        VK API позволяет делать до 3 запросов в секунду.
        """

        def wrapper(*args, **kwargs):
            time.sleep(0.1)

            try:
                res = func(*args, **kwargs)
                return res

            except Exception as e:
                print(e)

        return wrapper

    @classmethod
    @__sleep_decorator
    def get_members_number(cls, group_id: str) -> tuple:
        """
        Получение общей информации о группе.
        :return (число подписчиков, айди, заголовок группы).
        """

        # Отправляем запрос
        r = cls.__send_get_request(
            cls.VK_GROUP_GET_BY_ID, group_id=group_id, fields="members_count,name"
        )

        json = r.json()["response"][0]  # Структура ответа: {'response': [{data: data}]}
        print(
            f" {group_id}, {json['name']} ({json['id']}) количество подписчиков получено: {json['members_count']}"
        )

        return json["members_count"], json["id"], json["name"]

    @classmethod
    @__sleep_decorator
    def get_total_members_list(cls, group_id: str):
        """
        Получение полного списка подписчиков
        """

        # Создаем новый список, где будем хранить словари с данными о юзере
        members_d = []

        # Максимальная длина возвращаемого списка юзеров - 1000
        # Поэтому запрашиваем следующую тысячу каждую итерацию
        offset = 0

        while True:
            new_members = cls.get_members_sublist(group_id, offset)
            members_d += new_members
            offset += 1000

            if not new_members:
                break

            print(f" >>> {group_id}: {len(new_members)} подписчиков добавлено!")

        return members_d

    @classmethod
    @__sleep_decorator
    def get_members_sublist(cls, group_id: str, offset: int) -> list:
        """
        Возвращает список словарей, содержащих полезные данные о подписчике
        """

        # Отправляем запрос
        r = cls.__send_get_request(
            cls.VK_GROUP_GET_MEMBERS,
            group_id=group_id,
            fields="bdate,sex",
            offset=offset,
        )

        # Список словарей
        res_lst = []

        # Из получаемых данных сохраняем только id, дату рождения, пол, имя, фамилию
        for user_d in r.json()["response"]["items"]:
            new_user_d = dict()

            new_user_d["true_user_id"] = user_d["id"]
            new_user_d["bdate"] = user_d["bdate"] if "bdate" in user_d else "None"
            new_user_d["sex"] = user_d["sex"] if "sex" in user_d else 0
            new_user_d["first_name"] = user_d["first_name"]
            new_user_d["last_name"] = user_d["last_name"]

            res_lst.append(new_user_d)

        return res_lst
