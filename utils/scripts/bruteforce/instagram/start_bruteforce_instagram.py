import asyncio
import logging
import os.path

from aiogram.dispatcher.storage import FSMContextProxy

import data


async def start_bruteforce_instagram(user_id: int, bruteforce_data: FSMContextProxy):
    users_data_path = os.path.dirname(os.path.abspath(data.users.__file__)) + f"/user_{user_id}/scripts/bruteforce/instagram"
    current_path = os.path.dirname(os.path.abspath(__file__))
    cmd = f"sh '{current_path}/bruteforce_instagram.sh' '{users_data_path}'"
    if not os.path.exists(users_data_path):
        os.makedirs(users_data_path)
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
