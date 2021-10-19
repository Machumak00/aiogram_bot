import asyncio
from asyncio.subprocess import Process

from loader import dp


async def stop_script():
    while await dp.current_state().get_state() != 'PaPackDdosHpingState:stopped_script':
        await asyncio.sleep(0.2)
