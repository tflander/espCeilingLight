from asyncio import *

total_sleep_time_ms = 0


async def sleep_ms(time_ms):
    global total_sleep_time_ms
    total_sleep_time_ms += time_ms
