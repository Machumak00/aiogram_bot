from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils import on_startup_notify, set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
