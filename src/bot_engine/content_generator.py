from random import choice

from .content_enums import Smiles, Message, WAIT_MESSAGES


class MessageGenerator:
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
