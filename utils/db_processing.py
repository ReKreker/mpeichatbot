from __future__ import annotations

import asyncpg

from data.database import Database


async def get_undone_x(database: Database, user_id: int) -> dict[str, str | list[asyncpg.Record]]:
    all_x = await database.get_all_x()
    if not all_x:
        return {"msg": "Нечего сдавать", "data": ()}
    all_ids = [i.get("id") for i in all_x]

    done = await database.get_all_user_x_by_user_id(user_id)
    if done is None:
        return {"msg": "", "data": all_x}

    undone = ()
    done_ids = [i.get("id") for i in done]
    if len(done_ids) == len(all_ids):
        return {"msg": "Все сдано", "data": ()}

    for x in all_x:
        if x.get("id") not in done_ids:
            undone += (x,)
    return {"msg": "", "data": undone}


async def mark_as_done(database: Database, user_id: int, x_id: int):
    all_x = await database.get_all_x()
    if not all_x:
        return "Нечего сдавать"

    all_ids = [i.get("id") for i in all_x]
    if x_id not in all_ids:
        return "Невозможно сдать"

    done = await database.get_all_user_x_by_user_id(user_id)
    if done is None:
        await database.new_user_x(user_id, x_id)
        return "Добавление баллов!"

    done_ids = [i.get("id") for i in done]
    if x_id in done_ids:
        return "Уже было сдано"

    await database.new_user_x(user_id, x_id)
    return "Добавление баллов"


async def fully_del_x(database: Database, name: str):
    all_x = await database.get_all_x()
    x_id = -1
    for x in all_x:
        if x.get("name") == name:
            x_id = x.get("id")

    if x_id == -1:
        return "Не найден идентификатор для удаления"

    to_delete = await database.get_all_user_x_by_id(x_id)

    await database.del_x_by_name(name)
    for i in to_delete:
        await database.del_user_x(i.get("union_id"))

    return f"'{name}' успешно удалено"
