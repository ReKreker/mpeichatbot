from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.cb_data import PractCbFactory, ButtonCbFactory
from data.database import Database
from states.user import Practice
from utils.db_processing import get_undone_x

db = Database("practice")


async def gen_menu(msg: types.Message, state: FSMContext) -> None:
    if msg.from_user is None:
        return
    await state.clear()

    # TODO: извлекать из SQL названия всех практик(желательно от недавних до поздних)
    test_data = {1: "Практика 1", 2: "Практика 2", 3: "Практика 3"}
    button = types.InlineKeyboardButton
    kb = InlineKeyboardBuilder()
    for identif, name in test_data.items():
        data_button = ButtonCbFactory(id=identif)
        kb.add(button(text=name, callback_data=data_button.pack()))
    kb.adjust(1)

    await msg.reply("Выбери, какую сдать практику:", reply_markup=kb.as_markup())
    await state.set_state(Practice.generated)


async def require_proofs(query: types.CallbackQuery, state: FSMContext, bot: Bot):
    await query.message.delete()
    await query.message.answer(
        "Вышли практику в виде картинок, видео или файла (предпочительно docx/pdf, но можно и zip).\n" + \
        "<b>Отправь любое сообщение, чтобы завершить передачу</b>"
    )

    data = ButtonCbFactory.unpack(query.data)
    await state.set_data({"id": data.id, "db": db, "group": Practice, "cb_factory": PractCbFactory})
    await state.set_state(Practice.getting_proofs)
    return await bot.answer_callback_query(callback_query_id=query.id)
