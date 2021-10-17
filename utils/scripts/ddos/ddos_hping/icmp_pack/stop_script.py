import asyncio
from asyncio.subprocess import Process

from loader import dp


async def stop_script(proc: Process):
    while await dp.current_state().get_state() != 'IcmpPackDdosHpingState:stopped_script':
        await asyncio.sleep(0.2)
    proc.kill()
