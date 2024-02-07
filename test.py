from sqlalchemy.orm import declarative_base
import asyncio
import settings
from pymongo import MongoClient
import motor.motor_asyncio


async def main_func(query, *params):

    uri = f"mongodb+srv://slava:slava1990@cluster0.fduptu2.mongodb.net/callback_db"
    client = motor.motor_asyncio.AsyncIOMotorClient(uri)
    db = client["callback_db"]
    collection_name = settings.MONGODB_COLLECTION
    collection = db[collection_name]
    print(f"Client is: {client}")
    print(f"Collection is: {collection}")
    try:
        action, *params = params
        # Get the method from the collection object
        action_method = getattr(collection, action)
        # Execute the method and return
        print(f"action method is: {action_method}")
        if action in ["find_one", "insert_one", "sort", "update", "delete", "limit"]:
            # For methods that return a single document or modify the collection
            result = await action_method(query, *params)
            return result
        elif action in ["find"]:
            # For methods that return a cursor
            cursor = action_method(query, *params)
            results = await cursor.to_list(None)
            return results
        else:
            raise NotImplementedError(f"Method {action} is not supported.")
    finally:
        print(f"Client in finally: {client}")
        client.close()

if __name__ == "__main__":
    res = asyncio.run(main_func({
                                    "txId": "234",
                                    "createdAt": 54321,
                                    "status": "FAILED"
                                }, "insert_one",
                                ))
    print(res)




