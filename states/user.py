from aiogram.fsm.state import State, StatesGroup


class Activity(StatesGroup):
    generated = State()
    getting_proofs = State()
    next_proof = State()
    forwarded = State()
