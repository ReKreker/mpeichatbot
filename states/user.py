from aiogram.fsm.state import State, StatesGroup


class Event(StatesGroup):
    generated = State()
    getting_proofs = State()
    next_proof = State()
    forwarded = State()


class Practice(StatesGroup):
    generated = State()
    getting_proofs = State()
    next_proof = State()
    forwarded = State()
