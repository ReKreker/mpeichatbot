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

    await db.connect()
    info = await get_undone_x(db, msg.from_user.id)
    await db.disconnect()

    data = info["data"]
    if len(data) == 0:
        await msg.answer(info["msg"])
        await state.clear()
        return

    button = types.InlineKeyboardButton
    kb = InlineKeyboardBuilder()
    for x_id, name in data:
        data_button = ButtonCbFactory(id=x_id)
        kb.add(button(text=name, callback_data=data_button.pack()))
    kb.adjust(1)

    await msg.reply("Выбери, какую сдать практику:", reply_markup=kb.as_markup())
    await state.set_state(Practice.generated)


async def require_proofs(query: types.CallbackQuery, state: FSMContext, bot: Bot) -> bool:
    await query.message.delete()
    data = ButtonCbFactory.unpack(query.data)

    await db.connect()
    row = await db.get_x_by_id(data.id)
    await db.disconnect()
    name, descr = row[0].values()
    m = [
        f"<b>{name}</b>",
        f"<i>{descr}</i>",
        "",
        "Вышли практику в виде картинок, видео или файла (предпочительно docx/pdf, но можно и zip)",
        "<b>Отправь любое сообщение, чтобы завершить передачу</b>"
    ]
    await query.message.answer("\n".join(m))
    await state.set_data({"id": data.id, "db": db, "group": Practice, "cb_factory": PractCbFactory})
    await state.set_state(Practice.getting_proofs)
    return await bot.answer_callback_query(callback_query_id=query.id)
