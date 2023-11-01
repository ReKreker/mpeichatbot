from aiogram import html, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaDocument, InputMediaVideo, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data import config
from data.cb_data import ButtonInfo
from utils.keyboards import BuildKb


async def proof_handler(msg: types.Message, state: FSMContext) -> None:
    media = None
    if msg.document is not None:
        media = InputMediaDocument(media=msg.document.file_id)
    elif msg.video is not None:
        media = InputMediaVideo(media=msg.video.file_id)
    elif msg.photo is not None:
        media = InputMediaPhoto(media=msg.photo[-1].file_id)

    if media is None:
        return
    await state.update_data(proofs=[media])
    data = await state.get_data()
    state_group = data["group"]
    await state.set_state(state_group.next_proof)


async def next_proof_handler(msg: types.Message, state: FSMContext) -> None:
    media = None
    if msg.document is not None:
        media = InputMediaDocument(media=msg.document.file_id)
    elif msg.video is not None:
        media = InputMediaVideo(media=msg.video.file_id)
    elif msg.photo is not None:
        media = InputMediaPhoto(media=msg.photo[-1].file_id)

    if media is None:
        return
    data = await state.get_data()
    data["proofs"].append(media)
    await state.set_data(data)
    state_group = data["group"]
    await state.set_state(state_group.next_proof)


async def forward(msg: types.Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    x_id = data["id"]
    db = data["db"]
    cb_factory = data["cb_factory"]
    state_group = data["group"]

    await db.connect()
    info = await db.get_x_by_id(x_id)
    await db.disconnect()
    name, decs = info[0].values()

    m = [
        f"<a href='{msg.from_user.url}'>{html.quote(msg.from_user.full_name)}</a> прислал:",
        f"<b>{name}</b>",
        decs
    ]

    kb = InlineKeyboardBuilder()
    build_kb = BuildKb(cb_factory, msg)
    no = build_kb.get_button("🚫", ButtonInfo.NO, -1)
    yes = build_kb.get_button("✅", ButtonInfo.YES, x_id)
    # TODO: добавить возможность отписать что-то пользователю
    # reply = build_kb.get_button("reply", ButtonInfo.REPLY, -1)
    kb.add(no)
    kb.add(yes)

    for i in config.ADMINS:
        await bot.send_media_group(i, data["proofs"])
        await bot.send_message(i, "\n".join(m), reply_markup=kb.as_markup())

    for i in config.TO_NOTIF:
        await bot.send_media_group(i, data["proofs"])
        await bot.send_message(i, "\n".join(m), reply_markup=None)

    await state.set_state(state_group.forwarded)
