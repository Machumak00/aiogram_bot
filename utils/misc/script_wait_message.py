from asyncio import sleep

from aiogram.types import Message


async def script_wait_message(message: Message):
    while True:
        await sleep(5)
        await message.answer('Идёт выполнение скрипта. Пожалуйста, подождите...')