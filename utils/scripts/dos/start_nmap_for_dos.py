import asyncio
import logging
import os.path
import re

from aiogram.dispatcher.storage import FSMContextProxy
from aiogram.types import Message

import utils


async def start_nmap(message: Message, nmap_data: FSMContextProxy):
    current_path = os.path.dirname(os.path.abspath(utils.scripts.nmap.__file__))
    cmd = f"sh '{current_path}/nmap.sh' {nmap_data['ip']}"
    proc = await asyncio.create_subprocess_shell(
        cmd=cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    stdout_decoded = stdout.decode()
    stderr_decoded = stderr.decode()
    logging.info(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        logging.info(f'[stdout]\n{stdout_decoded}')
    if stderr:
        logging.info(f'[stderr]\n{stderr_decoded}')
    not_found_addresses = re.search(r"^Nmap done: 0 IP$", stdout_decoded)
    if not_found_addresses:
        return nmap_data['ip'], None
    ports = re.findall(r"(\d+)/tcp\s+open", stdout_decoded)
    return nmap_data['ip'], ports
