from enum import IntEnum

from aiogram.filters.callback_data import CallbackData

__all__ = (
    "ButtonInfo",
    "ButtonCbFactory",
    "NeponCbFactory",
    "QuizCbFactory",
    "PractCbFactory",
    "EventCbFactory"
)


class ButtonInfo(IntEnum):
    NONE = 0
    NO = 1
    YES = 2
    NEXT = 3
    PREV = 4


class ButtonCbFactory(CallbackData, sep=";", prefix="kb_button"):
    id: int = -1
    button: ButtonInfo = ButtonInfo.NONE


# Events & tasks implementation

class NeponCbFactory(CallbackData, prefix="kb_nepon"):
    user_id: int
    reply_msg_id: int


class QuizCbFactory(CallbackData, prefix="kb_quiz"):
    user_id: int
    reply_msg_id: int
    button: str  # packed ButtonCbFactory


class PractCbFactory(CallbackData, prefix="kb_prac"):
    user_id: int
    reply_msg_id: int
    button: str  # packed ButtonCbFactory


class EventCbFactory(CallbackData, prefix="kb_event"):
    user_id: int
    reply_msg_id: int
    button: str  # packed ButtonCbFactory
