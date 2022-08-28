import telebot

from storage import db_session, DatabaseInterface
from clients import RabbitClient
from worker import WorkerMessageHandler
from config import TELEGRAM_TOKEN
from .content_enums import Command
from .content_generator import MessageGenerator


def create_bot():
    """Создает бота"""

    # Экземпляр бота
    bot = telebot.TeleBot(TELEGRAM_TOKEN)
    rabbitmq_client = RabbitClient(RabbitClient.DEFAULT_QUEUE)

    @bot.message_handler(commands=[Command.START.value])
    def send_welcome(message):
        """
        Обработка команды /start.

        Добавление данных о юзере в БД и вывод приветственных сообщений.
        """

        # Получаем айди и имя юзера
        user_id = message.from_user.id
        chat_id = message.chat.id
        user_name = message.from_user.first_name

        # Отправляем в базу айди и имя
        DatabaseInterface.add_new_tg_user(user_id, user_name, db_session)

        # Выводим сообщения
        bot.send_message(
            chat_id, MessageGenerator.get_hello_msg(user_name), parse_mode="Markdown"
        )

        bot.send_message(
            chat_id, MessageGenerator.get_tutorial_msg(), parse_mode="Markdown"
        )

    @bot.message_handler(content_types="text")
    def message_reply(message):
        """Обработка кнопок, которые отправляют текстовые сообщения"""

        broker_msg = (
            message.text
            + WorkerMessageHandler.MESSAGE_DATA_SEP
            + str(message.from_user.id)
        )

        # Выводим сообщения
        bot.send_message(
            message.chat.id, MessageGenerator.get_wait_msg(), parse_mode="Markdown"
        )

        # Отправляем сообщение брокеру
        rabbitmq_client.publish(broker_msg, RabbitClient.DEFAULT_QUEUE)

    bot.infinity_polling()
