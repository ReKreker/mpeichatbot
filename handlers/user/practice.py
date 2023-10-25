from aiogram import Bot
from aiogram import html, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaDocument, InputMediaVideo, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data import config
from data.cb_data import PractCbFactory, ButtonCbFactory, ButtonInfo
from states.user import Activity


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
    await state.set_state(Activity.generated)


async def require_proofs(query: types.CallbackQuery, state: FSMContext, bot: Bot):
    await query.message.delete()
    await query.message.answer(
        "Вышли практику в виде картинок, видео или файла (предпочительно docx/pdf, но можно и zip).\n" + \
        "<b>Отправь любое сообщение, чтобы завершить передачу</b>"
    )

    data = ButtonCbFactory.unpack(query.data)
    await state.set_data({"id": data.id})
    await state.set_state(Activity.getting_proofs)
    return await bot.answer_callback_query(callback_query_id=query.id)


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
    await state.set_state(Activity.next_proof)


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
    await state.set_state(Activity.next_proof)


async def forward(msg: types.Message, state: FSMContext, bot: Bot) -> None:
    # TODO: получить название практики по data["id"]
    data = await state.get_data()
    name = "Практика 1"

    user = msg.from_user
    m = [
        f"<a href='tg://user?id={user.id}'>{html.quote(user.full_name)}</a> прислал practice!",
        name
    ]

    kb = InlineKeyboardBuilder()

    no_button = PractCbFactory(
        user_id=msg.from_user.id,
        reply_msg_id=msg.message_id,
        button=ButtonCbFactory(
            id=data["id"],
            button=ButtonInfo.NO
        ).pack()
    ).pack()
    kb.add(
        types.InlineKeyboardButton(
            text="🚫",
            callback_data=no_button
        ))

    yes_button = PractCbFactory(
        user_id=msg.from_user.id,
        reply_msg_id=msg.message_id,
        button=ButtonCbFactory(
            id=data["id"],
            button=ButtonInfo.YES
        ).pack()
    ).pack()
    kb.add(
        types.InlineKeyboardButton(
            text="✅",
            callback_data=yes_button
        ))
    kb.adjust(2)

    for i in config.ADMINS:
        await bot.send_media_group(i, data["proofs"])
        await bot.send_message(i, "\n".join(m), reply_markup=kb.as_markup())

    for i in config.TO_NOTIF:
        await bot.send_media_group(i, data["proofs"])
        await bot.send_message(i, "\n".join(m), reply_markup=None)

    await state.set_state(Activity.forwarded)
