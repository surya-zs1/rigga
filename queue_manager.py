import asyncio

download_queue=asyncio.Queue()


async def add_task(task):

    await download_queue.put(task)


async def get_task():

    return await download_queue.get()
