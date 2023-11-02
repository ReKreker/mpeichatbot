import asyncio

import asyncpg as asyncpg
import orjson
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

import handlers
import utils
from data import config
from data.database import Database
from middlewares import StructLoggingMiddleware


async def create_db_connections() -> None:
    db_pool = Database()
    await db_pool.connect()
    await db_pool.create_table("member",
                               [["user_id", "BIGINT"], ["username", "TEXT"], ["karmas", "INT"],
                                ["vacancies", "INT"]])

    await db_pool.create_table("user_event",
                               [["user_event_id", "SERIAL"], ["user_id", "BIGINT"], ["event_id", "INT"]])
    await db_pool.create_table("event",
                               [["event_id", "SERIAL"], ["event_name", "TEXT"], ["description", "TEXT"]])

    await db_pool.create_table("user_practice",
                               [["user_practice_id", "SERIAL"], ["user_id", "BIGINT"], ["practice_id", "INT"]])
    await db_pool.create_table("practice",
                               [["practice_id", "SERIAL"], ["practice_name", "TEXT"], ["description", "TEXT"]])

    await db_pool.create_table("nepon",
                               [["nepon_id", "SERIAL"], ["user_id", "BIGINT"],
                                ["time", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"]])

    await db_pool.create_table("quiz",
                               [["quiz_id", "SERIAL"], ["user_id", "BIGINT"],
                                ["time", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"]])
    await db_pool.disconnect()


async def close_db_connections(dp: Dispatcher) -> None:
    if "temp_bot_cloud_session" in dp.workflow_data:
        temp_bot_cloud_session: AiohttpSession = dp["temp_bot_cloud_session"]
        await temp_bot_cloud_session.close()
    if "temp_bot_local_session" in dp.workflow_data:
        temp_bot_local_session: AiohttpSession = dp["temp_bot_local_session"]
        await temp_bot_local_session.close()
    if "db_pool" in dp.workflow_data:
        db_pool: asyncpg.Pool = dp["db_pool"]
        await db_pool.close()


def setup_handlers(dp: Dispatcher) -> None:
    dp.include_router(handlers.user.prepare_router())
    dp.include_router(handlers.admin.prepare_router())
    dp.include_router(handlers.chat.prepare_router())


def setup_middlewares(dp: Dispatcher) -> None:
    dp.update.outer_middleware(StructLoggingMiddleware(logger=dp["aiogram_logger"]))


def setup_logging(dp: Dispatcher) -> None:
    dp["aiogram_logger"] = utils.logger.setup().bind(type="aiogram")
    dp["db_logger"] = utils.logger.setup().bind(type="db")
    dp["cache_logger"] = utils.logger.setup().bind(type="cache")


async def setup_aiogram(dp: Dispatcher) -> None:
    setup_logging(dp)
    logger = dp["aiogram_logger"]
    logger.debug("Configuring aiogram")
    await create_db_connections()
    setup_handlers(dp)
    setup_middlewares(dp)
    logger.info("Configured aiogram")


async def aiogram_on_startup_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await setup_aiogram(dispatcher)
    dispatcher["aiogram_logger"].info("Started polling")


async def aiogram_on_shutdown_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    dispatcher["aiogram_logger"].debug("Stopping polling")
    await close_db_connections(dispatcher)
    await bot.session.close()
    await dispatcher.storage.close()
    dispatcher["aiogram_logger"].info("Stopped polling")


def main() -> None:
    aiogram_session_logger = utils.logger.setup().bind(type="aiogram_session")

    session = utils.smart_session.SmartAiogramAiohttpSession(
        json_loads=orjson.loads,
        logger=aiogram_session_logger,
    )
    bot = Bot(config.BOT_TOKEN, parse_mode="HTML", session=session)

    dp = Dispatcher()
    dp["aiogram_session_logger"] = aiogram_session_logger
    dp["bot"] = bot
    dp["business_logger"] = utils.logger.setup().bind(type="business")
    dp.startup.register(aiogram_on_startup_polling)
    dp.shutdown.register(aiogram_on_shutdown_polling)
    db = Database()
    dp["db"] = db

    asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":
    main()
