import asyncio
import logging
import os

from aiogram.dispatcher.storage import FSMContextProxy

import data


async def start_msfvenom(user_id: int, msfvenom_data: FSMContextProxy):
    users_data_path = os.path.dirname(os.path.abspath(data.users.__file__)) + f"/user_{user_id}/scripts/msfvenom"
    current_path = os.path.dirname(os.path.abspath(__file__))
    cmd = f"sh '{current_path}/msfvenom_{msfvenom_data['system']}.sh' '{users_data_path}' {msfvenom_data['ip']} {msfvenom_data['port']} {msfvenom_data['file_name']}"
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
    return users_data_path + '/' + msfvenom_data['file_name']
