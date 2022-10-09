import os
from typing import Union
from enum import Enum

from requests import post

from data_processing import PostsHandler, get_related_publics
from config import TELEGRAM_TOKEN
from .report_text import ReportGenerator
from .report_plots import PlotsGenerator
from storage import db_session, DatabaseInterface


class Tasks(Enum):
    AUDIENCE_ANALYZE = 'audience_analyze'
    GET_ATTACHED_ARTISTS_IN_PUBLIC = 'get_attached_artists'
    GET_RELATED_PUBLICS = 'get_related_publics'


class WorkerMessageHandler:
    MESSAGE_DATA_SEP = "%"

    # TODO: Сделай клиент тг апи!
    @staticmethod
    def send_message(message_text: str, tg_user_id: Union[str, int]):
        messages = []
        while len(message_text) > 3_999:
            messages.append(message_text[:3999])
            message_text = message_text[3999:]

        messages.append(message_text)

        for msg in messages:
            send_message_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?"
            send_message_url += (
                f"chat_id={str(tg_user_id)}&text={msg}"
            )

            post(send_message_url)

    @staticmethod
    def send_plot(tg_user_id: str, img_name):
        img = open(img_name, "rb")
        send_photo_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto?chat_id={tg_user_id}"

        post(send_photo_url, files={"photo": img})
        img.close()

    @classmethod
    def process_audience_analyze_task(cls, group_screen_name, tg_user_chat_id) -> None:
        # Флаг существования такой группы
        is_added = True

        # Если группы нет в БД - парсим данные о ней
        if not DatabaseInterface.is_group_in_database(group_screen_name, db_session):
            is_added = DatabaseInterface.add_new_group(group_screen_name, db_session)

        if is_added:
            group_data = DatabaseInterface.get_groups_data(
                group_screen_name, db_session
            )

            message = ReportGenerator.get_report_text(group_data)
            plot_file_name = PlotsGenerator.two_plots_in_one(
                group_data["title"],
                group_data["men_ages_dict"],
                group_data["women_ages_dict"],
                tg_user_chat_id,
            )
        else:
            message = ReportGenerator.get_error_message(group_screen_name)

        cls.send_message(message, tg_user_chat_id)

        if is_added:
            cls.send_plot(tg_user_chat_id, plot_file_name)
            os.remove(plot_file_name)

    @classmethod
    def process_attached_artists_task(cls, data_to_process: str, tg_user_chat_id: Union[str, int]) -> None:
        artists_attach_dict = PostsHandler.count_artists_attachments_in_public(data_to_process, 30)

        # TODO: перенести в енум?
        if not artists_attach_dict:
            message_text = f'В постах vk.com/{data_to_process} нет прикрепленных песен.'

        else:
            # TODO: склонение слова "постов"?
            message_text = f'В паблике vk.com/{data_to_process} слушают:\n'

            for artist in artists_attach_dict:
                message_text += f'{artist}: {artists_attach_dict[artist]} постов\n'

        cls.send_message(message_text[:-1], str(tg_user_chat_id))

    @classmethod
    def process_get_related_publics_task(cls, public_name: str, tg_user_chat_id: Union[str, int]):
        found_groups = get_related_publics(public_name)

        # define higher values
        sorted_values = sorted(found_groups.values())
        sorted_values.reverse()

        if len(sorted_values) > 10:
            sorted_values = sorted_values[:10]

        message_text = f'У паблика vk.com/{public_name} общие подписчики с:\n'
        for popular_group in found_groups:
            if found_groups[popular_group] in sorted_values:
                message_text += f'vk.com/public{popular_group}: общих {found_groups[popular_group]} участников.\n'

        cls.send_message(message_text, str(tg_user_chat_id))

    @classmethod
    def worker_message_handler(cls, message_body: str) -> None:
        """
        Логика обработки сообщений из брокера.
        """
        task, data_to_process, tg_user_chat_id = message_body.split(cls.MESSAGE_DATA_SEP)

        # В зависимости от задачи выбирается обработчик
        if task == Tasks.AUDIENCE_ANALYZE.value:
            cls.process_audience_analyze_task(data_to_process, tg_user_chat_id)

        elif task == Tasks.GET_ATTACHED_ARTISTS_IN_PUBLIC.value:
            cls.process_attached_artists_task(data_to_process, tg_user_chat_id)

        elif task == Tasks.GET_RELATED_PUBLICS.value:
            cls.process_get_related_publics_task(data_to_process, tg_user_chat_id)
