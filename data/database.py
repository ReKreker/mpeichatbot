from __future__ import annotations

from abc import ABC, abstractmethod

import asyncpg

from data import config


class Strategy(ABC):
    @classmethod
    @abstractmethod
    def new_x_args(cls, name: str, descr: str) -> tuple:
        pass

    @classmethod
    @abstractmethod
    def del_x_by_name_args(cls, name: str) -> tuple:
        pass

    @classmethod
    @abstractmethod
    def del_user_x_args(cls, union_id: int) -> tuple:
        pass

    @classmethod
    @abstractmethod
    def new_user_x_args(cls, user_id: int, x_id: int) -> tuple:
        pass

    @classmethod
    @abstractmethod
    def get_all_user_x_by_user_id_args(cls, user_id: int) -> tuple:
        pass

    @classmethod
    @abstractmethod
    def get_all_user_x_by_id_args(cls, x_id: int) -> tuple:
        pass

    @classmethod
    @abstractmethod
    def get_all_x_args(cls) -> tuple:
        pass

    @classmethod
    @abstractmethod
    def get_x_by_id_args(cls, x_id: int) -> tuple:
        pass


class EmptyStrategy(Strategy):
    def new_x_args(self, name: str, descr: str) -> tuple:
        return ()

    def del_x_by_name_args(self, name: str) -> tuple:
        return ()

    def del_user_x_args(self, union_id: int) -> tuple:
        return ()

    def new_user_x_args(self, user_id: int, x_id: int) -> tuple:
        return ()

    def get_all_user_x_by_user_id_args(self, user_id: int) -> tuple:
        return ()

    def get_all_user_x_by_id_args(self, x_id: int) -> tuple:
        return ()

    def get_all_x_args(self) -> tuple:
        return ()

    def get_x_by_id_args(self, x_id: int) -> tuple:
        return ()


class EventStrategy(Strategy):
    def new_x_args(self, name: str, descr: str) -> tuple:
        return "event", {"event_name": name, "description": descr}

    def del_x_by_name_args(self, name: str) -> tuple:
        return "DELETE FROM event WHERE event_name=$1", name

    def del_user_x_args(self, union_id: int) -> tuple:
        return "DELETE FROM user_event WHERE user_event_id=$1", union_id

    def new_user_x_args(self, user_id: int, x_id: int) -> tuple:
        return "user_event", {"user_id": user_id, "event_id": x_id}

    def get_all_user_x_by_user_id_args(self, user_id: int) -> tuple:
        return "SELECT event_id AS id FROM user_event WHERE user_id=$1", user_id

    def get_all_user_x_by_id_args(self, x_id: int) -> tuple:
        return "SELECT user_event_id AS union_id, event_id AS id FROM user_event WHERE event_id=$1", x_id

    def get_all_x_args(self) -> tuple:
        return ("SELECT event_id AS id, event_name AS name FROM event ORDER BY event_id DESC",)

    def get_x_by_id_args(self, x_id: int) -> tuple:
        return "SELECT event_name AS name, description AS decsr FROM event WHERE event_id=$1", x_id


class PracticeStrategy(Strategy):
    def new_x_args(self, name: str, descr: str) -> tuple:
        return "practice", {"practice_name": name, "description": descr}

    def del_x_by_name_args(self, name: str) -> tuple:
        return "DELETE FROM practice WHERE practice_name=$1", name

    def del_user_x_args(self, union_id: int) -> tuple:
        return "DELETE FROM user_practice WHERE user_practice_id=$1", union_id

    def new_user_x_args(self, user_id: int, x_id: int) -> tuple:
        return "user_practice", {"user_id": user_id, "practice_id": x_id}

    def get_all_user_x_by_user_id_args(self, user_id: int) -> tuple:
        return "SELECT practice_id AS id FROM user_practice WHERE user_id=$1", user_id

    def get_all_user_x_by_id_args(self, x_id: int) -> tuple:
        return "SELECT user_practice_id AS union_id, practice_id AS id FROM user_practice WHERE practice_id=$1", x_id

    def get_all_x_args(self) -> tuple:
        return ("SELECT practice_id AS id, practice_name AS name FROM practice ORDER BY practice_id DESC",)

    def get_x_by_id_args(self, x_id: int) -> tuple:
        return "SELECT practice_name AS name, description AS decsr FROM practice WHERE practice_id=$1", x_id


strategies = {
    "event": EventStrategy,
    "practice": PracticeStrategy,
}


class Database:
    def __init__(self, strategy: str = ""):
        # self.dp = dispatcher
        self.db_name = config.PG_DATABASE
        self.user = config.PG_USER
        self.password = config.PG_PASSWORD
        self.host = config.PG_HOST
        self.port = config.PG_PORT
        self.pool = None
        strat = strategies.get(strategy)
        if strat is None:
            strat = EmptyStrategy
        self.strat = strat()

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

    async def new_x(self, name: str, descr: str) -> None:
        args = self.strat.new_x_args(name, descr)
        await self.insert_data(*args)

    async def del_x_by_name(self, name: str) -> None:
        args = self.strat.del_x_by_name_args(name)
        await self.execute_query(*args)

    async def del_user_x(self, union_id: int) -> None:
        args = self.strat.del_user_x_args(union_id)
        await self.execute_query(*args)

    async def new_user_x(self, user_id: int, x_id: int) -> None:
        args = self.strat.new_user_x_args(user_id, x_id)
        await self.insert_data(*args)

    async def get_all_user_x_by_user_id(self, user_id: int) -> list[asyncpg.Record] | None:
        args = self.strat.get_all_user_x_by_user_id_args(user_id)
        return await self.execute_query(*args)

    async def get_all_user_x_by_id(self, x_id: int) -> list[asyncpg.Record] | None:
        args = self.strat.get_all_user_x_by_id_args(x_id)
        return await self.execute_query(*args)

    async def get_all_x(self) -> list[asyncpg.Record]:
        args = self.strat.get_all_x_args()
        return await self.execute_query(*args)

    async def get_x_by_id(self, x_id: int) -> list[asyncpg.Record]:
        args = self.strat.get_x_by_id_args(x_id)
        return await self.execute_query(*args)
