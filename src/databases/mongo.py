from src import settings
from src.interfaces import DatabaseInterface
from pymongo.database import Database
import motor.motor_asyncio


class MongoDB(DatabaseInterface):
    def __init__(self):
        self.client: motor.MotorClient = None
        self.db: Database = None

    async def connect(self, host: str, port: int, user: str, password: str, database: str):
        # Construct MongoDB connection URI
        uri = f"mongodb+srv://{user}:{password}@{host}/{database}"
        self.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client[database]

    async def disconnect(self):
        if self.client:
            self.client.close()

    async def execute_query(self, query, *params):
        if self.db is None:
            raise RuntimeError("MongoDB connection is not established.")

        collection_name = settings.DB_TABLE
        collection = self.db[collection_name]
        action, *params = params
        # Get the method from the collection object
        action_method = getattr(collection, action)

        supported_methods = {
            "find_one", "insert_one", "insert_many",
            "sort", "update", "delete_one",
            "delete_many", "limit"
        }
        if action in supported_methods:
            # For methods that return a single document or modify the collection
            result = await action_method(query, *params)
            return result
        elif action == "find":
            # For methods that return a cursor
            cursor = action_method(query, *params)
            results = await cursor.to_list(None)
            return results
        else:
            raise NotImplementedError(f"Method '{action}' is not supported.")

