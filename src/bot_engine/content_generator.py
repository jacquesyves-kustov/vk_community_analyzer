from random import choice

from telebot import types

from .content_enums import Smiles, Message, WAIT_MESSAGES, Buttons, CALLBACK_DATA_SEP
from worker import Tasks


class MessageGenerator:
    @staticmethod
    def get_default_inline_buttons(data: str, user_id: str):
        """
        Создает стандартный набор кнопок.
        """

        # TODO: добавить смайлики в кнопки?
        keyboard = types.InlineKeyboardMarkup()

        audience_analyze_btn = types.InlineKeyboardButton(
            Buttons.AUDIENCE_ANALYZE_INLINE.value,
            callback_data=Tasks.AUDIENCE_ANALYZE.value + CALLBACK_DATA_SEP + data + CALLBACK_DATA_SEP + user_id
        )

        attached_artists_btn = types.InlineKeyboardButton(
            Buttons.GET_ATTACHED_ARTIST.value,
            callback_data=Tasks.GET_ATTACHED_ARTISTS_IN_PUBLIC.value + CALLBACK_DATA_SEP + data + CALLBACK_DATA_SEP + user_id
        )

        related_publics_btn = types.InlineKeyboardButton(
            Buttons.GET_RELATED_PUBLIC.value,
            callback_data=Tasks.GET_RELATED_PUBLICS.value + CALLBACK_DATA_SEP + data + CALLBACK_DATA_SEP + user_id
        )

        keyboard.row(audience_analyze_btn)
        keyboard.row(attached_artists_btn)
        keyboard.row(related_publics_btn)

        return keyboard

    @staticmethod
    def get_default_answer(requested_name: str) -> str:
        return Message.DEFAULT_ANSWER.value.format(requested_name)

    @staticmethod
    def get_hello_msg(tg_user_first_name: str) -> str:
        return (
            Smiles.VICTORY_HAND.value
            + " "
            + Message.HELLO.value.format(tg_user_first_name)
        )

    @staticmethod
    def get_tutorial_msg() -> str:
        return Message.TUTORIAL.value

    @staticmethod
    def get_wait_msg() -> str:
        return choice(WAIT_MESSAGES)
