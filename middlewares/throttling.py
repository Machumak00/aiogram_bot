import asyncio
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood'):
        self.limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def throttle(self, target: Union[types.Message, types.CallbackQuery]):
        handler = current_handler.get()
        if not handler:
            return
        dp = Dispatcher.get_current()
        limit = getattr(handler, "throttling_rate_limit", self.limit)
        key = getattr(handler, "throttling_key", f"{self.prefix}_{handler.__name__}")
        try:
            await dp.throttle(key, rate=limit)
        except Throttled as t:
            await self.target_throttled(target, t, dp, key)
            raise CancelHandler()

    async def target_throttled(self, target: Union[types.Message, types.CallbackQuery],
                               throttled: Throttled, dispatcher: Dispatcher, key: str):
        msg = target.message if isinstance(target, types.CallbackQuery) else target
        delta = round(throttled.rate - throttled.delta, 2)
        if throttled.exceeded_count == 2:
            await msg.reply(f"Вы выполняете слишком много попыток к этому запросу.\n"
                            f"Попробуйте снова через {delta}.")
            return
        await asyncio.sleep(delta)
        thr = await dispatcher.check_key(key)
        if thr.exceeded_count == throttled.exceeded_count:
            await msg.reply(f"Теперь я могу Вам отвечать на этот запрос.")

    async def on_process_message(self, message, data):
        await self.throttle(message)

    async def on_process_callback_query(self, call, data):
        await self.throttle(call)
