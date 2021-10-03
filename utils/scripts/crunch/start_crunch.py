import asyncio
import logging
import os

from aiogram.dispatcher.storage import FSMContextProxy

import data
from utils.misc.files import create_dirs


async def start_crunch(user_id: int, crunch_data: FSMContextProxy):
    sep = os.path.sep
    users_data_path = os.path.dirname(os.path.abspath(data.users.__file__)) + \
                      f"{sep}user_{user_id}{sep}scripts{sep}crunch"
    current_path = os.path.dirname(os.path.abspath(__file__))
    if crunch_data['is_template']:
        template_data = f"'-t {crunch_data['symbols']}'"
    else:
        template_data = f"' '"
    cmd = f"sh '{current_path}{sep}crunch.sh' {crunch_data['min_length']} {crunch_data['max_length']} " \
          f"{template_data} {users_data_path}{sep}passwords.txt"
    create_dirs(users_data_path)
    proc = await asyncio.create_subprocess_shell(
        cmd=cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    logging.info(f"[{cmd!r} exited with {proc.returncode}]")
    if stdout:
        logging.info(f"[stdout]\n{stdout.decode()}")
    if stderr:
        logging.info(f"[stderr]\n{stderr.decode()}")
    return users_data_path
