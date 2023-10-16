from aiogram.fsm.state import State, StatesGroup


class Practice(StatesGroup):
    to_upload = State()
    forwarded = State()


class Event(StatesGroup):
    to_upload = State()
    forwarded = State()
