from aiogram import Bot
from aiogram import html, types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data import config
from data.cb_data import QuizCbFactory, ButtonInfo
from utils.keyboards import BuildKb


async def gen_menu(msg: types.Message, bot: Bot) -> None:
    if msg.from_user is None:
        return

    await msg.reply("Отправлено на проверку")

    m = f"<a href='{msg.from_user.url}'>{html.quote(msg.from_user.full_name)}</a> победитель квиза?"

    kb = InlineKeyboardBuilder()
    build_kb = BuildKb(QuizCbFactory, msg)
    no = build_kb.get_button("🚫", ButtonInfo.NO, -1)
    yes = build_kb.get_button("✅", ButtonInfo.YES, -1)
    kb.add(no)
    kb.add(yes)
    kb.adjust(2)

    for i in config.ADMINS:
        await bot.send_message(i, m, reply_markup=kb.as_markup())

    for i in config.TO_NOTIF:
        await bot.send_message(i, m, reply_markup=None)
