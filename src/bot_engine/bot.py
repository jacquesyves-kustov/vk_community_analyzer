import telebot

from storage import db_session, DatabaseInterface
from clients import RabbitClient
from worker import WorkerMessageHandler
from config import TELEGRAM_TOKEN
from .content_enums import Command, CALLBACK_DATA_SEP
from .content_generator import MessageGenerator


def create_bot():
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
            chat_id,
            MessageGenerator.get_hello_msg(user_name),
            parse_mode="Markdown"
        )

        bot.send_message(
            chat_id,
            MessageGenerator.get_tutorial_msg(),
            parse_mode="Markdown"
        )

    @bot.message_handler(content_types="text")
    def message_reply(message):
        """Обработка кнопок, которые отправляют текстовые сообщения"""

        # Выводим сообщения
        bot.send_message(
            message.chat.id,
            MessageGenerator.get_default_answer(message.text),
            reply_markup=MessageGenerator.get_default_inline_buttons(message.text, str(message.chat.id))
        )

    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler(call):
        """
        Обработка inline кнопок.
        call.data.split(callback_data_sep)[0] - команда.
        call.data.split(callback_data_sep)[1] - данные для передачи хэндлеру.
        call.data.split(callback_data_sep)[2] - user_id.
        ...
        """

        workers_task, data_to_process, user_id = call.data.split(CALLBACK_DATA_SEP)

        broker_msg = (
            workers_task
            + WorkerMessageHandler.MESSAGE_DATA_SEP
            + data_to_process
            + WorkerMessageHandler.MESSAGE_DATA_SEP
            + user_id
        )

        rabbitmq_client.publish(broker_msg, RabbitClient.DEFAULT_QUEUE)

        bot.send_message(
            call.message.chat.id,
            MessageGenerator.get_wait_msg(),
            parse_mode="Markdown"
        )

    bot.infinity_polling()
