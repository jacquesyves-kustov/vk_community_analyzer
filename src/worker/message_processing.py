import os

from requests import post

from config import TELEGRAM_TOKEN
from .report_text import ReportGenerator
from .report_plots import PlotsGenerator
from storage import db_session, DatabaseInterface


class WorkerMessageHandler:
    MESSAGE_DATA_SEP = "%"

    @staticmethod
    def send_message(message_text: str, tg_user_id: str):
        # Заполняем строку запроса
        send_message_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?"
        send_message_url += (
            f"chat_id={tg_user_id}&text={message_text}&parse_mode=markdown"
        )

        # Отправляем запрос
        post(send_message_url)

    @staticmethod
    def send_plot(tg_user_id: str, img_name):
        img = open(img_name, "rb")
        send_photo_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto?chat_id={tg_user_id}"

        post(send_photo_url, files={"photo": img})
        img.close()

    @classmethod
    def worker_message_handler(cls, message_body: str) -> None:
        """Логика обработки сообщений из парсера"""

        # Флаг существования такой группы
        is_added = True

        # Сплитим сообщение, чтобы получить интересующую группу и айди запросившего юзера
        group_screen_name, tg_user_chat_id = message_body.split(cls.MESSAGE_DATA_SEP)

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
