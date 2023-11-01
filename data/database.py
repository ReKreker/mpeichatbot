import asyncpg
import orjson
import structlog
from aiogram import Dispatcher

import utils
from data import config


class Database:
    def __init__(self):
        # self.dp = dispatcher
        self.db_name = config.PG_DATABASE
        self.user = config.PG_USER
        self.password = config.PG_PASSWORD
        self.host = config.PG_HOST
        self.port = config.PG_PORT
        self.pool = None
        # self.logger: structlog.typing.FilteringBoundLogger = self.dp["business_logger"]
        # self.logger.debug("Connecting to PostgreSQL", db=self.db_name)

    async def connect(self) -> None:
        try:
            self.pool = await asyncpg.create_pool(
                database=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            # self.dp["db_pool"] = self.pool
            # self.dp["temp_bot_cloud_session"] = utils.smart_session.SmartAiogramAiohttpSession(
            #     json_loads=orjson.loads,
            #     logger=self.dp["aiogram_session_logger"],
            # )

            # self.logger.debug("Successfully connected to PostgresSQL", db=self.db_name)
        except asyncpg.exceptions.PostgresError:
            pass
            # self.logger.error(f"Error connecting to the database: {e}", db=self.db_name)

    async def disconnect(self) -> None:
        if self.pool:
            await self.pool.close()
            # self.logger.debug("Disconnected from the database", db=self.db_name)

    async def execute_query(self, query: str, *args) -> None | list[asyncpg.Record]:
        """
        :param query: SQL request with $1, $2
        :param args: args to insert in $1, $2
        """
        if self.pool:
            try:
                async with self.pool.acquire() as conn:
                    result = await conn.fetch(query, *args)
                return result
            except asyncpg.exceptions.PostgresError as e:
                print(e)
                # self.logger.error(f"Error executing query: {e}", db=self.db_name)
                return None
        else:
            # self.logger.error(f"Not connected to the database", db=self.db_name)
            return None

    async def create_table(self, table_name, columns) -> None:
        """
        :param table_name: Name of the table (expectly)
        :param columns: columns in format [col_name, col_type (INTEGER, TEXT...)]
        :type columns: list
        """
        if self.pool:
            query = f"CREATE TABLE IF NOT EXISTS {table_name} " \
                    f"({', '.join([f'{col_name} {col_type}' for col_name, col_type in columns])});"
            await self.execute_query(query)
        else:
            pass
            # self.logger.error(f"Not connected to the database", db=self.db_name)

    async def insert_data(self, table_name, data) -> None:
        """
        :param table_name: Name of the table (expectly)
        :param data: columns in format {col_name: col_data}
        :type data: dict
        """
        if self.pool:
            columns = data.keys()
            values = [data[col] for col in columns]
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) " \
                    f"VALUES ({', '.join([f'${i + 1}' for i in range(len(values))])});"
            await self.execute_query(query, *values)
        else:
            pass
            # self.logger.error(f"Not connected to the database", db=self.db_name)

    async def get_user(self, user_id) -> list[asyncpg.Record]:
        return await self.execute_query("SELECT * FROM member WHERE user_id=$1", user_id)

    async def new_user(self, user_id, username) -> None:
        await self.insert_data("member", {"user_id": user_id, "username": username, "karmas": 0, "vacancies": 0})

    async def add_karmas(self, user_id, username, karmas) -> None:
        if not self.get_user(user_id):
            await self.new_user(user_id, username)
        await self.execute_query("UPDATE member SET karmas=karmas+$1 WHERE user_id=$2", (karmas, user_id))

    async def new_event(self, event_name, event_description):
        await self.insert_data("event", {"event_name": event_name, "description": event_description})

    async def del_event_by_name(self, event_name):
        await self.execute_query("DELETE FROM event WHERE event_name=$1", (event_name,))

    async def new_user_event(self, user_id, event_id):
        await self.insert_data("user_event", {"user_id": user_id, "id": event_id})

    async def get_events(self):
        return await self.execute_query("SELECT event_id, event_name FROM event ORDER BY event_id DESC")

    async def get_event_by_id(self, event_id):
        return await self.execute_query("SELECT event_name, description FROM event WHERE event_id=$1", (event_id,))
