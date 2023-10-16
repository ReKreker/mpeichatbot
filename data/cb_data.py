from aiogram.filters.callback_data import CallbackData


class NeponCbFactory(CallbackData, prefix="kb_nepon"):
    user_id: int
    reply_msg_id: int


class QuizCbFactory(CallbackData, prefix="kb_quiz"):
    user_id: int
    reply_msg_id: int
    is_yes: bool


class PractListCbFactory(CallbackData, prefix="kb_prac_list"):
    user_id: int
    reply_msg_id: int
    name: str


class PractChooseCbFactory(CallbackData, prefix="kb_prac_choose"):
    user_id: int
    reply_msg_id: int
    is_yes: bool


class EventListCbFactory(CallbackData, prefix="kb_prac_list"):
    user_id: int
    reply_msg_id: int
    name: str


class EventChooseCbFactory(CallbackData, prefix="kb_prac_choose"):
    user_id: int
    reply_msg_id: int
    is_yes: bool
