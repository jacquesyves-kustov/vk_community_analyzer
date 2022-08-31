from datetime import datetime

from clients import VkApiClient


class PostsHandler:
    @staticmethod
    def get_set_of_artists_from_posts_att(post: dict) -> set:
        artists_set = set()

        for el in post["attachments"]:  # Для каждого прикрепленного файла
            if el["type"] == "audio":  # Если прикрепленный файл - аудио
                # Проверка на то, сколько артистов закреплены за песней
                # Если их несколько, то нужно провалиться в 'main_artists'
                if "main_artists" in el["audio"]:
                    for ar in el["audio"]["main_artists"]:
                        artists_set.add(ar["name"])

                else:
                    artists_set.add(el["audio"]["artist"])

        return artists_set

    @classmethod
    def count_artists_mentions(cls, public_screen_name: str, days_limit: int) -> dict:
        """
        Подсчитывает количество прикреплений песен артистов к постам в паблике.

        :param public_screen_name: Короткий идентификатор сообщества в адресной строке.
        :param days_limit: Количество дней, за которые надо посчитать количество упоминаний.

        :return: Словарь {'artist': число уникальных постов с прикреплением песни}.
        """
        today = datetime.today()
        diff = 0
        offset = 0

        artists_d = dict()

        while diff < days_limit:
            data = VkApiClient.send_get_request(
                VkApiClient.VK_WALL_GET,
                domain=public_screen_name,
                count=100,
                offset=offset,
            )
            offset += 100

            data = (
                data.json()
            )  # {'response': {'count': 2, 'items': [{'id': 1, ...}, {'id': 2, ...}]}}
            data = data["response"]
            data = data["items"]

            if not data:  # Если список постов пуст, то выходим из цикла
                break

            for post in data:
                if "attachments" not in post:
                    continue

                # Определяем разницу в сутках между текущим днем и днем публикации
                post_time = datetime.utcfromtimestamp(post["date"])
                diff = today - post_time
                diff = diff.days

                # Если дата публикации поста выходит за данный лимит, то выходим из вложенного цикла
                if diff >= days_limit:
                    break

                # Получаем set артистов, чьи песни были прикреплены к посту
                artists_set = cls.get_set_of_artists_from_posts_att(post)

                for artist in artists_set:
                    artists_d[artist] = artists_d.get(artist, 0) + 1

        artists_d = dict(sorted(artists_d.items(), key=lambda item: item[1]))

        return artists_d
