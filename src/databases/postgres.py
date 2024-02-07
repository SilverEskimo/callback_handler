from src.interfaces import DatabaseInterface
import asyncpg
from asyncpg import Connection


class PostgresDB(DatabaseInterface):
    def __init__(self):
        self.conn: Connection = None

    async def connect(self, host: str, port: int, user: str, password: str, database: str):
        try:
            self.conn = await asyncpg.connect(host=host, port=port, user=user, password=password, database=database)
        except Exception as e:
            raise Exception(e)

    async def disconnect(self):
        try:
            if self.conn:
                await self.conn.close()
        except Exception as e:
            raise Exception(e)

    async def execute_query(self, query: str, *params):
        if not self.conn:
            raise RuntimeError("Database connection is not established.")
        return await self.conn.fetch(query, *params)

