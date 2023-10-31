import asyncpg
import orjson
import structlog
from aiogram import Dispatcher

import utils
from data import config


class Database:
    def __init__(self, dispatcher: Dispatcher):
        self.dp = dispatcher
        self.db_name = config.PG_DATABASE
        self.user = config.PG_USER
        self.password = config.PG_PASSWORD
        self.host = config.PG_HOST
        self.port = config.PG_PORT
        self.pool = None
        self.logger: structlog.typing.FilteringBoundLogger = self.dp["business_logger"]
        self.logger.debug("Connecting to PostgreSQL", db=self.db_name)

    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(
                database=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.dp["db_pool"] = self.pool
            self.dp["temp_bot_cloud_session"] = utils.smart_session.SmartAiogramAiohttpSession(
                json_loads=orjson.loads,
                logger=self.dp["aiogram_session_logger"],
            )

            self.logger.debug("Succesfully connected to PostgreSQL", db=self.db_name)
        except asyncpg.exceptions.PostgresError as e:
            self.logger.error(f"Error connecting to the database: {e}", db=self.db_name)

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            self.logger.debug("Disconnected from the database", db=self.db_name)

    async def execute_query(self, query, *args):
        """
        :param query: SQL request with %s
        :param args: args to insert in %s
        """
        if self.pool:
            try:
                async with self.pool.acquire() as conn:
                    result = await conn.fetch(query, *args)
                return result
            except asyncpg.exceptions.PostgresError as e:
                self.logger.error(f"Error executing query: {e}", db=self.db_name)
                return None
        else:
            self.logger.error(f"Not connected to the database", db=self.db_name)
            return None

    async def create_table(self, table_name, columns):
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
            self.logger.error(f"Not connected to the database", db=self.db_name)

    async def insert_data(self, table_name, data):
        """
        :param table_name: Name of the table (expectly)
        :param data: columns in format {col_name: col_data}
        :type data: dict
        """
        if self.pool:
            columns = data.keys()
            values = [data[col] for col in columns]
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) " \
                    f"VALUES ({', '.join(['%s' for _ in range(len(values))])});"
            await self.execute_query(query, *values)
        else:
            self.logger.error(f"Not connected to the database", db=self.db_name)

    async def fetch_all_data(self, table_name):
        """
        Get all data from table
        :param table_name: Name of the table (expectly)
        """
        if self.pool:
            query = f"SELECT * FROM {table_name};"
            return await self.execute_query(query)
        else:
            self.logger.error(f"Not connected to the database", db=self.db_name)
            return None

    def get_user(self, user_id):
        return self.execute_query("SELECT * FROM members WHERE user_id=%s", (user_id,))

    def new_user(self, user_id, username):
        self.insert_data("members", {"user_id": user_id, "username": username, "karmas": 0, "vacancies": 0})

    def add_karmas(self, user_id, username, karmas):
        if not self.get_user(user_id):
            self.new_user(user_id, username)
        self.execute_query("UPDATE members SET karmas=karmas+%s WHERE user_id=%s", (karmas, user_id))

    def new_event(self, event_name, event_description):
        self.insert_data("events", {"event_name": event_name, "description": event_description})
