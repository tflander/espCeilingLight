from asyncio import *


async def sleep_ms(time_ms):
    await sleep(time_ms / 1000)
