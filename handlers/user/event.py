from aiogram import types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.cb_data import EventCbFactory, ButtonCbFactory
from data.database import Database
from states.user import Event
from utils.db_processing import get_undone_x

db = Database()


async def gen_menu(msg: types.Message, state: FSMContext) -> None:
    if msg.from_user is None:
        return
    await state.clear()

    await db.connect()
    events_data = await db.get_events()
    await db.disconnect()

    button = types.InlineKeyboardButton
    kb = InlineKeyboardBuilder()
    for identif, name in events_data:
        data_button = ButtonCbFactory(id=identif)
        kb.add(button(text=name, callback_data=data_button.pack()))
    kb.adjust(1)

    await msg.reply("Выбери, какое мероприятие сдать:", reply_markup=kb.as_markup())
    await state.set_state(Event.generated)


async def require_proofs(query: types.CallbackQuery, state: FSMContext, bot: Bot):
    await query.message.delete()
    await query.message.answer(
        "Вышли док-ва в виде картинок, видео или файла (предпочительно docx/pdf, но можно и zip).\n" + \
        "<b>Отправь любое сообщение, чтобы завершить передачу</b>"
    )

    data = ButtonCbFactory.unpack(query.data)
    await state.set_data({"id": data.id, "db": db, "group": Event, "cb_factory": EventCbFactory})
    await state.set_state(Event.getting_proofs)
    return await bot.answer_callback_query(callback_query_id=query.id)
