import os
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(os.environ["MONGO_URL"])

db = client.leechbot
files = db.files


async def get_cached(url):

    return await files.find_one({"url": url})


async def save_cache(url, file_id):

    await files.insert_one({
        "url": url,
        "file_id": file_id
    })
