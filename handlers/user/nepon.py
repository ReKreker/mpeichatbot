from aiogram import Bot
from aiogram import html, types
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data import config
from data.cb_data import NeponCbFactory, ButtonInfo
from data.database import Database
from utils.keyboards import BuildKb

db = Database()


async def gen_menu(msg: types.Message, bot: Bot) -> None:
    if msg.from_user is None:
        return
    if msg.text.strip() == "/nepon":
        nepon_without_term = FSInputFile("memes/nepon_without_term.png")
        await msg.reply_photo(nepon_without_term)
        return

    await msg.reply("Отправлено спикеру!")

    m = [
        f"От <a href='{msg.from_user.url}'>{html.quote(msg.from_user.full_name)}</a> пришёл nepon:",
        msg.text[6:].strip()
    ]

    # таймаут на 24 часа на отображение кнопки одобрения для запросов от конкретного юзера
    await db.connect()
    recent = await db.execute_query("SELECT * FROM nepon WHERE time >= CURRENT_TIMESTAMP - INTERVAL '24 hours'")
    await db.disconnect()

    if len(recent) == 0:
        kb = InlineKeyboardBuilder()
        build_kb = BuildKb(NeponCbFactory, msg)
        yes = build_kb.get_button("✅", ButtonInfo.NONE, -1)
        kb.add(yes)
        markup = kb.as_markup()
    else:
        markup = None

    for i in config.ADMINS:
        await bot.send_message(i, "\n".join(m), reply_markup=markup)

    for i in config.TO_NOTIF:
        await bot.send_message(i, "\n".join(m), reply_markup=None)
